import aiohttp
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client
from .api import OpenAIClient
from .const import CONF_API_KEY, CONF_ORG_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


class HacsAiTokenUsageConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            # Validate by attempting API call
            session = aiohttp_client.async_get_clientsession(self.hass)
            client = OpenAIClient(user_input[CONF_API_KEY], user_input.get(CONF_ORG_ID))
            try:
                await client.fetch_usage()
                # If success, create entry
                await self.async_set_unique_id(user_input[CONF_API_KEY])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"OpenAI Usage ({user_input[CONF_API_KEY][:8]}...)",
                    data=user_input,
                )
            except aiohttp.ClientResponseError as e:
                _LOGGER.error("OpenAI API error: %s - %s", e.status, e.message)
                if e.status == 403:
                    errors["base"] = "access_forbidden"
                elif e.status == 401:
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"
            except aiohttp.ClientError as e:
                _LOGGER.error("OpenAI API connection failed: %s", e)
                errors["base"] = "cannot_connect"
            except Exception as e:
                _LOGGER.error("Unexpected error during OpenAI API validation: %s", e)
                errors["base"] = "cannot_connect"
            except Exception as e:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_ORG_ID): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(self, entry_data):
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        if user_input:
            return await self.async_step_user()
        return self.async_show_form(
            step_id="reauth_confirm", data_schema=vol.Schema({})
        )
