import logging
from datetime import timedelta
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import OpenAIClient
from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class HacsAiTokenUsageCoordinator(DataUpdateCoordinator):
    """Coordinator for fetching OpenAI token usage."""

    def __init__(self, hass, config_entry):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=DEFAULT_UPDATE_INTERVAL),
        )
        self.api = OpenAIClient(
            config_entry.data["api_key"], config_entry.data.get("org_id")
        )

    async def _async_update_data(self):
        """Fetch data from OpenAI API."""
        try:
            async with async_timeout.timeout(30):
                return await self.api.fetch_usage()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
