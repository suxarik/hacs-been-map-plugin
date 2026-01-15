"""Constants for Been Map integration."""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "been_map"
PLATFORMS = ["sensor"]

# Configuration keys
CONF_PERSON_ENTITY_ID = "person_entity_id"
CONF_MANUAL_COUNTRIES = "manual_countries"
CONF_VISITED_COLOR = "visited_color"
CONF_CURRENT_COLOR = "current_color"
CONF_UNVISITED_COLOR = "unvisited_color"

# Default values
DEFAULT_VISITED_COLOR = "#4CAF50"
DEFAULT_CURRENT_COLOR = "#FF5722"
DEFAULT_UNVISITED_COLOR = "#FFFFFF"

# Path to countries data file
COUNTRIES_DATA_PATH = Path(__file__).parent / "data" / "countries.json"


def load_countries() -> dict[str, str]:
    """Load countries from JSON file."""
    try:
        with open(COUNTRIES_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {code: info["name"] for code, info in data.get("countries", {}).items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_countries_with_paths() -> dict[str, dict[str, str]]:
    """Load countries with paths from JSON file."""
    try:
        with open(COUNTRIES_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("countries", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Load countries at module import
COUNTRIES = load_countries()
COUNTRIES_WITH_PATHS = load_countries_with_paths()
