from copy import deepcopy
from unittest.mock import Mock, patch

import pytest

from flowgate.command_handler import CommandHandler

module = "flowgate.command_handler"

command_class, id = "FooCommand", "1"
message = Mock(value={"class": command_class, "data": {"id": id}})
events = [1, 2, 3]

command = Mock()
command._class = command_class
command.id = id


class CommandHandlerTests:
    def setup_method(self):
        self.mock_handler = Mock()

        command_handler = CommandHandler
        command_handler.handlers = {command_class: self.mock_handler}

        self.message_deserializer = Mock()
        self.message_deserializer.return_value = command

        self.handler = command_handler(message_deserializer=self.message_deserializer)

    @patch(f"{module}.CommandHandler._handle_command")
    @patch(f"{module}.CommandHandler._can_handle_command")
    def test_handle(self, mock_can_handle, mock_handle):
        """
        Test that the correct methods are invoked when handling a command.
        """
        mock_can_handle.return_value = True
        self.handler.handle(message)

        self.message_deserializer.assert_called_once_with(message)
        mock_can_handle.assert_called_once_with(message)
        mock_handle.assert_called_once_with(command)

    def test_can_handle_command(self):
        """
        Test that we only handle registered commands.
        """
        can_handle = self.handler._can_handle_command(message)
        assert can_handle is True

        _message = deepcopy(message)
        _message.value["class"] = "BarCommand"
        can_handle = self.handler._can_handle_command(_message)
        assert can_handle is False

    def test_handle_command(self):
        """
        Test that the correct command handler is invoked.
        """
        self.handler._handle_command(command)
        self.mock_handler.assert_called_once_with(command)
