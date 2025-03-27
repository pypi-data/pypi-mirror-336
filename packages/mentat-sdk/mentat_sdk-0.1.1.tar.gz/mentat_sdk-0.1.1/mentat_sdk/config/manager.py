"""
Configuration manager for the Mentat SDK.

This module handles the storage and retrieval of configuration data
received from the Mentat server.
"""

import logging
import time
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages configuration data for the Mentat SDK.

    This class stores and provides access to configuration data
    received from the Mentat server.
    """

    def __init__(self):
        """Initialize a new configuration manager."""
        self._config: Dict[str, Any] = {}
        self._initial_config_received = False

    def update_config(self, config: Dict[str, Any]) -> None:
        """
        Update the configuration with new data.

        Args:
            config (Dict[str, Any]): The new configuration data.

        Raises:
            TypeError: If config is not a dictionary.
        """
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")

        self._config = config
        self._initial_config_received = True
        logger.debug(f"Updated configuration: {config}")

    def get_config(self) -> Dict[str, Any]:
        """
        Get the current configuration.

        Returns:
            Dict[str, Any]: The current configuration.

        Raises:
            TimeoutError: If the initial configuration is not received within 0.1 seconds.
        """
        if not self._initial_config_received:
            # Wait up to 0.1 seconds for initial config
            start_time = time.time()
            while not self._initial_config_received and time.time() - start_time < 0.1:
                time.sleep(0.01)  # Small sleep to prevent busy waiting

            if not self._initial_config_received:
                raise TimeoutError(
                    "Initial configuration not received from server within 0.1 seconds"
                )

        return self._config
