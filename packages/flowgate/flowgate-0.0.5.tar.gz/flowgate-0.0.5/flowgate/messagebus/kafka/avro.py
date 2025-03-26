import time
from functools import partial
from typing import Callable

import structlog
from confluent_kafka import KafkaError, KafkaException

from flowgate.services.kafka.avro.consumer import AvroConsumer
from flowgate.services.kafka.avro.message import Message
from flowgate.services.kafka.avro.producer import AvroProducer

from flowgate.messagebus.base import MessageBusBackend
from flowgate.messagebus.kafka.config import (
    get_consumer_config,
    get_offset_watchdog_config,
    get_producer_config,
)
from flowgate.messagebus.kafka.offset_watchdog import OffsetWatchdog
from flowgate.serializers import to_message_from_dto

logger = structlog.get_logger(__name__)


class KafkaAvroBackend(MessageBusBackend):
    def __init__(
        self,
        config: dict,
        producer: AvroProducer = AvroProducer,
        consumer: AvroConsumer = AvroConsumer,
        value_serializer: Callable = to_message_from_dto,
        get_producer_config: Callable = get_producer_config,
        get_consumer_config: Callable = get_consumer_config,
        get_offset_watchdog_config: Callable = get_offset_watchdog_config,
    ) -> None:
        self.consumer = None
        self.producer = None
        self.offset_watchdog = None

        producer_config = get_producer_config(config)
        consumer_config = get_consumer_config(config)
        offset_wd_config = get_offset_watchdog_config(config)

        if producer_config:
            self.flush = producer_config.pop("flush", False)
            self.producer = producer(producer_config, value_serializer=value_serializer)
        if consumer_config:
            self.consumer = partial(consumer, config=consumer_config)
        if offset_wd_config:
            self.offset_watchdog = OffsetWatchdog(offset_wd_config)

    def should_process(self, message: Message) -> bool:
        return not self.offset_watchdog or not self.offset_watchdog.seen(message)

    def mark_processed(self, message: Message):
        if self.offset_watchdog:
            try:
                self.offset_watchdog.set_seen(message)
            except Exception:
                logger.exception("Failed to set offset, but will continue")

    def handle(
        self, handler: Callable, message: Message, consumer: AvroConsumer
    ) -> None:
        start_time = time.time()
        if not self.should_process(message):
            return
        handler(message)
        self.mark_processed(message)
        if not consumer.is_auto_commit:
            try:
                consumer.commit(asynchronous=False)
            except KafkaException as e:
                if e.args[0].code() == KafkaError._NO_OFFSET:
                    logger.warning("Offset already committed")
                else:
                    raise
        end_time = time.time() - start_time
        logger.debug(f"Message processed in {end_time:.5f}s")

    def produce(
        self, value: dict, key: str = None, topic: str = None, **kwargs
    ) -> None:
        if self.producer is None:
            raise ValueError("Producer is not configured")

        while True:
            try:
                self.producer.produce(key=key, value=value, topic=topic, **kwargs)
                break
            except BufferError:
                self.producer.poll(timeout=0.5)
            continue

        self.producer.poll(0)

        if self.flush:
            self.producer.flush()

    def get_consumer(self) -> AvroConsumer:
        if self.consumer is None:
            raise ValueError("Consumer is not configured")
        return self.consumer

    def consume(self, handler: Callable) -> None:
        if not callable(handler):
            raise ValueError("You must pass a message handler")
        Consumer = self.get_consumer()
        with Consumer() as consumer:
            for message in consumer:
                self._handle(handler, message, consumer)
