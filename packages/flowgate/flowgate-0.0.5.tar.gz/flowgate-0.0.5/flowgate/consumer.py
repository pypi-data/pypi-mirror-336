from flowgate.handler import Handler
from flowgate.messagebus.messagebus import MessageBus


class Consumer:
    def __init__(self, messagebus: MessageBus, handler: Handler) -> None:
        self._messagebus = messagebus
        self._handler = handler

    def consume(self) -> None:
        self._messagebus.consume(handler=self._handler.handle)
