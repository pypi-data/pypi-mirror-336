"""
Mentat SDK - A Python client for interacting with the Mentat web server.

This package provides a client for connecting to a Mentat server and
interacting with its features, including config management, notifications,
and command execution.
"""

from mentat_sdk.client import MentatClient
from mentat_sdk.logger import MentatLogger

__version__ = "0.1.0"

__all__ = ["MentatClient", "MentatLogger"]
