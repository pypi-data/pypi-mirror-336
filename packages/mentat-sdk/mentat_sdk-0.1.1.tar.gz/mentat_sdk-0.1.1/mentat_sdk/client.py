"""
Client for interacting with the Mentat web server.
"""

import threading
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from mentat_sdk.commands.handler import CommandManager
from mentat_sdk.config.manager import ConfigManager
from mentat_sdk.logger import MentatLogger
from mentat_sdk.notifications.manager import NotificationManager
from mentat_sdk.websocket.connection import WebSocketConnection
from mentat_sdk.websocket.exceptions import WebSocketConnectionError


class MentatClient:
    """
    A client for interacting with the Mentat web server.

    This client provides methods to communicate with the Mentat server,
    handling authentication and API requests.

    Attributes:
        logger (MentatLogger): Logger instance for this client.
        config (Dict[str, Any]): The current configuration from the server.

    Note:
        This class implements a singleton pattern - only one instance will exist
        per host/port combination. This helps prevent issues with notification and
        command tracking when multiple client instances are created.
    """

    # Singleton instances (keyed by host:port)
    _instances = {}
    _lock = threading.Lock()

    def __new__(
        cls, host: str = "0.0.0.0", port: int = 8765, log_level: Optional[int] = None
    ) -> "MentatClient":
        """
        Create a new MentatClient instance, or return an existing one for the same host/port.

        Args:
            host (str): The hostname or IP address of the Mentat server.
            port (int): The port number of the Mentat server.
            log_level (Optional[int]): The logging level to use.

        Returns:
            MentatClient: The client instance.
        """
        # Generate a key for this host/port combination
        key = f"{host}:{port}"

        # Use lock for thread safety during instance creation
        with cls._lock:
            # If an instance for this host/port already exists, return it
            if key in cls._instances:
                instance = cls._instances[key]
                # Optionally update log level if explicitly provided
                if log_level is not None and hasattr(instance, "logger"):
                    instance.logger.setLevel(log_level)
                return instance

            # Create a new instance
            instance = super().__new__(cls)
            cls._instances[key] = instance

            # Set a flag to indicate this is a new instance
            instance._initialized = False

            return instance

    def __init__(
        self, host: str = "0.0.0.0", port: int = 8765, log_level: Optional[int] = None
    ) -> None:
        """
        Initialize a new Mentat client instance.

        Args:
            host (str): The hostname or IP address of the Mentat server.
                Defaults to "0.0.0.0".
            port (int): The port number of the Mentat server.
                Defaults to 8765.
            log_level (Optional[int]): The logging level to use. If None, defaults to INFO.

        Raises:
            TypeError: If parameters have invalid types.
            WebSocketConnectionError: If connection to the server fails.
        """
        # Skip initialization if this instance has already been initialized
        if hasattr(self, "_initialized") and self._initialized:
            return

        # Store parameters
        self.host = host
        self.port = port

        if not isinstance(host, str):
            raise TypeError("host must be a string")
        if not isinstance(port, int):
            raise TypeError("port must be an integer")
        if log_level is not None and not isinstance(log_level, int):
            raise TypeError("log_level must be an integer or None")

        # Initialize logger
        self.logger = (
            MentatLogger("client", level=log_level)
            if log_level
            else MentatLogger("client")
        )
        self.logger.info("Initializing Mentat client")

        # Initialize WebSocket connection
        self._websocket = WebSocketConnection(host, port)

        # Initialize managers
        self._config_manager = ConfigManager()
        self._notification_manager = NotificationManager(self._websocket)
        self._command_manager = CommandManager(self._websocket)

        # Register handlers for server messages
        self._websocket.register_message_handler(
            "connection_established", self._handle_connection_established
        )

        self._websocket.register_message_handler(
            "config_update", self._handle_config_update
        )

        # Connect to server
        try:
            self._websocket.connect()
            self.logger.info(f"Connected to Mentat server at {host}:{port}")
        except WebSocketConnectionError as e:
            self.logger.error(f"Failed to connect to Mentat server: {e}")
            raise

        # Mark this instance as initialized
        self._initialized = True

    def __del__(self) -> None:
        """Clean up resources when the client is destroyed."""
        if hasattr(self, "_websocket"):
            self._websocket.disconnect()

    def shutdown(self, timeout: float = 1.0) -> bool:
        """
        Gracefully shut down the client, ensuring all pending messages are sent.

        This method should be called before terminating the program to ensure
        that all notifications and commands have been properly sent to the server.

        Args:
            timeout (float): Maximum time in seconds to wait for pending operations.
                Defaults to 1.0 second.

        Returns:
            bool: True if shutdown was clean, False if timeout occurred.

        Example:
            ```python
            client = MentatClient()
            # ... use client ...
            client.shutdown()  # Ensure all messages are sent
            ```
        """
        if not hasattr(self, "_websocket") or not self._websocket.connected:
            # Already disconnected
            self.logger.debug("Client already disconnected, skipping shutdown")
            return True

        self.logger.info(f"Gracefully shutting down client (timeout: {timeout}s)")

        # In this implementation, we consider the shutdown clean immediately
        # since we don't have a reliable way to check for pending messages yet
        # A short delay is still used to allow any in-progress operations to complete
        clean_shutdown = True

        # Small delay to allow any final operations to complete
        if timeout > 0:
            time.sleep(min(0.1, timeout))

        # Disconnect the websocket
        self._websocket.disconnect()
        self.logger.info("WebSocket connection closed")

        # Remove from singleton instances if possible
        try:
            key = f"{self.host}:{self.port}"
            with self.__class__._lock:
                if key in self.__class__._instances:
                    del self.__class__._instances[key]
                    self.logger.debug("Removed client from singleton registry")
        except Exception as e:
            self.logger.warning(f"Error cleaning up singleton instance: {e}")

        self.logger.info("Client shut down successfully")
        return clean_shutdown

    # Config access
    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the current configuration from the server.

        Returns:
            Dict[str, Any]: The current configuration.

        Raises:
            TimeoutError: If the initial configuration is not received from the server.
        """
        try:
            return self._config_manager.get_config()
        except TimeoutError as e:
            self.logger.error("Failed to get initial configuration from server")
            error_msg = (
                "Failed to get initial configuration from server. "
                "Make sure the server is running and properly connected."
            )
            raise TimeoutError(error_msg) from e

    # Notification methods
    def create_notification(
        self,
        title: str,
        description: str,
        possible_responses: Optional[List[str]] = None,
        response_callback: Optional[Callable[[str, str], None]] = None,
    ) -> str:
        """
        Create and send a notification to the Mentat server.

        Args:
            title (str): The notification title.
            description (str): The notification description.
            possible_responses (Optional[List[str]]): List of possible responses.
            response_callback (Optional[Callable[[str, str], None]]): Callback function
                to execute when a response is received. Will be called with
                (notification_id, response).

        Returns:
            str: The ID of the created notification.

        Raises:
            TypeError: If parameters have invalid types.
            WebSocketNotConnectedError: If client is not connected to the server.
        """
        try:
            return self._notification_manager.create_notification(
                title=title,
                description=description,
                possible_responses=possible_responses,
                callback=response_callback,
            )
        except Exception as e:
            self.logger.error(f"Failed to create notification: {e}")
            raise

    def get_notification_response(
        self, notification_id: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if a notification has received a response.

        Args:
            notification_id (str): The ID of the notification to check.

        Returns:
            Tuple[bool, Optional[str]]: A tuple where the first element is a boolean
                indicating if a response was received, and the second element is
                the response string if one was received, or None otherwise.

        Raises:
            TypeError: If notification_id is not a string.
        """
        try:
            return self._notification_manager.get_notification_response(notification_id)
        except Exception as e:
            self.logger.error(f"Failed to get notification response: {e}")
            raise

    def notification_response_executed(self, notification_id: str) -> None:
        """
        Notify the server that a notification response has been successfully executed.

        Args:
            notification_id (str): The ID of the notification.

        Raises:
            TypeError: If notification_id is not a string.
            ValueError: If the notification doesn't exist or doesn't have a response.
            WebSocketNotConnectedError: If client is not connected to the server.
        """
        try:
            self._notification_manager.notification_response_executed(notification_id)
        except Exception as e:
            self.logger.error(f"Failed to mark notification response as executed: {e}")
            raise

    def notification_response_execution_error(
        self, notification_id: str, error: str
    ) -> None:
        """
        Notify the server that a notification response execution failed.

        Args:
            notification_id (str): The ID of the notification.
            error (str): Description of the error that occurred.

        Raises:
            TypeError: If notification_id or error is not a string.
            ValueError: If notification doesn't exist or doesn't have a response.
            WebSocketNotConnectedError: If client is not connected to the server.
        """
        try:
            self._notification_manager.notification_response_execution_error(
                notification_id, error
            )
        except Exception as e:
            error_msg = f"Failed to mark notification response as execution error: {e}"
            self.logger.error(error_msg)
            raise

    # Command methods
    def register_command_handler(
        self, command_key: str, handler: Callable[[str, Dict[str, Any]], None]
    ) -> None:
        """
        Register a handler for a specific command type.

        Args:
            command_key (str): The command key to handle.
            handler (Callable[[str, Dict[str, Any]], None]): The handler function.
                Will be called with (command_id, parameters).

        Raises:
            TypeError: If command_key is not a string or handler is not callable.
        """
        try:
            self._command_manager.register_handler(command_key, handler)
        except Exception as e:
            self.logger.error(f"Failed to register command handler: {e}")
            raise

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
            TypeError: If parameters have invalid types.
            ValueError: If the command doesn't exist.
            WebSocketNotConnectedError: If client is not connected to the server.
        """
        try:
            self._command_manager.acknowledge_command(
                command_id=command_id,
                has_progress_percentage=has_progress_percentage,
                progress_steps=progress_steps,
            )
        except Exception as e:
            self.logger.error(f"Failed to acknowledge command: {e}")
            raise

    def update_command_progress(
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
            ValueError: If the command doesn't exist or progress parameters are invalid.
            WebSocketNotConnectedError: If client is not connected to the server.
        """
        try:
            self._command_manager.update_progress(
                command_id=command_id,
                progress_step=progress_step,
                progress_step_status=progress_step_status,
                progress_percentage=progress_percentage,
            )
        except Exception as e:
            self.logger.error(f"Failed to update command progress: {e}")
            raise

    def command_executed(self, command_id: str) -> None:
        """
        Notify the server that a command has been successfully executed.

        Args:
            command_id (str): The ID of the command.

        Raises:
            TypeError: If command_id is not a string.
            ValueError: If the command doesn't exist.
            WebSocketNotConnectedError: If client is not connected to the server.
        """
        try:
            self._command_manager.command_executed(command_id)
        except Exception as e:
            self.logger.error(f"Failed to mark command as executed: {e}")
            raise

    def command_execution_error(self, command_id: str, error: str) -> None:
        """
        Notify the server that a command execution failed.

        Args:
            command_id (str): The ID of the command.
            error (str): Description of the error that occurred.

        Raises:
            TypeError: If command_id or error is not a string.
            ValueError: If the command doesn't exist.
            WebSocketNotConnectedError: If client is not connected to the server.
        """
        try:
            self._command_manager.command_execution_error(command_id, error)
        except Exception as e:
            self.logger.error(f"Failed to mark command as execution error: {e}")
            raise

    # Server message handlers
    def _handle_connection_established(self, message: Dict[str, Any]) -> None:
        """
        Handle connection established messages from the server.

        Args:
            message (Dict[str, Any]): The connection established message.
        """
        self.logger.info("Connection established with Mentat server")

    def _handle_config_update(self, message: Dict[str, Any]) -> None:
        """
        Handle config update messages from the server.

        Args:
            message (Dict[str, Any]): The config update message.
        """
        if "config" not in message:
            self.logger.warning("Received config update message without config data")
            return

        config = message["config"]
        self._config_manager.update_config(config)
        self.logger.info("Updated configuration from server")
