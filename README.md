# Been Map - Home Assistant Custom Integration

A Home Assistant integration and Lovelace card that tracks and displays countries a person has visited on an interactive SVG world map.

![Been Map](https://img.shields.io/badge/Home%20Assistant-2024.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Track visited countries**: Automatically track countries based on person entity location
- **Coordinates-based detection**: Uses latitude/longitude to determine country via bounding boxes
- **Zone-based detection**: Falls back to timezone/zone mapping for country detection
- **Manual country management**: Add/remove countries manually via services
- **Interactive SVG world map**: Beautiful visual representation of visited countries
- **Customizable colors**: Configure colors for visited, current, and unvisited countries
- **Current location highlighting**: Current country has more pronounced borders
- **Tooltips**: Hover over countries to see their name and status
- **Responsive design**: Works on all screen sizes

## Installation

### Via HACS

1. Open HACS in Home Assistant
2. Go to "Integrations" → "Explore & Download Repositories"
3. Search for "Been Map"
4. Click "Download" and follow the instructions

### Manual Installation

1. Copy the `custom_components/been_map` directory to your Home Assistant `custom_components` folder
2. Copy `been-map-card.js` file to your `www` folder
3. Restart Home Assistant
4. Add the integration via Settings → Devices & Services → Add Integration → Been Map

## Configuration

### Integration Setup

After installing the integration, add it via the UI:

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Been Map**
4. Configure the following options:

| Option | Description | Default |
|--------|-------------|---------|
| Person Entity | Select the person entity to track | `person.person` |
| Manual Countries | Comma-separated list of country codes (e.g., US, GB, FR) | `[]` |
| Visited Color | Color for countries that have been visited | `#4CAF50` (green) |
| Current Color | Color for the current location | `#FF5722` (orange) |
| Unvisited Color | Color for countries not yet visited | `#FFFFFF` (white) |

### Lovelace Card Configuration

Add the card to your Lovelace dashboard:

```yaml
type: custom:been-map-card
entity: sensor.been_map
title: My Travel Map
visited_color: '#4CAF50'
current_color: '#FF5722'
unvisited_color: '#FFFFFF'
border_color: '#CCCCCC'
border_width: 1
current_border_width: 3
height: 400
manual_countries:
  - US
  - GB
  - FR
```

#### Card Options

| Option | Description | Default |
|--------|-------------|---------|
| `entity` | The Been Map sensor entity | `sensor.been_map` |
| `title` | Card title | `Been Map` |
| `visited_color` | Color for visited countries | `#4CAF50` |
| `current_color` | Color for current location | `#FF5722` |
| `unvisited_color` | Color for unvisited countries | `#FFFFFF` |
| `border_color` | Border color for countries | `#CCCCCC` |
| `border_width` | Border width (in pixels) | `1` |
| `current_border_width` | Border width for current country | `3` |
| `height` | Map height in pixels | `400` |
| `manual_countries` | List of country codes to mark as visited | `[]` |

## Services

The integration provides three services for managing visited countries:

### Add Visited Country

Manually add a country to the visited list.

**Service:** `been_map.add_visited_country`

**Data:**
```yaml
country_code: "US"
```

### Remove Visited Country

Remove a country from the visited list.

**Service:** `been_map.remove_visited_country`

**Data:**
```yaml
country_code: "US"
```

### Set Visited Countries

Set the complete list of visited countries (replaces existing list).

**Service:** `been_map.set_visited_countries`

**Data:**
```yaml
country_codes:
  - "US"
  - "GB"
  - "FR"
  - "DE"
```

## Country Codes

Country codes use the ISO 3166-1 alpha-2 format (e.g., US, GB, FR, DE, JP, AU).

### Common Country Codes

| Code | Country |
|------|---------|
| US | United States |
| GB | United Kingdom |
| FR | France |
| DE | Germany |
| IT | Italy |
| ES | Spain |
| CA | Canada |
| AU | Australia |
| JP | Japan |
| CN | China |
| IN | India |
| BR | Brazil |
| RU | Russia |
| ZA | South Africa |
| MX | Mexico |
| AR | Argentina |

For a complete list, see the [`countries.json`](custom_components/been_map/data/countries.json) file.

## How It Works

### Automatic Tracking

The integration tracks countries by monitoring the selected person entity:

1. **Coordinates-based detection**: When a person's latitude/longitude changes, the integration checks which country's bounding box contains those coordinates
2. **Zone-based detection**: As a fallback, when a person enters a zone that corresponds to a country, that country is automatically added to the visited list
3. The current country is highlighted with a different color and thicker border

### Manual Management

You can also manually manage visited countries:
- Use services to add/remove countries
- Configure manual countries in the integration setup
- Override countries in the card configuration

### Country Detection

The integration uses two methods for country detection:

1. **Bounding Box Detection**: Uses latitude/longitude coordinates and checks which country's bounding box contains the point. This is the most accurate method.
2. **Timezone/Zone Detection**: Falls back to mapping timezones and zones to countries when coordinates are not available.

## Troubleshooting

### Countries Not Showing

1. Verify the person entity is correctly configured
2. Check that the person has latitude/longitude attributes available
3. Ensure country codes are valid (ISO 3166-1 alpha-2 format)
4. Check Home Assistant logs for debug messages

### Map Not Loading

1. Clear your browser cache
2. Check the browser console for errors
3. Verify that `been-map-card.js` file is in your `www` folder
4. Ensure the `countries.json` file is accessible at `/local/been_map/countries.json`

### Services Not Working

1. Ensure the integration is properly loaded
2. Check Home Assistant logs for errors
3. Verify you're using the correct country codes

### Country Detection Issues

The bounding box method provides approximate country detection. For more precise detection:
1. Ensure your person entity has accurate GPS coordinates
2. The integration logs debug messages showing detected countries
3. Check the logs to see which country was detected for your coordinates

## Development

### Project Structure

```
been_map/
├── custom_components/
│   └── been_map/
│       ├── __init__.py          # Main integration file
│       ├── const.py             # Constants and country data loader
│       ├── config_flow.py       # Configuration flow
│       ├── sensor.py            # Sensor entity with coordinate detection
│       ├── services.yaml         # Service definitions
│       ├── strings.json         # Localization strings
│       ├── data/
│       │   └── countries.json   # Country data, paths, and bounding boxes
│       └── www/
│           └── been-map-card.js  # Lovelace card
├── hacs.json                   # HACS configuration
├── manifest.json               # Integration manifest
└── README.md                  # This file
```

### Adding New Countries

To add a new country to the map:

1. Edit [`custom_components/been_map/data/countries.json`](custom_components/been_map/data/countries.json)
2. Add an entry with:
   - `name`: Country name
   - `path`: SVG path for the map display
   - `bounding_box`: `[min_lat, max_lat, min_lon, max_lon]`

Example:
```json
"XX": {
  "name": "Country Name",
  "path": "M x,y L x,y ...",
  "bounding_box": [min_lat, max_lat, min_lon, max_lon]
}
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License.

## Credits

- Built for Home Assistant
- Inspired by travel tracking applications
- SVG map paths based on simplified world map data
- Bounding boxes for coordinate-based country detection
