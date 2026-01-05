import pytest
from custom_components.hacs_ai_token_usage.sensor import OpenAITotalTokensSensor


async def test_sensor_native_value(hass, coordinator, config_entry):
    """Test sensor value."""
    sensor = OpenAITotalTokensSensor(coordinator, config_entry)
    coordinator.data = {"total_tokens": 100}
    assert sensor.native_value == 100
