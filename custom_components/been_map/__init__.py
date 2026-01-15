"""The Been Map integration."""
from __future__ import annotations

import logging
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.service import async_register_admin_service

from .const import COUNTRIES, DOMAIN

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "been_map"
PLATFORMS: Final = (Platform.SENSOR,)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Been Map from a config entry."""
    _LOGGER.info("Setting up Been Map integration")
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "person_entity_id": entry.data.get("person_entity_id"),
        "manual_countries": entry.data.get("manual_countries", []),
        "visited_color": entry.data.get("visited_color", "#4CAF50"),
        "current_color": entry.data.get("current_color", "#FF5722"),
        "unvisited_color": entry.data.get("unvisited_color", "#FFFFFF"),
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    async_register_admin_service(
        hass,
        DOMAIN,
        "add_visited_country",
        async_add_visited_country,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        "remove_visited_country",
        async_remove_visited_country,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        "set_visited_countries",
        async_set_visited_countries,
    )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Been Map integration")
    
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_add_visited_country(service: ServiceCall) -> None:
    """Add a country to the visited list."""
    country_code = service.data.get("country_code", "").upper()
    
    if country_code not in COUNTRIES:
        _LOGGER.error("Invalid country code: %s", country_code)
        return
    
    hass = service.hass
    for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
        if country_code not in entry_data.get("manual_countries", []):
            entry_data.setdefault("manual_countries", []).append(country_code)
            _LOGGER.info("Added country %s to visited list", country_code)
            
            # Update sensor state
            sensor_entity_id = f"sensor.{DOMAIN}_sensor"
            if sensor_entity_id in hass.states:
                state = hass.states.get(sensor_entity_id)
                if state and state.attributes:
                    visited = list(state.attributes.get("visited_countries", []))
                    if country_code not in visited:
                        visited.append(country_code)
                        hass.states.async_set(
                            sensor_entity_id,
                            state.state,
                            {**state.attributes, "visited_countries": visited}
                        )


async def async_remove_visited_country(service: ServiceCall) -> None:
    """Remove a country from the visited list."""
    country_code = service.data.get("country_code", "").upper()
    
    hass = service.hass
    for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
        if country_code in entry_data.get("manual_countries", []):
            entry_data["manual_countries"].remove(country_code)
            _LOGGER.info("Removed country %s from visited list", country_code)
            
            # Update sensor state
            sensor_entity_id = f"sensor.{DOMAIN}_sensor"
            if sensor_entity_id in hass.states:
                state = hass.states.get(sensor_entity_id)
                if state and state.attributes:
                    visited = list(state.attributes.get("visited_countries", []))
                    if country_code in visited:
                        visited.remove(country_code)
                        hass.states.async_set(
                            sensor_entity_id,
                            state.state,
                            {**state.attributes, "visited_countries": visited}
                        )


async def async_set_visited_countries(service: ServiceCall) -> None:
    """Set the complete list of visited countries."""
    country_codes = service.data.get("country_codes", [])
    
    if not isinstance(country_codes, list):
        _LOGGER.error("country_codes must be a list")
        return
    
    # Validate country codes
    valid_codes = [code.upper() for code in country_codes if code.upper() in COUNTRIES]
    invalid_codes = [code for code in country_codes if code.upper() not in COUNTRIES]
    
    if invalid_codes:
        _LOGGER.warning("Invalid country codes: %s", invalid_codes)
    
    hass = service.hass
    for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
        entry_data["manual_countries"] = valid_codes
        _LOGGER.info("Set visited countries: %s", valid_codes)
        
        # Update sensor state
        sensor_entity_id = f"sensor.{DOMAIN}_sensor"
        if sensor_entity_id in hass.states:
            state = hass.states.get(sensor_entity_id)
            if state:
                hass.states.async_set(
                    sensor_entity_id,
                    str(len(valid_codes)) + " countries",
                    {**state.attributes, "visited_countries": valid_codes}
                )
