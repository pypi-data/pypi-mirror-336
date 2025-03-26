from flowgate.services.kafka.avro.message import Message


class OffsetWatchdogBackend:

    def __init__(self, config: dict) -> None:
        self.config = config
        self.group_id = config.get("group.id", "default")

    def _key(self, message: Message) -> str:
        return f"{message._meta.topic}:{message._meta.partition}:{self.group_id}"

    def seen(self, message: Message) -> bool:
        raise NotImplementedError()

    def set_seen(self, message: Message):
        raise NotImplementedError()
