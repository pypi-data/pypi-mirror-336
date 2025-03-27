"""
Message parser for WebSocket communication.

This module handles the parsing and validation of messages exchanged with
the Mentat server over WebSocket connections.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from mentat_sdk.websocket.exceptions import WebSocketMessageError

logger = logging.getLogger(__name__)


def parse_message(raw_message: str) -> Dict[str, Any]:
    """
    Parse a raw message string into a structured message dictionary.

    Args:
        raw_message (str): The raw message string received from the WebSocket.

    Returns:
        Dict[str, Any]: The parsed message as a dictionary.

    Raises:
        WebSocketMessageError: If the message cannot be parsed or is invalid.
    """
    try:
        message = json.loads(raw_message)
        if not isinstance(message, dict):
            raise WebSocketMessageError("Message must be a JSON object")

        # Check for required fields
        if "type" not in message:
            raise WebSocketMessageError("Message missing required field: type")

        return message
    except json.JSONDecodeError as e:
        error_msg = f"Failed to parse WebSocket message: {e}"
        logger.error(error_msg)
        raise WebSocketMessageError(error_msg) from e


def format_message(message_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a message for sending to the server.

    Args:
        message_type (str): The type of message being sent.
        payload (Dict[str, Any]): The message payload.

    Returns:
        Dict[str, Any]: The formatted message with metadata.
    """
    # Create basic message structure
    message = {"type": message_type, **payload}

    # Add timestamp if not provided
    if "timestamp" not in message and "created_at" not in message:
        message["timestamp"] = datetime.now(timezone.utc).isoformat()

    return message
