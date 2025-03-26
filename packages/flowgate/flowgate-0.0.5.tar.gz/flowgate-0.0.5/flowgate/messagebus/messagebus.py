from typing import Callable, Dict, Type

import structlog

from flowgate.messagebus.kafka import KafkaAvroBackend
from flowgate.messagebus.testing import KafkaMockBackend
from flowgate.messagebus.base import MessageBusBackend

BACKENDS: Dict[str, Type[MessageBusBackend]] = {
    "kafka_avro": KafkaAvroBackend,
    "mock": KafkaMockBackend,
}

logger = structlog.get_logger(__name__)


class MessageBus:

    DEFAULT_BACKEND = "kafka_avro"

    def __init__(self, config: dict, **kwargs) -> None:
        backend = BACKENDS.get(config.get("backend", self.DEFAULT_BACKEND))
        logger.debug("Using message bus backend", backend=backend.__name__)
        self.backend = backend(config, **kwargs)

    def produce(self, value, key=None, **kwargs):
        self.backend.produce(key=key, value=value, **kwargs)

    def get_consumer(self):
        return self.backend.get_consumer()

    def consume(self, handler: Callable):
        self.backend.consume(handler)
