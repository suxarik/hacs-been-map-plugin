"""Sensor platform for Been Map integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CURRENT_COLOR,
    CONF_MANUAL_COUNTRIES,
    CONF_PERSON_ENTITY_ID,
    CONF_UNVISITED_COLOR,
    CONF_VISITED_COLOR,
    COUNTRIES_WITH_PATHS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Been Map sensor from config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities(
        [
            BeenMapSensor(
                entry,
                data[CONF_PERSON_ENTITY_ID],
                data[CONF_MANUAL_COUNTRIES],
                data[CONF_VISITED_COLOR],
                data[CONF_CURRENT_COLOR],
                data[CONF_UNVISITED_COLOR],
            )
        ]
    )


class BeenMapSensor(SensorEntity):
    """Representation of a Been Map sensor."""

    def __init__(
        self,
        entry: ConfigEntry,
        person_entity_id: str,
        manual_countries: list[str],
        visited_color: str,
        current_color: str,
        unvisited_color: str,
    ) -> None:
        """Initialize sensor."""
        self._entry = entry
        self._person_entity_id = person_entity_id
        self._manual_countries = manual_countries or []
        self._visited_color = visited_color
        self._current_color = current_color
        self._unvisited_color = unvisited_color
        self._attr_unique_id = f"{DOMAIN}_sensor"
        self._attr_name = "Been Map"
        self._attr_has_entity_name = True
        self._visited_countries: set[str] = set(self._manual_countries)
        self._current_country: str | None = None
        self._last_coordinates: tuple[float, float] | None = None
        self._country_cache: dict[tuple[float, float], str] = {}

    @property
    def native_value(self) -> str:
        """Return state of sensor."""
        return f"{len(self._visited_countries)} countries"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "visited_countries": sorted(list(self._visited_countries)),
            "current_country": self._current_country,
            "visited_color": self._visited_color,
            "current_color": self._current_color,
            "unvisited_color": self._unvisited_color,
            "person_entity_id": self._person_entity_id,
        }

    def get_country_from_zone(self, zone: str | None) -> str | None:
        """Get country code from zone attribute."""
        if zone is None:
            return None
        
        # Try to extract country code from zone
        # Zone format can be: "Europe/Berlin", "America/New_York", etc.
        # Or it could be a country code directly
        if len(zone) == 2 and zone.upper() in COUNTRIES_WITH_PATHS:
            return zone.upper()
        
        # Map common timezones to countries
        timezone_to_country = {
            "Europe/London": "GB",
            "Europe/Paris": "FR",
            "Europe/Berlin": "DE",
            "Europe/Rome": "IT",
            "Europe/Madrid": "ES",
            "Europe/Amsterdam": "NL",
            "Europe/Brussels": "BE",
            "Europe/Vienna": "AT",
            "Europe/Zurich": "CH",
            "Europe/Stockholm": "SE",
            "Europe/Oslo": "NO",
            "Europe/Copenhagen": "DK",
            "Europe/Helsinki": "FI",
            "Europe/Warsaw": "PL",
            "Europe/Prague": "CZ",
            "Europe/Budapest": "HU",
            "Europe/Athens": "GR",
            "Europe/Lisbon": "PT",
            "Europe/Dublin": "IE",
            "America/New_York": "US",
            "America/Los_Angeles": "US",
            "America/Chicago": "US",
            "America/Toronto": "CA",
            "America/Vancouver": "CA",
            "America/Mexico_City": "MX",
            "America/Sao_Paulo": "BR",
            "America/Buenos_Aires": "AR",
            "Asia/Tokyo": "JP",
            "Asia/Shanghai": "CN",
            "Asia/Hong_Kong": "HK",
            "Asia/Seoul": "KR",
            "Asia/Singapore": "SG",
            "Asia/Dubai": "AE",
            "Asia/Kolkata": "IN",
            "Asia/Bangkok": "TH",
            "Asia/Jakarta": "ID",
            "Asia/Manila": "PH",
            "Asia/Kuala_Lumpur": "MY",
            "Australia/Sydney": "AU",
            "Australia/Melbourne": "AU",
            "Pacific/Auckland": "NZ",
            "Africa/Cairo": "EG",
            "Africa/Johannesburg": "ZA",
            "Africa/Lagos": "NG",
        }
        
        return timezone_to_country.get(zone)

    def get_country_from_coordinates(self, latitude: float, longitude: float) -> str | None:
        """
        Get country code from latitude/longitude using bounding boxes.
        
        This method checks if coordinates fall within a country's bounding box
        from the countries.json data file.
        """
        # Round coordinates to reduce cache size
        rounded_lat = round(latitude, 2)
        rounded_lon = round(longitude, 2)
        coord_key = (rounded_lat, rounded_lon)
        
        # Check cache first
        if coord_key in self._country_cache:
            return self._country_cache[coord_key]
        
        # Check which country coordinates fall within
        for country_code, country_data in COUNTRIES_WITH_PATHS.items():
            bounding_box = country_data.get("bounding_box")
            if bounding_box and len(bounding_box) == 4:
                min_lat, max_lat, min_lon, max_lon = bounding_box
                if (min_lat <= latitude <= max_lat and 
                    min_lon <= longitude <= max_lon):
                    self._country_cache[coord_key] = country_code
                    _LOGGER.debug(
                        "Country detected from coordinates (%s, %s): %s",
                        latitude, longitude, country_code
                    )
                    return country_code
        
        # If no match found, return None
        self._country_cache[coord_key] = None
        return None

    def update(self) -> None:
        """Update sensor state."""
        hass = self.hass
        person_state = hass.states.get(self._person_entity_id)
        
        if person_state is None:
            _LOGGER.warning("Person entity %s not found", self._person_entity_id)
            return
        
        # Get current country from person's location
        zone = person_state.attributes.get("zone")
        country_from_zone = None
        
        if zone and zone != "home":
            country_from_zone = self.get_country_from_zone(zone)
            if country_from_zone and country_from_zone in COUNTRIES_WITH_PATHS:
                self._current_country = country_from_zone
                self._visited_countries.add(country_from_zone)
        
        # Check for latitude/longitude for more accurate country detection
        latitude = person_state.attributes.get("latitude")
        longitude = person_state.attributes.get("longitude")
        
        if latitude is not None and longitude is not None:
            current_coords = (latitude, longitude)
            
            # Only update if coordinates have changed significantly
            if (self._last_coordinates is None or 
                abs(current_coords[0] - self._last_coordinates[0]) > 0.01 or
                abs(current_coords[1] - self._last_coordinates[1]) > 0.01):
                
                country_from_coords = self.get_country_from_coordinates(latitude, longitude)
                
                if country_from_coords and country_from_coords in COUNTRIES_WITH_PATHS:
                    # Prefer coordinates-based detection over zone-based
                    self._current_country = country_from_coords
                    self._visited_countries.add(country_from_coords)
                
                self._last_coordinates = current_coords
        
        self.async_write_ha_state()
