"""
WebSocket connection handler for the Mentat SDK.

This module handles the WebSocket connection to the Mentat server, including
connection management, message sending, and message receiving.
"""

import json
import logging
import threading
import time
from typing import Any, Callable, Dict, Optional

import websocket

from mentat_sdk.websocket.exceptions import (WebSocketConnectionError,
                                             WebSocketMessageError,
                                             WebSocketNotConnectedError)
from mentat_sdk.websocket.message_parser import format_message, parse_message

logger = logging.getLogger(__name__)


class WebSocketConnection:
    """
    Manages the WebSocket connection to the Mentat server.

    This class handles establishing and maintaining the connection,
    sending and receiving messages, and routing incoming messages
    to the appropriate handlers.
    """

    def __init__(self, host: str, port: int):
        """
        Initialize a new WebSocket connection handler.

        Args:
            host (str): The host to connect to.
            port (int): The port to connect to.

        Raises:
            TypeError: If host is not a string or port is not an integer.
        """
        if not isinstance(host, str):
            raise TypeError("host must be a string")
        if not isinstance(port, int):
            raise TypeError("port must be an integer")

        self.host = host
        self.port = port
        self.ws = None
        self.connected = False
        self.message_handlers = {}
        self._receiver_thread = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> None:
        """
        Establish the WebSocket connection to the server.

        Raises:
            WebSocketConnectionError: If the connection fails.
        """
        url = f"ws://{self.host}:{self.port}"

        try:
            # Create and connect the WebSocket
            self.ws = websocket.WebSocket()
            self.ws.connect(url)
            self.connected = True

            # Start the receiver thread
            self._receiver_thread = threading.Thread(
                target=self._message_receiver, daemon=True
            )
            self._receiver_thread.start()

            logger.info(f"Connected to Mentat server at {url}")
        except Exception as e:
            self.connected = False
            error_msg = f"Failed to connect to Mentat server at {url}: {e}"
            logger.error(error_msg)
            raise WebSocketConnectionError(error_msg) from e

    def disconnect(self) -> None:
        """
        Disconnect from the WebSocket server.
        """
        if self.ws and self.connected:
            try:
                self.ws.close()
                logger.info("Disconnected from Mentat server")
            except Exception as e:
                logger.error(f"Error during disconnection: {e}")
            finally:
                self.connected = False
                self.ws = None

    def send_message(self, message: Dict[str, Any]) -> None:
        """
        Send a message to the Mentat server.

        Args:
            message (Dict[str, Any]): The message to send.

        Raises:
            WebSocketNotConnectedError: If the WebSocket is not connected.
            WebSocketMessageError: If there's an error sending the message.
        """
        if not self.connected or not self.ws:
            error_msg = "Cannot send message: WebSocket is not connected"
            logger.error(error_msg)
            raise WebSocketNotConnectedError(error_msg)

        try:
            message_json = json.dumps(message)
            self.ws.send(message_json)
            logger.debug(f"Sent message: {message}")
        except Exception as e:
            error_msg = f"Failed to send message: {e}"
            logger.error(error_msg)
            raise WebSocketMessageError(error_msg) from e

    def register_message_handler(
        self, message_type: str, handler: Callable[[Dict[str, Any]], None]
    ) -> None:
        """
        Register a handler for a specific message type.

        Args:
            message_type (str): The message type to handle.
            handler (Callable[[Dict[str, Any]], None]): The handler function.

        Raises:
            TypeError: If message_type is not a string or handler is not callable.
        """
        if not isinstance(message_type, str):
            raise TypeError("message_type must be a string")
        if not callable(handler):
            raise TypeError("handler must be callable")

        self.message_handlers[message_type] = handler
        logger.debug(f"Registered handler for message type: {message_type}")

    def _message_receiver(self) -> None:
        """
        Background thread that receives and processes messages from the server.
        """
        while self.connected and self.ws:
            try:
                # Receive message
                raw_message = self.ws.recv()
                if not raw_message:
                    continue

                # Parse message
                message = parse_message(raw_message)
                message_type = message.get("type")

                logger.debug(f"Received message: {message}")

                # Route to appropriate handler
                handler = self.message_handlers.get(message_type)
                if handler:
                    try:
                        handler(message)
                    except Exception as e:
                        logger.error(
                            f"Error in message handler for type {message_type}: {e}"
                        )
                else:
                    logger.warning(
                        f"No handler registered for message type: {message_type}"
                    )

            except websocket.WebSocketConnectionClosedException:
                logger.warning("WebSocket connection closed by server")
                self.connected = False
                break
            except Exception as e:
                logger.error(f"Error in message receiver: {e}")
                time.sleep(0.1)  # Avoid high CPU usage on repeated errors
