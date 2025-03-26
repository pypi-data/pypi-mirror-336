from typing import Any

import structlog

from flowgate.services.kafka.avro.message import Message

from flowgate.handler import Handler
from flowgate.utils import get_callable_representation

logger = structlog.get_logger(__name__)


class EventHandler(Handler):
    def _can_handle_command(self, message: Message) -> bool:
        event_class = message.value["class"]
        if event_class not in self.handlers:
            logger.debug("Unhandled event", event_class=event_class)
            return False

        return True

    def _handle_event(self, event: Any) -> None:
        handler = self.handlers[event._class]
        handler_name = get_callable_representation(handler)
        logger.debug("Calling event handler", handler=handler_name)

        handler(event)

    def handle(self, message: dict) -> None:
        if not self._can_handle_command(message):
            return

        event = self.message_deserializer(message)
        logger.info("Handling event", event_class=event._class)

        self._handle_event(event)
