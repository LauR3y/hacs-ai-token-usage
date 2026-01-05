from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import HacsAiTokenUsageCoordinator
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            OpenAIInputTokensSensor(coordinator, config_entry),
            OpenAIOutputTokensSensor(coordinator, config_entry),
            OpenAITotalTokensSensor(coordinator, config_entry),
        ]
    )


class OpenAIInputTokensSensor(CoordinatorEntity, SensorEntity):
    """Sensor for OpenAI input tokens."""

    def __init__(self, coordinator: HacsAiTokenUsageCoordinator, config_entry):
        super().__init__(coordinator)
        self._attr_name = f"OpenAI Input Tokens ({config_entry.data['api_key'][:8]}...)"
        self._attr_unique_id = f"{config_entry.entry_id}_input_tokens"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = "tokens"

    @property
    def native_value(self):
        return self.coordinator.data.get("input_tokens", 0)

    @property
    def extra_state_attributes(self):
        return {"last_updated": self.coordinator.data.get("last_updated")}


class OpenAIOutputTokensSensor(CoordinatorEntity, SensorEntity):
    """Sensor for OpenAI output tokens."""

    def __init__(self, coordinator: HacsAiTokenUsageCoordinator, config_entry):
        super().__init__(coordinator)
        self._attr_name = (
            f"OpenAI Output Tokens ({config_entry.data['api_key'][:8]}...)"
        )
        self._attr_unique_id = f"{config_entry.entry_id}_output_tokens"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = "tokens"

    @property
    def native_value(self):
        return self.coordinator.data.get("output_tokens", 0)

    @property
    def extra_state_attributes(self):
        return {"last_updated": self.coordinator.data.get("last_updated")}


class OpenAITotalTokensSensor(CoordinatorEntity, SensorEntity):
    """Sensor for OpenAI total tokens."""

    def __init__(self, coordinator: HacsAiTokenUsageCoordinator, config_entry):
        super().__init__(coordinator)
        self._attr_name = f"OpenAI Total Tokens ({config_entry.data['api_key'][:8]}...)"
        self._attr_unique_id = f"{config_entry.entry_id}_total_tokens"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = "tokens"

    @property
    def native_value(self):
        return self.coordinator.data.get("total_tokens", 0)

    @property
    def extra_state_attributes(self):
        return {"last_updated": self.coordinator.data.get("last_updated")}
