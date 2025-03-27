"""
UUID generation utilities for the Mentat SDK.
"""

import uuid
from typing import Any, Dict


def generate_uuid() -> str:
    """
    Generate a UUID v4 string.

    Returns:
        str: A UUID v4 string.
    """
    return str(uuid.uuid4())


def generate_notification_id() -> str:
    """
    Generate a notification ID.

    Returns:
        str: A UUID v4 string for use as a notification ID.
    """
    return generate_uuid()
