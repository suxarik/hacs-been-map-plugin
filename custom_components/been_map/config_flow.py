"""Config flow for Been Map integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_CURRENT_COLOR,
    CONF_MANUAL_COUNTRIES,
    CONF_PERSON_ENTITY_ID,
    CONF_UNVISITED_COLOR,
    CONF_VISITED_COLOR,
    DEFAULT_CURRENT_COLOR,
    DEFAULT_UNVISITED_COLOR,
    DEFAULT_VISITED_COLOR,
)

_LOGGER = logging.getLogger(__name__)


def validate_person_entity(hass: HomeAssistant, person_entity_id: str) -> bool:
    """Validate that the person entity exists."""
    return hass.states.get(person_entity_id) is not None


class BeenMapConfigFlow(config_entries.ConfigFlow, domain="been_map"):
    """Handle a config flow for Been Map."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        super().__init__()
        self._init_info = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate person entity
            if not validate_person_entity(self.hass, user_input[CONF_PERSON_ENTITY_ID]):
                errors[CONF_PERSON_ENTITY_ID] = "invalid_person"
            else:
                await self.async_set_unique_id("been_map")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="Been Map",
                    data=user_input,
                )

        data_schema = {
            "person_entity_id": selector.EntitySelector(
                selector.EntitySelectorConfig(domain="person")
            ),
            "manual_countries": selector.ObjectSelector(),
            "visited_color": selector.ColorSelector(
                selector.ColorSelectorConfig(default=DEFAULT_VISITED_COLOR)
            ),
            "current_color": selector.ColorSelector(
                selector.ColorSelectorConfig(default=DEFAULT_CURRENT_COLOR)
            ),
            "unvisited_color": selector.ColorSelector(
                selector.ColorSelectorConfig(default=DEFAULT_UNVISITED_COLOR)
            ),
        }

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_import(
        self, import_data: dict[str, Any]
    ) -> FlowResult:
        """Import a config entry from configuration.yaml."""
        return await self.async_step_user(import_data)
