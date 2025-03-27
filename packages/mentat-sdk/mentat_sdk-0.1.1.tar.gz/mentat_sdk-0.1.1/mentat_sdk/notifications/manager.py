"""
Notification manager for the Mentat SDK.

This module handles the creation, tracking, and response handling
for notifications in the Mentat system.
"""

import logging
import threading
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

from mentat_sdk.notifications.model import Notification
from mentat_sdk.utils.uuid_generator import generate_notification_id
from mentat_sdk.websocket.connection import WebSocketConnection
from mentat_sdk.websocket.exceptions import WebSocketNotConnectedError
from mentat_sdk.websocket.message_parser import format_message

logger = logging.getLogger(__name__)

# Type definitions
NotificationCallback = Callable[[str, str], None]  # notification_id, response


class NotificationManager:
    """
    Manages notifications for the Mentat SDK.

    This class handles creating notifications, tracking responses,
    and executing callbacks when responses are received.
    """

    def __init__(self, websocket_connection: WebSocketConnection):
        """
        Initialize a new notification manager.

        Args:
            websocket_connection (WebSocketConnection): The WebSocket connection
                to use for sending notifications and receiving responses.
        """
        if not isinstance(websocket_connection, WebSocketConnection):
            raise TypeError("websocket_connection must be a WebSocketConnection")

        self._websocket = websocket_connection
        self._notifications: Dict[str, Notification] = {}
        self._responses: Dict[str, str] = {}
        self._callbacks: Dict[str, NotificationCallback] = {}
        self._lock = threading.RLock()  # Add a lock for thread safety

        # Register for notification response messages
        self._websocket.register_message_handler(
            "notification_response", self._handle_notification_response
        )

    def create_notification(
        self,
        title: str,
        description: str,
        possible_responses: Optional[List[str]] = None,
        callback: Optional[NotificationCallback] = None,
    ) -> str:
        """
        Create and send a new notification.

        Args:
            title (str): The notification title.
            description (str): The notification description.
            possible_responses (Optional[List[str]]): List of possible responses.
            callback (Optional[Callable[[str, str], None]]): Callback function
                to execute when a response is received.

        Returns:
            str: The ID of the created notification.

        Raises:
            TypeError: If parameters have invalid types.
            WebSocketNotConnectedError: If the WebSocket is not connected.
        """
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        if possible_responses is not None and not isinstance(possible_responses, list):
            raise TypeError("possible_responses must be a list or None")
        if callback is not None and not callable(callback):
            raise TypeError("callback must be callable or None")

        # Generate notification ID
        notification_id = generate_notification_id()

        # Convert possible_responses list to indexed dict if provided
        response_dict = None
        if possible_responses:
            response_dict = {str(i): resp for i, resp in enumerate(possible_responses)}

        # Create notification object
        notification = Notification(
            notification_id=notification_id,
            title=title,
            description=description,
            possible_responses=response_dict,
        )

        # Store notification and callback
        with self._lock:
            self._notifications[notification_id] = notification
            if callback:
                self._callbacks[notification_id] = callback

        # Prepare message for sending
        payload = {"type": "create_notification", **notification.to_dict()}

        message = format_message("create_notification", notification.to_dict())

        # Send notification
        try:
            self._websocket.send_message(message)
            logger.debug(f"Sent notification: {notification_id}")
        except WebSocketNotConnectedError:
            # Clean up stored data if send fails
            with self._lock:
                if notification_id in self._notifications:
                    del self._notifications[notification_id]
                if notification_id in self._callbacks:
                    del self._callbacks[notification_id]
            raise

        return notification_id

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
        if not isinstance(notification_id, str):
            raise TypeError("notification_id must be a string")

        with self._lock:
            has_response = notification_id in self._responses
            response = self._responses.get(notification_id)

        return (has_response, response)

    def notification_response_executed(self, notification_id: str) -> None:
        """
        Notify the server that a notification response has been successfully executed.

        Args:
            notification_id (str): The ID of the notification.

        Raises:
            TypeError: If notification_id is not a string.
            ValueError: If the notification doesn't exist or doesn't have a response.
            WebSocketNotConnectedError: If the WebSocket is not connected.
        """
        if not isinstance(notification_id, str):
            raise TypeError("notification_id must be a string")

        with self._lock:
            if notification_id not in self._notifications:
                raise ValueError(f"Notification {notification_id} doesn't exist")

            if notification_id not in self._responses:
                raise ValueError(
                    f"Notification {notification_id} doesn't have a response"
                )

        # Prepare message
        payload = {
            "notification_id": notification_id,
            "status": "executed",
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

        message = format_message("notification_response_executed", payload)

        # Send message
        self._websocket.send_message(message)
        logger.debug(f"Sent notification response executed: {notification_id}")

        # Clean up
        self._cleanup_notification(notification_id)

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
            ValueError: If the notification doesn't exist or doesn't have a response.
            WebSocketNotConnectedError: If the WebSocket is not connected.
        """
        if not isinstance(notification_id, str):
            raise TypeError("notification_id must be a string")
        if not isinstance(error, str):
            raise TypeError("error must be a string")

        with self._lock:
            if notification_id not in self._notifications:
                raise ValueError(f"Notification {notification_id} doesn't exist")

            if notification_id not in self._responses:
                raise ValueError(
                    f"Notification {notification_id} doesn't have a response"
                )

        # Prepare message
        payload = {
            "notification_id": notification_id,
            "status": "executed_error",
            "error": error,
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }

        message = format_message("notification_response_executed_error", payload)

        # Send message
        self._websocket.send_message(message)
        logger.debug(f"Sent notification response execution error: {notification_id}")

        # Clean up
        self._cleanup_notification(notification_id)

    def _handle_notification_response(self, message: Dict[str, Any]) -> None:
        """
        Handle notification response messages from the server.

        Args:
            message (Dict[str, Any]): The notification response message.
        """
        notification_id = message.get("notification_id")
        response = message.get("response")

        if not notification_id or not response:
            logger.warning(f"Received invalid notification response: {message}")
            return

        with self._lock:
            if notification_id not in self._notifications:
                logger.warning(
                    f"Received response for unknown notification: {notification_id}"
                )
                return

        logger.debug(
            f"Received response for notification {notification_id}: {response}"
        )

        # Store the response
        with self._lock:
            self._responses[notification_id] = response

            # Update the notification object
            notification = self._notifications[notification_id]
            notification.set_response(response)

            # Get the callback if registered
            callback = self._callbacks.get(notification_id)

        # Send acknowledgment to server
        ack_payload = {
            "notification_id": notification_id,
            "status": "acknowledged",
            "acknowledged_at": datetime.now(timezone.utc).isoformat(),
        }

        ack_message = format_message("notification_response_acknowledged", ack_payload)
        self._websocket.send_message(ack_message)
        logger.debug(f"Sent notification response acknowledgment: {notification_id}")

        # Execute callback if registered
        if callback:
            try:
                # Execute the callback in a new thread to avoid blocking
                logger.debug(
                    f"Starting thread for notification callback execution: {notification_id}"
                )
                thread = threading.Thread(
                    target=self._execute_callback,
                    args=(callback, notification_id, response),
                    daemon=True,
                )
                thread.start()
            except Exception as e:
                logger.error(
                    f"Error executing callback for notification {notification_id}: {e}"
                )

    def _execute_callback(
        self, callback: NotificationCallback, notification_id: str, response: str
    ) -> None:
        """
        Execute a notification response callback in a thread.

        Args:
            callback (NotificationCallback): The callback function.
            notification_id (str): The notification ID.
            response (str): The selected response.
        """
        logger.debug(
            f"Executing notification callback in thread for: {notification_id}"
        )
        try:
            callback(notification_id, response)
        except Exception as e:
            logger.error(f"Error in notification callback: {e}", exc_info=True)

    def _cleanup_notification(self, notification_id: str) -> None:
        """
        Clean up stored data for a notification after it's complete.

        Args:
            notification_id (str): The ID of the notification to clean up.
        """
        with self._lock:
            if notification_id in self._notifications:
                del self._notifications[notification_id]
            if notification_id in self._responses:
                del self._responses[notification_id]
            if notification_id in self._callbacks:
                del self._callbacks[notification_id]
