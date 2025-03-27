"""
Notification data models for the Mentat SDK.

This module defines the data structures for notifications
created and managed by the Mentat SDK.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional


class Notification:
    """
    Represents a notification in the Mentat system.

    A notification is a message displayed to the user, potentially
    with response options that the user can select.
    """

    def __init__(
        self,
        notification_id: str,
        title: str,
        description: str,
        possible_responses: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize a new notification.

        Args:
            notification_id (str): Unique identifier for the notification.
            title (str): Title of the notification.
            description (str): Description of the notification.
            possible_responses (Optional[Dict[str, str]]): Possible responses
                indexed by position (e.g., {"0": "Accept", "1": "Reject"}).
        """
        self.notification_id = notification_id
        self.title = title
        self.description = description
        self.possible_responses = possible_responses
        self.response = None
        self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the notification to a dictionary for serialization.

        Returns:
            Dict[str, Any]: The notification as a dictionary.
        """
        notification_dict = {
            "notification_id": self.notification_id,
            "title": self.title,
            "description": self.description,
            "status": "pending",
            "created_at": self.created_at,
        }

        if self.possible_responses:
            notification_dict["potential_responses"] = self.possible_responses

        return notification_dict

    def set_response(self, response: str) -> None:
        """
        Set the response chosen by the user.

        Args:
            response (str): The selected response.
        """
        self.response = response
