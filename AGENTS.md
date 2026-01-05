# AGENTS.md - Coding Guidelines for HACS AI Token Usage

This file provides coding guidelines for agents working on the HACS AI Token Usage repository, a Home Assistant custom integration for monitoring OpenAI token usage.

## Repository Overview
- **Language**: Python 3.9+
- **Framework**: Home Assistant custom integration
- **Purpose**: Fetch and expose OpenAI token usage data as sensors
- **Structure**: Standard HA integration with async API polling, config flow, and sensors

## 1. Build/Lint/Test Commands

### Testing
Run all tests:
```
pytest
```

Run tests in a specific file:
```
pytest custom_components/hacs_ai_token_usage/tests/test_config_flow.py
```

Run a single test:
```
pytest custom_components/hacs_ai_token_usage/tests/test_config_flow.py::test_config_flow_success
```

Run tests with coverage:
```
pytest --cov=custom_components/hacs_ai_token_usage
```

### Linting
Use Ruff for fast linting and formatting:
```
ruff check .
ruff format .
```

If Ruff is not available, use Flake8:
```
flake8 custom_components/hacs_ai_token_usage
```

### Type Checking
Use MyPy for static type analysis:
```
mypy custom_components/hacs_ai_token_usage
```

### Code Quality Checks
Run all quality checks:
```
ruff check . && ruff format --check . && mypy custom_components/hacs_ai_token_usage && pytest
```

### Home Assistant Validation
Validate integration with HA:
```
python -m homeassistant --config /path/to/config --script check_config
```

## 2. Code Style Guidelines

### General Principles
- Follow PEP 8 with 88-character line length (Ruff default)
- Use type hints for all function parameters and return values
- Prefer async/await for I/O operations
- Write descriptive docstrings for classes and public methods
- Keep functions small and focused (single responsibility)
- Use meaningful variable names; avoid abbreviations

### Imports
- Group imports: standard library, third-party, local
- Use absolute imports within the integration
- Sort imports alphabetically within groups
- Example:
```python
import logging
from typing import Dict, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
```

### Naming Conventions
- **Variables/Functions**: snake_case (e.g., `fetch_usage`, `api_key`)
- **Classes**: PascalCase (e.g., `OpenAIClient`, `HacsAiTokenUsageCoordinator`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DOMAIN`, `DEFAULT_UPDATE_INTERVAL`)
- **Files**: snake_case matching class names (e.g., `config_flow.py`)
- **Test Functions**: snake_case with descriptive names (e.g., `test_config_flow_success`)

### Type Hints
- Use typing module for complex types
- Specify Optional for nullable types
- Example:
```python
from typing import Optional

def fetch_data(api_key: str, org_id: Optional[str] = None) -> Dict[str, Any]:
    pass
```

### Async Programming
- Use async/await consistently for HA integration patterns
- Always use `async with` for HTTP sessions
- Handle timeouts with `async_timeout`
- Example:
```python
async with aiohttp.ClientSession() as session:
    async with async_timeout.timeout(30):
        async with session.get(url) as response:
            return await response.json()
```

### Error Handling
- Catch specific exceptions, not broad `Exception`
- Use `_LOGGER` for logging errors
- Raise `UpdateFailed` for coordinator errors
- Example:
```python
try:
    data = await self.api.fetch_usage()
except aiohttp.ClientError as err:
    _LOGGER.error("API request failed: %s", err)
    raise UpdateFailed(f"API error: {err}") from err
```

### Logging
- Use module-level `_LOGGER = logging.getLogger(__name__)`
- Log at appropriate levels: debug, info, warning, error
- Include context in log messages
- Example:
```python
_LOGGER.info("Fetching usage data for org %s", org_id)
```

### Docstrings
- Use Google-style docstrings
- Document parameters, return types, and exceptions
- Example:
```python
def fetch_usage(self) -> Dict[str, Any]:
    """Fetch aggregated token usage from OpenAI API.

    Returns:
        Dict containing input_tokens, output_tokens, etc.

    Raises:
        aiohttp.ClientError: If API request fails.
    """
```

### Configuration and Constants
- Define constants in `const.py`
- Use meaningful names for config entry keys
- Validate user input in config flow

### Sensor and Entity Guidelines
- Extend appropriate base classes (SensorEntity, CoordinatorEntity)
- Set unique_id for entity persistence
- Use device_class and state_class appropriately
- Provide extra_state_attributes for additional data

### Testing
- Use pytest fixtures for HA components
- Mock external API calls
- Test both success and failure paths
- Name test files as `test_*.py`
- Example test structure:
```python
async def test_sensor_native_value(hass, coordinator, config_entry):
    sensor = MySensor(coordinator, config_entry)
    coordinator.data = {"value": 42}
    assert sensor.native_value == 42
```

### Security
- Never log API keys or sensitive data
- Use HTTPS for all external requests
- Validate user input to prevent injection

### Git Practices
- Write clear commit messages
- Use conventional commits (feat:, fix:, docs:, etc.)
- Create releases for new versions
- Update manifest.json version on changes

### Home Assistant Specific
- Follow HA integration file structure
- Use config_entries for modern setup
- Handle reauth for expired credentials
- Implement proper unload/cleanup
- Test with HA dev environment

### Performance
- Avoid blocking operations in async code
- Use appropriate polling intervals
- Cache data when possible
- Profile with HA's built-in tools

### Documentation
- Keep README.md up-to-date
- Document breaking changes
- Use examples in docstrings
- Reference HA docs for integration patterns

## External Rules
No Cursor rules (.cursor/rules/ or .cursorrules) or Copilot rules (.github/copilot-instructions.md) found. Follow these guidelines for consistency.

## Tools and Dependencies
- Python 3.9+
- aiohttp for HTTP requests
- pytest for testing
- ruff for linting/formatting
- mypy for type checking
- Home Assistant core for integration development

This guide ensures consistent, maintainable code across the repository. Update as needed for new patterns or tools.