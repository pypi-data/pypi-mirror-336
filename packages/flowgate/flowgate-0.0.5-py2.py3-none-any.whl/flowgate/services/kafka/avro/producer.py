import atexit

import structlog
from confluent_kafka.avro import AvroProducer as ConfluentAvroProducer

from flowgate.services.kafka.avro.config import KAFKA_PRODUCER_DEFAULT_CONFIG
from flowgate.services.kafka.avro.exceptions import (
    KafkaTopicNotRegistered,
    SchemaNotFound,
)
from flowgate.services.kafka.avro.schema_registry import AvroSchemaRegistry

logger = structlog.get_logger(__name__)


class AvroProducer(ConfluentAvroProducer):
    def __init__(
        self,
        config,
        value_serializer=None,
        schema_registry=AvroSchemaRegistry,
        **kwargs,
    ):
        config = {**KAFKA_PRODUCER_DEFAULT_CONFIG, **config}

        schema_registry_url = config["schema.registry.url"]
        self.schema_registry = schema_registry(schema_registry_url)
        self.value_serializer = config.pop("value_serializer", value_serializer)

        self.bootstrap_servers = config["bootstrap.servers"]
        self.client_id = config["client.id"]

        topics = config.pop("topics")
        self.topic_schemas = self._get_topic_schemas(topics)

        default_topic_schema = next(iter(self.topic_schemas.values()))
        self.default_topic, *_ = default_topic_schema

        logger.info("Initializing producer", config=config)
        atexit.register(self._close)

        super().__init__(config, **kwargs)

    def _close(self):
        logger.info("Flushing producer")
        super().flush()

    def _get_subject_names(self, topic):
        key_subject_name = f"{topic}-key"
        value_subject_name = f"{topic}-value"
        return key_subject_name, value_subject_name

    def _get_topic_schemas(self, topics):
        topic_schemas = {}
        for topic in topics:
            key_name, value_name = self._get_subject_names(topic)
            try:
                key_schema = self.schema_registry.get_latest_schema(key_name)
            except SchemaNotFound:
                key_schema = None
            value_schema = self.schema_registry.get_latest_schema(value_name)
            topic_schemas[topic] = (topic, key_schema, value_schema)

        return topic_schemas

    def produce(self, value, key=None, topic=None, headers=None, **kwargs):
        if headers is None:
            headers = {}
        topic = topic or self.default_topic
        try:
            _, key_schema, value_schema = self.topic_schemas[topic]
        except KeyError:
            raise KafkaTopicNotRegistered(f"Topic {topic} is not registered")

        if self.value_serializer:
            value = self.value_serializer(value)

        message_class = value.get("class") if isinstance(value, dict) else None
        resource_name = f"{topic}:{message_class}" if message_class else topic

        logger.info(
            "Producing message", topic=topic, key=key, value=value, headers=headers
        )

        super().produce(
            topic=topic,
            key=key,
            value=value,
            key_schema=key_schema,
            value_schema=value_schema,
            headers=headers,
            **kwargs,
        )

    def flush(self, *args, **kwargs):
        logger.info("Flushing producer")
        super().flush(*args, **kwargs)

    def poll(self, *args, **kwargs):
        super().poll(*args, **kwargs)
