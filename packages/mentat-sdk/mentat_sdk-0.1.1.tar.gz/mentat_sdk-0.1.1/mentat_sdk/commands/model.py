"""
Command data models for the Mentat SDK.

This module defines the data structures for commands
received and managed by the Mentat SDK.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional


class Command:
    """
    Represents a command in the Mentat system.

    A command is an instruction received from the server
    that the client should execute.
    """

    def __init__(
        self,
        command_id: str,
        command_key: str,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a new command.

        Args:
            command_id (str): Unique identifier for the command.
            command_key (str): Key identifying the type of command.
            parameters (Optional[Dict[str, Any]]): Command parameters.
        """
        self.command_id = command_id
        self.command_key = command_key
        self.parameters = parameters or {}
        self.has_progress_percentage = False
        self.progress_steps: Dict[str, str] = {}
        self.current_step = None
        self.status = "received"
        self.received_at = datetime.now(timezone.utc).isoformat()

    def acknowledge(
        self,
        has_progress_percentage: bool = False,
        progress_steps: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Acknowledge the command and set up progress tracking.

        Args:
            has_progress_percentage (bool): Whether to track progress percentage.
            progress_steps (Optional[Dict[str, str]]): Progress steps for the command.
        """
        self.has_progress_percentage = has_progress_percentage
        if progress_steps:
            self.progress_steps = progress_steps
        self.status = "acknowledged"

    def update_progress(
        self,
        progress_step: str,
        progress_step_status: str,
        progress_percentage: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Update the progress of the command.

        Args:
            progress_step (str): The current progress step.
            progress_step_status (str): Status of the current step
                (started, completed, failed).
            progress_percentage (Optional[int]): Current progress percentage.

        Returns:
            Dict[str, Any]: Progress milestone data.

        Raises:
            ValueError: If progress_step is not in progress_steps values.
            ValueError: If progress_step_status is invalid.
            ValueError: If progress_percentage is provided but not enabled.
        """
        if progress_step not in self.progress_steps.values():
            raise ValueError(
                f"Progress step '{progress_step}' not defined in progress_steps values: {list(self.progress_steps.values())}"
            )

        valid_statuses = ["started", "completed", "failed"]
        if progress_step_status not in valid_statuses:
            raise ValueError(
                f"Invalid progress_step_status: {progress_step_status}. "
                f"Must be one of {valid_statuses}"
            )

        if progress_percentage is not None:
            if not self.has_progress_percentage:
                raise ValueError("Progress percentage not enabled for this command")

            if (
                not isinstance(progress_percentage, int)
                or progress_percentage < 0
                or progress_percentage > 100
            ):
                raise ValueError(
                    "Progress percentage must be an integer between 0 and 100"
                )

        self.current_step = progress_step

        # Create progress milestone
        milestone = {
            "progress_step": progress_step,
            "progress_step_status": progress_step_status,
            "progress_timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if progress_percentage is not None:
            milestone["progress_percentage"] = progress_percentage

        return milestone
