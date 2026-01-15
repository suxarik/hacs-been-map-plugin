/**
 * Been Map Lovelace Card
 * A card that displays a world map showing countries a person has been to
 */

class BeenMapCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._config = {};
    this._countries = {};
    this._visitedCountries = [];
    this._currentCountry = null;
    this._countriesData = null;
    this._loadCountriesData();
  }

  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
    };
  }

  set config(config) {
    this._config = config;
    this._sensorEntity = config.entity || 'sensor.been_map';
    this._visitedColor = config.visited_color || '#4CAF50';
    this._currentColor = config.current_color || '#FF5722';
    this._unvisitedColor = config.unvisited_color || '#FFFFFF';
    this._borderColor = config.border_color || '#CCCCCC';
    this._currentBorderWidth = config.current_border_width || 3;
    this._borderWidth = config.border_width || 1;
    this._height = config.height || 400;
    this._title = config.title || 'Been Map';
    this._manualCountries = config.manual_countries || [];
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    this.updateData();
    this.render();
  }

  getCardSize() {
    return 3;
  }

  async _loadCountriesData() {
    try {
      const response = await fetch('/local/been_map/countries.json');
      if (!response.ok) {
        throw new Error('Failed to load countries data');
      }
      const data = await response.json();
      this._countriesData = data.countries || {};
      this.render();
    } catch (error) {
      console.error('Error loading countries data:', error);
      // Fallback to embedded data if fetch fails
      this._countriesData = this._getEmbeddedCountries();
      this.render();
    }
  }

  _getEmbeddedCountries() {
    // Fallback embedded countries data
    return {
      "US": { "name": "United States", "path": "M 150,80 L 280,80 L 290,150 L 260,180 L 160,170 L 140,120 Z" },
      "CA": { "name": "Canada", "path": "M 150,30 L 280,30 L 280,80 L 150,80 Z" },
      "MX": { "name": "Mexico", "path": "M 140,180 L 260,180 L 250,220 L 150,210 Z" },
      "BR": { "name": "Brazil", "path": "M 220,250 L 280,250 L 290,350 L 240,380 L 210,320 Z" },
      "AR": { "name": "Argentina", "path": "M 200,320 L 240,380 L 230,450 L 200,440 L 190,360 Z" },
      "CO": { "name": "Colombia", "path": "M 180,240 L 220,240 L 230,280 L 190,280 Z" },
      "GB": { "name": "United Kingdom", "path": "M 430,70 L 450,70 L 450,100 L 430,100 Z" },
      "FR": { "name": "France", "path": "M 440,110 L 470,110 L 470,140 L 440,140 Z" },
      "DE": { "name": "Germany", "path": "M 470,100 L 500,100 L 500,130 L 470,130 Z" },
      "IT": { "name": "Italy", "path": "M 470,140 L 490,140 L 500,180 L 470,170 Z" },
      "ES": { "name": "Spain", "path": "M 410,140 L 440,140 L 440,170 L 410,170 Z" },
      "PL": { "name": "Poland", "path": "M 500,100 L 530,100 L 530,130 L 500,130 Z" },
      "UA": { "name": "Ukraine", "path": "M 530,100 L 570,100 L 570,130 L 530,130 Z" },
      "RU": { "name": "Russia", "path": "M 570,40 L 750,40 L 750,130 L 570,130 Z" },
      "SE": { "name": "Sweden", "path": "M 490,40 L 510,40 L 510,90 L 490,90 Z" },
      "NO": { "name": "Norway", "path": "M 470,40 L 490,40 L 490,90 L 470,90 Z" },
      "FI": { "name": "Finland", "path": "M 510,40 L 540,40 L 540,90 L 510,90 Z" },
      "NL": { "name": "Netherlands", "path": "M 450,100 L 470,100 L 470,120 L 450,120 Z" },
      "BE": { "name": "Belgium", "path": "M 440,120 L 460,120 L 460,130 L 440,130 Z" },
      "CH": { "name": "Switzerland", "path": "M 460,130 L 480,130 L 480,150 L 460,150 Z" },
      "AT": { "name": "Austria", "path": "M 480,130 L 510,130 L 510,150 L 480,150 Z" },
      "CZ": { "name": "Czech Republic", "path": "M 490,120 L 520,120 L 520,140 L 490,140 Z" },
      "GR": { "name": "Greece", "path": "M 510,160 L 530,160 L 540,180 L 510,180 Z" },
      "PT": { "name": "Portugal", "path": "M 400,150 L 410,150 L 410,180 L 400,180 Z" },
      "CN": { "name": "China", "path": "M 580,140 L 680,140 L 680,220 L 580,220 Z" },
      "JP": { "name": "Japan", "path": "M 700,140 L 730,140 L 730,190 L 700,190 Z" },
      "IN": { "name": "India", "path": "M 580,220 L 630,220 L 640,290 L 590,280 Z" },
      "KR": { "name": "South Korea", "path": "M 680,150 L 700,150 L 700,180 L 680,180 Z" },
      "TH": { "name": "Thailand", "path": "M 630,260 L 660,260 L 660,300 L 630,300 Z" },
      "VN": { "name": "Vietnam", "path": "M 650,260 L 680,260 L 680,300 L 650,300 Z" },
      "ID": { "name": "Indonesia", "path": "M 620,320 L 720,320 L 720,360 L 620,360 Z" },
      "MY": { "name": "Malaysia", "path": "M 600,300 L 650,300 L 650,320 L 600,320 Z" },
      "PH": { "name": "Philippines", "path": "M 680,270 L 720,270 L 720,310 L 680,310 Z" },
      "PK": { "name": "Pakistan", "path": "M 550,200 L 590,200 L 590,240 L 550,240 Z" },
      "IR": { "name": "Iran", "path": "M 520,180 L 560,180 L 560,220 L 520,220 Z" },
      "SA": { "name": "Saudi Arabia", "path": "M 520,230 L 580,230 L 580,280 L 520,280 Z" },
      "AE": { "name": "United Arab Emirates", "path": "M 550,250 L 570,250 L 570,270 L 550,270 Z" },
      "TR": { "name": "Turkey", "path": "M 500,150 L 540,150 L 540,180 L 500,180 Z" },
      "KZ": { "name": "Kazakhstan", "path": "M 570,100 L 650,100 L 650,150 L 570,150 Z" },
      "UZ": { "name": "Uzbekistan", "path": "M 570,150 L 620,150 L 620,190 L 570,190 Z" },
      "MN": { "name": "Mongolia", "path": "M 650,100 L 700,100 L 700,150 L 650,150 Z" },
      "AF": { "name": "Afghanistan", "path": "M 560,190 L 600,190 L 600,230 L 560,230 Z" },
      "BD": { "name": "Bangladesh", "path": "M 620,230 L 640,230 L 640,250 L 620,250 Z" },
      "LK": { "name": "Sri Lanka", "path": "M 610,290 L 630,290 L 630,310 L 610,310 Z" },
      "NP": { "name": "Nepal", "path": "M 600,220 L 620,220 L 620,240 L 600,240 Z" },
      "MM": { "name": "Myanmar", "path": "M 630,250 L 660,250 L 660,290 L 630,290 Z" },
      "KH": { "name": "Cambodia", "path": "M 640,280 L 660,280 L 660,310 L 640,310 Z" },
      "LA": { "name": "Laos", "path": "M 630,290 L 650,290 L 650,310 L 630,310 Z" },
      "SG": { "name": "Singapore", "path": "M 640,340 L 660,340 L 660,360 L 640,360 Z" },
      "EG": { "name": "Egypt", "path": "M 500,200 L 540,200 L 540,250 L 500,250 Z" },
      "ZA": { "name": "South Africa", "path": "M 520,380 L 560,380 L 560,420 L 520,420 Z" },
      "NG": { "name": "Nigeria", "path": "M 460,300 L 500,300 L 500,340 L 460,340 Z" },
      "KE": { "name": "Kenya", "path": "M 560,320 L 590,320 L 590,360 L 560,360 Z" },
      "MA": { "name": "Morocco", "path": "M 410,200 L 450,200 L 450,240 L 410,240 Z" },
      "DZ": { "name": "Algeria", "path": "M 430,190 L 470,190 L 470,230 L 430,230 Z" },
      "LY": { "name": "Libya", "path": "M 470,200 L 510,200 L 510,260 L 470,260 Z" },
      "SD": { "name": "Sudan", "path": "M 520,250 L 570,250 L 570,300 L 520,300 Z" },
      "ET": { "name": "Ethiopia", "path": "M 560,300 L 600,300 L 600,350 L 560,350 Z" },
      "TZ": { "name": "Tanzania", "path": "M 560,350 L 600,350 L 600,390 L 560,390 Z" },
      "CD": { "name": "Democratic Republic of the Congo", "path": "M 520,330 L 560,330 L 560,380 L 520,380 Z" },
      "AO": { "name": "Angola", "path": "M 490,350 L 530,350 L 530,400 L 490,400 Z" },
      "GH": { "name": "Ghana", "path": "M 450,290 L 480,290 L 480,320 L 450,320 Z" },
      "CI": { "name": "Ivory Coast", "path": "M 440,300 L 470,300 L 470,330 L 440,330 Z" },
      "SN": { "name": "Senegal", "path": "M 410,260 L 440,260 L 440,290 L 410,290 Z" },
      "MG": { "name": "Madagascar", "path": "M 590,380 L 610,380 L 610,420 L 590,420 Z" },
      "MU": { "name": "Mauritius", "path": "M 600,400 L 620,400 L 620,420 L 600,420 Z" },
      "AU": { "name": "Australia", "path": "M 680,380 L 760,380 L 760,440 L 680,440 Z" },
      "NZ": { "name": "New Zealand", "path": "M 770,420 L 800,420 L 800,460 L 770,460 Z" },
      "PG": { "name": "Papua New Guinea", "path": "M 720,310 L 760,310 L 760,350 L 720,350 Z" },
      "FJ": { "name": "Fiji", "path": "M 780,350 L 800,350 L 800,380 L 780,380 Z" },
    };
  }

  updateData() {
    if (!this._hass) return;

    const state = this._hass.states[this._sensorEntity];
    if (state && state.attributes) {
      this._visitedCountries = state.attributes.visited_countries || this._manualCountries;
      this._currentCountry = state.attributes.current_country;
      
      // Override colors from sensor attributes if available
      if (state.attributes.visited_color) {
        this._visitedColor = state.attributes.visited_color;
      }
      if (state.attributes.current_color) {
        this._currentColor = state.attributes.current_color;
      }
      if (state.attributes.unvisited_color) {
        this._unvisitedColor = state.attributes.unvisited_color;
      }
    }
  }

  render() {
    if (!this.shadowRoot || !this._countriesData) return;

    const isVisited = (countryCode) => this._visitedCountries.includes(countryCode);
    const isCurrent = (countryCode) => this._currentCountry === countryCode;

    let svgContent = '';
    
    // Render all countries from the countries data
    Object.entries(this._countriesData).forEach(([countryCode, countryInfo]) => {
      const path = countryInfo.path;
      if (path) {
        let fill = this._unvisitedColor;
        let strokeWidth = this._borderWidth;
        let stroke = this._borderColor;

        if (isCurrent(countryCode)) {
          fill = this._currentColor;
          strokeWidth = this._currentBorderWidth;
          stroke = this._currentColor;
        } else if (isVisited(countryCode)) {
          fill = this._visitedColor;
        }

        svgContent += `<path d="${path}" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}" data-country="${countryCode}" class="country-path" />`;
      }
    });

    const style = `
      <style>
        :host {
          display: block;
          font-family: var(--paper-font-body1_-_font-family);
        }
        ha-card {
          padding: 16px;
        }
        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
        }
        .card-header h3 {
          margin: 0;
          font-size: 1.2rem;
          font-weight: 500;
        }
        .stats {
          display: flex;
          gap: 16px;
          font-size: 0.9rem;
          color: var(--secondary-text-color);
        }
        .map-container {
          width: 100%;
          height: ${this._height}px;
          background: ${this._unvisitedColor};
          border-radius: 8px;
          overflow: hidden;
        }
        svg {
          width: 100%;
          height: 100%;
        }
        .country-path {
          transition: fill 0.3s ease, stroke-width 0.3s ease;
          cursor: pointer;
        }
        .country-path:hover {
          opacity: 0.8;
        }
        .legend {
          display: flex;
          gap: 16px;
          margin-top: 12px;
          font-size: 0.85rem;
          flex-wrap: wrap;
        }
        .legend-item {
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .legend-color {
          width: 16px;
          height: 16px;
          border-radius: 3px;
          border: 1px solid var(--divider-color);
        }
        .tooltip {
          position: absolute;
          background: var(--ha-card-background, var(--card-background-color, #fff));
          padding: 8px 12px;
          border-radius: 4px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.2);
          font-size: 0.85rem;
          pointer-events: none;
          z-index: 1000;
          display: none;
        }
      </style>
    `;

    this.shadowRoot.innerHTML = `
      ${style}
      <ha-card>
        <div class="card-header">
          <h3>${this._title}</h3>
          <div class="stats">
            <span>Visited: ${this._visitedCountries.length}</span>
            ${this._currentCountry ? `<span>Current: ${this._countriesData[this._currentCountry]?.name || this._currentCountry}</span>` : ''}
          </div>
        </div>
        <div class="map-container">
          <svg viewBox="0 0 800 500" preserveAspectRatio="xMidYMid meet">
            ${svgContent}
          </svg>
        </div>
        <div class="legend">
          <div class="legend-item">
            <div class="legend-color" style="background: ${this._visitedColor}"></div>
            <span>Visited</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background: ${this._currentColor}"></div>
            <span>Current</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" style="background: ${this._unvisitedColor}"></div>
            <span>Not Visited</span>
          </div>
        </div>
        <div class="tooltip" id="tooltip"></div>
      </ha-card>
    `;

    // Add tooltip functionality
    const tooltip = this.shadowRoot.getElementById('tooltip');
    const paths = this.shadowRoot.querySelectorAll('.country-path');
    
    paths.forEach(path => {
      path.addEventListener('mouseenter', (e) => {
        const countryCode = e.target.getAttribute('data-country');
        const countryInfo = this._countriesData[countryCode];
        const countryName = countryInfo?.name || countryCode;
        const visited = isVisited(countryCode);
        const current = isCurrent(countryCode);
        
        let status = 'Not Visited';
        if (current) status = 'Currently Here';
        else if (visited) status = 'Visited';
        
        tooltip.textContent = `${countryName} - ${status}`;
        tooltip.style.display = 'block';
      });
      
      path.addEventListener('mousemove', (e) => {
        const rect = this.getBoundingClientRect();
        tooltip.style.left = (e.clientX - rect.left + 10) + 'px';
        tooltip.style.top = (e.clientY - rect.top + 10) + 'px';
      });
      
      path.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
      });
    });
  }
}

customElements.define('been-map-card', BeenMapCard);

// For HACS
console.info('Been Map Card loaded');
