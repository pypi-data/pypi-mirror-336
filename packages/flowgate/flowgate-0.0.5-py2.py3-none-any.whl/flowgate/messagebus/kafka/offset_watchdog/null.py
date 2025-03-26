from flowgate.services.kafka.avro.message import Message

from flowgate.messagebus.kafka.offset_watchdog.base import (
    OffsetWatchdogBackend,
)


class NullOffsetWatchdogBackend(OffsetWatchdogBackend):

    def seen(self, message: Message) -> bool:
        return False

    def set_seen(self, message: Message):
        pass
