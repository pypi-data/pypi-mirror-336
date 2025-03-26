import socket
from functools import partial
from typing import Callable

import structlog
from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.avro import AvroConsumer as ConfluentAvroConsumer

from flowgate.services.kafka.avro.exceptions import (
    PartitionEndReached,
    KafkaBrokerTransportError,
)
from flowgate.services.kafka.avro.message import Message
from flowgate.services.kafka.avro.utils import retry_exception

logger = structlog.get_logger(__name__)


@retry_exception(exceptions=[KafkaBrokerTransportError])
def get_message(consumer, error_handler, timeout=0.1, stop_on_eof=False):
    message = consumer.poll(timeout=timeout)
    if message is None:
        return None

    if message.error():
        try:
            error_handler(message.error())
        except PartitionEndReached:
            if stop_on_eof:
                raise
            else:
                return None

    return message


def default_error_handler(kafka_error):
    code = kafka_error.code()
    if code == KafkaError._PARTITION_EOF:
        raise PartitionEndReached
    elif code == KafkaError._TRANSPORT:
        raise KafkaBrokerTransportError(kafka_error)
    else:
        raise KafkaException(kafka_error)


class AvroConsumer:
    DEFAULT_CONFIG = {
        "client.id": socket.gethostname(),
        "default.topic.config": {"auto.offset.reset": "earliest"},
        "enable.auto.commit": False,
        "fetch.wait.max.ms": 1000,
        "fetch.min.bytes": 10000,
        "log.connection.close": False,
        "log.thread.name": False,
    }

    def __init__(
        self,
        config,
        get_message: Callable = get_message,
        error_handler: Callable = default_error_handler,
        **kwargs,
    ) -> None:
        stop_on_eof = config.pop("stop_on_eof", False)
        poll_timeout = config.pop("poll_timeout", 0.1)
        self.non_blocking = config.pop("non_blocking", False)

        self.config = {**self.DEFAULT_CONFIG, **config}
        self.topics = self._get_topics(self.config)

        self.client_id = self.config["client.id"]
        self.bootstrap_servers = self.config["bootstrap.servers"]
        self.group_id = self.config["group.id"]

        logger.info("Initializing consumer", config=self.config)
        self.consumer = ConfluentAvroConsumer(self.config, **kwargs)
        self.consumer.subscribe(self.topics)

        self._generator = self._message_generator()

        self._get_message = partial(
            get_message,
            consumer=self.consumer,
            error_handler=error_handler,
            timeout=poll_timeout,
            stop_on_eof=stop_on_eof,
        )

    def __getattr__(self, name):
        return getattr(self.consumer, name)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._generator)
        except PartitionEndReached:
            raise StopIteration

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        logger.info("Closing consumer")
        self.consumer.close()
        self._generator.close()

    def _message_generator(self):
        while True:
            message = self._get_message()
            if message is None:
                if self.non_blocking:
                    yield None
                continue

            value, resource_name = message.value(), message.topic()
            message_class = value.get("class") if isinstance(value, dict) else None

            message = Message(message)
            yield message

    def _get_topics(self, config):
        topics = config.pop("topics", None)
        if topics is None:
            raise ValueError("You must subscribe to at least one topic")

        if not isinstance(topics, list):
            topics = [topics]

        return topics

    @property
    def is_auto_commit(self):
        return self.config.get("enable.auto.commit", True)

    def commit(self, *args, **kwargs):
        self.consumer.commit(*args, **kwargs)


class AvroLazyConsumer(ConfluentAvroConsumer):
    def poll(self, timeout=None):
        if timeout is None:
            timeout = -1

        message = Consumer.poll(self, timeout)
        return message

    def decode_message(self, message):
        if not message.error():
            if message.value() is not None:
                decoded_value = self._serializer.decode_message(message.value())
                message.set_value(decoded_value)

            if message.key() is not None:
                decoded_key = self._serializer.decode_message(message.key())
                message.set_key(decoded_key)
        return message
