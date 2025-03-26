from typing import Any

import structlog

from flowgate.services.kafka.avro.message import Message

from flowgate.handler import Handler
from flowgate.utils import get_callable_representation

logger = structlog.get_logger(__name__)


class CommandHandler(Handler):
    def _can_handle_command(self, message: Message) -> bool:
        command_class = message.value["class"]
        if command_class not in self.handlers:
            logger.debug("Unhandled command", command_class=command_class)
            return False

        return True

    def _handle_command(self, command: Any, handler_inst: Any = None) -> None:
        command_class = command._class
        handler = self.handlers[command_class]

        logger.info("Calling command handler", command_class=command_class)
        if handler_inst:
            handler(handler_inst, command)
        else:
            handler(command)

    def handle(self, message: dict) -> None:
        if not self._can_handle_command(message):
            return

        command = self.message_deserializer(message)
        logger.info("Handling command", command_class=command._class)

        command_class = command._class
        handler = self.handlers[command_class]
        handler_name = get_callable_representation(handler)
        logger.debug("Calling command handler", handler=handler_name)

        self._handle_command(command)
