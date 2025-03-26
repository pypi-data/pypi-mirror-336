from typing import Callable

from flowgate.serializers import from_message_to_dto


class Handler:
    handlers: dict = {}

    def __init__(self, message_deserializer: Callable = from_message_to_dto) -> None:
        if not self.handlers:
            raise ValueError("No handlers defined for this Handler class")
        self.message_deserializer = message_deserializer

    def handle(self, message: dict) -> None:
        raise NotImplementedError(
            "You need to implement handle method in your subclass"
        )
