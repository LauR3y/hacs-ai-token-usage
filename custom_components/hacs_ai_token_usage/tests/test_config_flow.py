import pytest
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType
from custom_components.hacs_ai_token_usage import config_flow


async def test_config_flow_success(hass):
    """Test successful config flow."""
    flow = config_flow.HacsAiTokenUsageConfigFlow()
    flow.hass = hass
    result = await flow.async_step_user({"api_key": "test_key", "org_id": "test_org"})
    assert result["type"] == FlowResultType.CREATE_ENTRY
