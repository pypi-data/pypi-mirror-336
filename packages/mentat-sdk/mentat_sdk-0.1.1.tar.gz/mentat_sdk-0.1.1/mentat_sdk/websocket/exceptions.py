"""
WebSocket connection exceptions for Mentat SDK.
"""


class WebSocketConnectionError(Exception):
    """Exception raised when the WebSocket connection fails."""

    pass


class WebSocketMessageError(Exception):
    """Exception raised when there's an error sending or parsing a WebSocket message."""

    pass


class WebSocketNotConnectedError(Exception):
    """Exception raised when trying to send a message on a closed connection."""

    pass
