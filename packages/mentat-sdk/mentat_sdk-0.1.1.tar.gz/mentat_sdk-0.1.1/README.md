# Mentat SDK

A Python client SDK for interacting with the Mentat web server.

## Features

- **Configuration Management**: Access server configuration
- **Notifications**: Create notifications with possible responses and handle user interactions
- **Commands**: Execute commands received from the server and report progress

## Installation

### Using Poetry (recommended)

```bash
poetry add mentat-sdk
```

### Using pip

```bash
pip install mentat-sdk
```

## Quick Start

```python
import logging
from mentat_sdk import MentatClient, MentatLogger

# Initialize a logger
logger = MentatLogger("my_app")

# Create a client instance
client = MentatClient(
    host="0.0.0.0",  # Default host
    port=8765,       # Default port
    log_level=logging.INFO
)

# Access configuration
config = client.config
logger.info(f"Server configuration: {config}")

# Create a notification
notification_id = client.create_notification(
    title="System Update Available",
    description="A new system update is available. Would you like to install it now?",
    possible_responses=["Accept", "Decline"],
    response_callback=lambda notification_id, response: logger.info(f"User selected: {response}")
)

# Check for notification response later
has_response, response = client.get_notification_response(notification_id)
if has_response:
    logger.info(f"Response received: {response}")
```

## Working with Commands

Register handlers for commands from the server:

```python
from mentat_sdk import MentatLogger

# Initialize a logger
logger = MentatLogger("command_handler")

def handle_system_restart(command_id, parameters):
    # Acknowledge the command
    client.acknowledge_command(
        command_id=command_id,
        has_progress_percentage=True,
        progress_steps={
            "0": "Starting",
            "1": "Shutting down services",
            "2": "Restarting system",
            "3": "Done"
        }
    )
    
    try:
        # Update progress
        client.update_command_progress(
            command_id=command_id,
            progress_step="Starting",
            progress_step_status="started",
            progress_percentage=10
        )
        
        # ... perform the actual work ...
        
        # Complete the command
        client.command_executed(command_id)
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        # Report error
        client.command_execution_error(command_id, str(e))

# Register the handler
client.register_command_handler("system_restart", handle_system_restart)
```

## Full Example

See the `tests/running.py` file for a complete example of using the SDK.

## License

MIT

## For Contributors

### Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/ylan-skoz/mentat-sdk.git
   cd mentat-sdk
   ```

2. Install dependencies with Poetry
   ```bash
   poetry install
   ```

3. Run tests
   ```bash
   poetry run pytest
   ```

### Releasing a New Version

This package uses GitHub Actions for automated testing and deployment to PyPI. To release a new version:

1. Update version in both files:
   - `pyproject.toml`: Update the `version` field
   - `mentat_sdk/__init__.py`: Update the `__version__` variable

2. Create a git tag with the version number:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

3. The GitHub Actions workflow will automatically:
   - Run tests against multiple Python versions
   - Build the package
   - Publish to PyPI if all tests pass

Note: You'll need a PyPI API token stored as a GitHub repository secret named `PYPI_API_TOKEN`.
