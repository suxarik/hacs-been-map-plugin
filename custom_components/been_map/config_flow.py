"""Config flow for Been Map integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

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
    DOMAIN,
    DEFAULT_CURRENT_COLOR,
    DEFAULT_UNVISITED_COLOR,
    DEFAULT_VISITED_COLOR,
)

_LOGGER = logging.getLogger(__name__)


def validate_person_entity(hass: HomeAssistant, person_entity_id: str) -> bool:
    """Validate that the person entity exists."""
    return hass.states.get(person_entity_id) is not None


class BeenMapConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Been Map."""

    VERSION = 1

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
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title="Been Map",
                    data=user_input,
                )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_PERSON_ENTITY_ID,
                    default="person.person",
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="person")
                ),
                vol.Optional(
                    CONF_MANUAL_COUNTRIES,
                    default=[],
                ): selector.ObjectSelector(),
                vol.Optional(
                    CONF_VISITED_COLOR,
                    default=DEFAULT_VISITED_COLOR,
                ): selector.ColorSelector(),
                vol.Optional(
                    CONF_CURRENT_COLOR,
                    default=DEFAULT_CURRENT_COLOR,
                ): selector.ColorSelector(),
                vol.Optional(
                    CONF_UNVISITED_COLOR,
                    default=DEFAULT_UNVISITED_COLOR,
                ): selector.ColorSelector(),
            }
        )

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
