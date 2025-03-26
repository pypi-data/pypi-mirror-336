import structlog
from redis import StrictRedis
from redis.sentinel import Sentinel

from flowgate.services.kafka.avro.message import Message

from flowgate.messagebus.kafka.offset_watchdog.base import (
    OffsetWatchdogBackend,
)

logger = structlog.get_logger(__name__)

__all__ = ["RedisOffsetWatchdogBackend"]


class RedisOffsetWatchdogBackend(OffsetWatchdogBackend):

    DEFAULT_CONFIG = {
        "url": None,
        "sentinel": None,
        "sentinel_master": "mymaster",
        "db": 0,
        "prefix": "offset_watchdog",
    }

    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self._redis = None
        self._config = {**self.DEFAULT_CONFIG, **config}
        self._prefix = self._config["prefix"]

    @property
    def redis(self) -> StrictRedis:
        if self._redis is None:
            if self._config["sentinel"]:
                sentinel = Sentinel(
                    self._config["sentinel"], socket_timeout=0.1, db=self._config["db"]
                )
                self._redis = sentinel.master_for(self._config["sentinel_master"])
            else:
                self._redis = StrictRedis.from_url(
                    self._config["url"], db=self._config["db"]
                )
        return self._redis

    def seen(self, message: Message) -> bool:
        key = f"{self._prefix}:{self._key(message)}"
        try:
            last_offset = self.redis.get(key)
            if last_offset is None:
                return False
            return message._meta.offset <= int(last_offset)
        except Exception:
            logger.exception("Failed to check offset")
            return False

    def set_seen(self, message: Message):
        key = f"{self._prefix}:{self._key(message)}"
        try:
            self.redis.set(key, message._meta.offset)
        except Exception:
            logger.exception("Failed to set offset")
