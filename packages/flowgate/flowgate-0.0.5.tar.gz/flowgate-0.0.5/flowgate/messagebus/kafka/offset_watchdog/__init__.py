from typing import Dict, Type

import structlog

from flowgate.services.kafka.avro.message import Message
from flowgate.messagebus.kafka.offset_watchdog.base import (
    OffsetWatchdogBackend,
)
from flowgate.messagebus.kafka.offset_watchdog.memory import (
    InMemoryOffsetWatchdogBackend,
)
from flowgate.messagebus.kafka.offset_watchdog.null import (
    NullOffsetWatchdogBackend,
)
from flowgate.messagebus.kafka.offset_watchdog.redis import (
    RedisOffsetWatchdogBackend,
)

BACKENDS: Dict[str, Type[OffsetWatchdogBackend]] = {
    "null": NullOffsetWatchdogBackend,
    "memory": InMemoryOffsetWatchdogBackend,
    "redis": RedisOffsetWatchdogBackend,
}

logger = structlog.get_logger(__name__)


class OffsetWatchdog:
    DEFAULT_BACKEND = "memory"

    def __init__(self, config: dict) -> None:
        backend_name = config.get("backend", self.DEFAULT_BACKEND)
        backend_config = config.get("backend_config")
        self.config = backend_config

        logger.debug(
            "Using offset watchdog backend", backend=backend_name, config=self.config
        )
        backend_class = BACKENDS.get(backend_name, BACKENDS[self.DEFAULT_BACKEND])
        self.backend = backend_class(config=self.config)

    def seen(self, message: Message) -> bool:
        seen = self.backend.seen(message)
        if seen:
            logger.warning(
                "Message already seen previously", message_meta=message._meta
            )
        return seen

    def set_seen(self, message: Message):
        """Marks the message as already seen"""
        self.backend.set_seen(message)
