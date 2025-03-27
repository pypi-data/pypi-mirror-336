"""
Command handler for the Mentat SDK.

This module handles the receiving, acknowledging, and tracking
of commands from the Mentat server.
"""

import logging
import threading
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from mentat_sdk.commands.model import Command
from mentat_sdk.websocket.connection import WebSocketConnection
from mentat_sdk.websocket.exceptions import WebSocketNotConnectedError
from mentat_sdk.websocket.message_parser import format_message

logger = logging.getLogger(__name__)

# Type definitions
CommandHandler = Callable[[str, Dict[str, Any]], None]  # command_id, parameters


class CommandManager:
    """
    Manages commands for the Mentat SDK.

    This class handles receiving commands from the server,
    executing registered handlers, and tracking command progress.
    """

    def __init__(self, websocket_connection: WebSocketConnection):
        """
        Initialize a new command manager.

        Args:
            websocket_connection (WebSocketConnection): The WebSocket connection
                to use for receiving commands and sending updates.
        """
        if not isinstance(websocket_connection, WebSocketConnection):
            raise TypeError("websocket_connection must be a WebSocketConnection")

        self._websocket = websocket_connection
        self._command_handlers: Dict[str, CommandHandler] = {}
        self._active_commands: Dict[str, Command] = {}
        self._lock = threading.RLock()  # Add a lock for thread safety

        # Register for command messages
        self._websocket.register_message_handler("create_command", self._handle_command)

    def register_handler(self, command_key: str, handler: CommandHandler) -> None:
        """
        Register a handler for a specific command type.

        Args:
            command_key (str): The command key to handle.
            handler (Callable[[str, Dict[str, Any]], None]): The handler function.
                Will be called with (command_id, parameters).

        Raises:
            TypeError: If command_key is not a string or handler is not callable.
        """
        if not isinstance(command_key, str):
            raise TypeError("command_key must be a string")
        if not callable(handler):
            raise TypeError("handler must be callable")

        with self._lock:
            self._command_handlers[command_key] = handler
        logger.debug(f"Registered handler for command key: {command_key}")

    def acknowledge_command(
        self,
        command_id: str,
        has_progress_percentage: bool = False,
        progress_steps: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Acknowledge receipt of a command and prepare for progress tracking.

        Args:
            command_id (str): The ID of the command to acknowledge.
            has_progress_percentage (bool): Whether to track progress percentage.
            progress_steps (Optional[Dict[str, str]]): Dictionary mapping step indices
                to step descriptions.

        Raises:
            TypeError: If command_id is not a string.
            ValueError: If the command doesn't exist.
            WebSocketNotConnectedError: If the WebSocket is not connected.
        """
        if not isinstance(command_id, str):
            raise TypeError("command_id must be a string")

        with self._lock:
            if command_id not in self._active_commands:
                raise ValueError(f"Command {command_id} doesn't exist")

            # Update command
            command = self._active_commands[command_id]
            command.acknowledge(
                has_progress_percentage=has_progress_percentage,
                progress_steps=progress_steps,
            )

        # Prepare message
        payload = {
            "command_id": command_id,
            "status": "acknowledged",
            "acknowledged_at": datetime.now(timezone.utc).isoformat(),
            "has_progress_percentage": has_progress_percentage,
        }

        if progress_steps:
            payload["progress_steps"] = progress_steps

        message = format_message("command_acknowledged", payload)

        # Send message
        self._websocket.send_message(message)
        logger.debug(f"Sent command acknowledgment: {command_id}")

    def update_progress(
        self,
        command_id: str,
        progress_step: str,
        progress_step_status: str,
        progress_percentage: Optional[int] = None,
    ) -> None:
        """
        Update the progress of a command.

        Args:
            command_id (str): The ID of the command to update.
            progress_step (str): The current progress step.
            progress_step_status (str): Status of the current step
                (started, completed, failed).
            progress_percentage (Optional[int]): Current progress percentage.

        Raises:
            TypeError: If parameters have invalid types.
            ValueError: If the command doesn't exist.
            ValueError: If progress parameters are invalid.
            WebSocketNotConnectedError: If the WebSocket is not connected.
        """
        if not isinstance(command_id, str):
            raise TypeError("command_id must be a string")
        if not isinstance(progress_step, str):
            raise TypeError("progress_step must be a string")
        if not isinstance(progress_step_status, str):
            raise TypeError("progress_step_status must be a string")
        if progress_percentage is not None and not isinstance(progress_percentage, int):
            raise TypeError("progress_percentage must be an integer or None")

        milestone = None
        with self._lock:
            if command_id not in self._active_commands:
                raise ValueError(f"Command {command_id} doesn't exist")

            command = self._active_commands[command_id]

            # Update command progress
            milestone = command.update_progress(
                progress_step=progress_step,
                progress_step_status=progress_step_status,
                progress_percentage=progress_percentage,
            )

        # Prepare message
        status = "in_progress"
        if progress_step_status == "failed":
            status = "failed"

        payload = {
            "command_id": command_id,
            "status": status,
            "progress_milestone": milestone,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        if progress_step_status == "failed":
            payload["error"] = f"Failed at step '{progress_step}'"

        message = format_message("command_progress_update", payload)

        # Send message
        self._websocket.send_message(message)
        logger.debug(
            f"Sent command progress update: {command_id} - {progress_step} ({progress_step_status})"
        )

    def command_executed(self, command_id: str) -> None:
        """
        Notify the server that a command has been successfully executed.

        Args:
            command_id (str): The ID of the command.

        Raises:
            TypeError: If command_id is not a string.
            ValueError: If the command doesn't exist.
            WebSocketNotConnectedError: If the WebSocket is not connected.
        """
        if not isinstance(command_id, str):
            raise TypeError("command_id must be a string")

        with self._lock:
            if command_id not in self._active_commands:
                raise ValueError(f"Command {command_id} doesn't exist")

        # Prepare message
        payload = {
            "command_id": command_id,
            "status": "executed",
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

        message = format_message("command_executed", payload)

        # Send message
        self._websocket.send_message(message)
        logger.debug(f"Sent command executed: {command_id}")

        # Clean up
        self._cleanup_command(command_id)

    def command_execution_error(self, command_id: str, error: str) -> None:
        """
        Notify the server that a command execution failed.

        Args:
            command_id (str): The ID of the command.
            error (str): Description of the error that occurred.

        Raises:
            TypeError: If command_id or error is not a string.
            ValueError: If the command doesn't exist.
            WebSocketNotConnectedError: If the WebSocket is not connected.
        """
        if not isinstance(command_id, str):
            raise TypeError("command_id must be a string")
        if not isinstance(error, str):
            raise TypeError("error must be a string")

        with self._lock:
            if command_id not in self._active_commands:
                raise ValueError(f"Command {command_id} doesn't exist")

        # Prepare message
        payload = {
            "command_id": command_id,
            "status": "executed_error",
            "error": error,
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

        message = format_message("command_executed_error", payload)

        # Send message
        self._websocket.send_message(message)
        logger.debug(f"Sent command execution error: {command_id}")

        # Clean up
        self._cleanup_command(command_id)

    def _handle_command(self, message: Dict[str, Any]) -> None:
        """
        Handle command messages from the server.

        Args:
            message (Dict[str, Any]): The command message.
        """
        command_id = message.get("command_id")
        command_key = message.get("command_key")
        parameters = message.get("parameters", {})

        if not command_id or not command_key:
            logger.warning(f"Received invalid command message: {message}")
            return

        logger.debug(f"Received command: {command_id} ({command_key})")

        # Create command object
        command = Command(
            command_id=command_id, command_key=command_key, parameters=parameters
        )

        # Store command and get handler atomically
        handler = None
        with self._lock:
            self._active_commands[command_id] = command
            # Check if a handler is registered for this command type
            handler = self._command_handlers.get(command_key)

        # Execute handler if found
        if handler:
            # Execute handler in a thread
            try:
                logger.debug(
                    f"Starting thread for command handler execution: {command_id}"
                )
                thread = threading.Thread(
                    target=self._execute_handler,
                    args=(handler, command_id, parameters),
                    daemon=True,
                )
                thread.start()
            except Exception as e:
                logger.error(
                    f"Error starting command handler thread: {e}", exc_info=True
                )
        else:
            logger.warning(f"No handler registered for command key: {command_key}")

    def _execute_handler(
        self, handler: CommandHandler, command_id: str, parameters: Dict[str, Any]
    ) -> None:
        """
        Execute a command handler in a thread.

        Args:
            handler (CommandHandler): The handler function.
            command_id (str): The command ID.
            parameters (Dict[str, Any]): The command parameters.
        """
        logger.debug(f"Executing command handler in thread for: {command_id}")
        try:
            handler(command_id, parameters)
        except Exception as e:
            logger.error(f"Error in command handler: {e}", exc_info=True)
            # Report error to server
            try:
                self.command_execution_error(command_id, str(e))
            except Exception as report_error:
                logger.error(
                    f"Error reporting command error: {report_error}", exc_info=True
                )

    def _cleanup_command(self, command_id: str) -> None:
        """
        Clean up stored data for a command after it's complete.

        Args:
            command_id (str): The ID of the command to clean up.
        """
        with self._lock:
            if command_id in self._active_commands:
                del self._active_commands[command_id]
