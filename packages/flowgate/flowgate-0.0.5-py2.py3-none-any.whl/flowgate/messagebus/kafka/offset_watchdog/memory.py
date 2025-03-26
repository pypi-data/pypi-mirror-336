from flowgate.services.kafka.avro.message import Message

from flowgate.messagebus.kafka.offset_watchdog.base import (
    OffsetWatchdogBackend,
)


class InMemoryOffsetWatchdogBackend(OffsetWatchdogBackend):

    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self._offset_map: dict = {}

    def seen(self, message: Message) -> bool:
        last_offset = self._offset_map.get(self._key(message), -1)
        return message._meta.offset <= last_offset

    def set_seen(self, message: Message):
        self._offset_map[self._key(message)] = message._meta.offset
