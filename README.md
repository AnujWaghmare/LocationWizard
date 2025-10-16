# Location-Based Wind and Seismic Zone Wizard for OsdagBridge

A FOSS-based interactive application for determining seismic zones and wind speeds at any location in India using Survey of India (SoI) shapefiles and ISRO/NRSC satellite data.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/AnujWaghmare/LocationWizard.git
cd LocationWizard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

## 📋 Features

- **Interactive Map**: Click anywhere on India map to get zone information
- **Seismic Zones**: IS 1893 compliant seismic zone identification (II-V)
- **Wind Speeds**: IS 875 basic wind speed values (Vb in m/s)
- **Zone Factors**: Automatic calculation of seismic zone factors (Z)
- **Administrative Info**: State and place name identification
- **NavIC Ready**: Integration notes for NavIC positioning system
- **FOSS Stack**: 100% Free and Open Source Software

## 🗺️ Data Sources

### Primary Sources (Mandatory)
- **Survey of India (SoI)**: Administrative boundaries and topographic data
- **ISRO/NRSC**: Satellite imagery from Bhuvan, MOSDAC, VEDAS portals

### Reference Standards
- **IS 1893**: Seismic zone classifications
- **IS 875**: Wind load calculations and basic wind speeds

## 🛠️ Technology Stack

- **Backend**: Python 3.9+, GeoPandas, Shapely, Fiona
- **Frontend**: Streamlit, Folium (Leaflet)
- **Spatial**: GDAL/OGR, PyProj, RTree
- **Testing**: Pytest
- **Data**: GeoJSON, Survey of India shapefiles

## 📁 Project Structure

```
LocationWizard/
├── streamlit_app.py      # Main Streamlit application
├── core.py              # Core location properties function
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── data/               # Spatial data files
│   ├── seismic_zones.geojson
│   ├── wind_zones.geojson
│   ├── admin_boundaries.geojson
│   ├── provenance.md   # Data source documentation
│   └── fetch_soi.sh    # SoI data acquisition script
└── tests/              # Unit tests
    └── test_location_properties.py
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_location_properties.py -v

# Test coverage
pytest --cov=core tests/
```

## 📊 API Usage

```python
from core import get_location_properties

# Get properties for Delhi
result = get_location_properties(28.6139, 77.2090)
print(result)
# Output:
# {
#   'lat': 28.6139,
#   'lon': 77.2090,
#   'seismic_zone': 'IV',
#   'zone_factor': 0.24,
#   'basic_wind_speed': 44.0,
#   'place_name': 'Delhi',
#   'state': 'Delhi'
# }
```

## 🛰️ NavIC Integration

This application is designed to work with NavIC (Navigation with Indian Constellation) for enhanced positioning accuracy:

### NavIC Advantages
- **Coverage**: Indian subcontinent + 1500km extension
- **Accuracy**: 1-5 meters (better than GPS in India)
- **Reliability**: Indigenous satellite constellation

### Integration Steps
1. Use NavIC-enabled GNSS receiver or smartphone
2. Capture coordinates with NavIC precision
3. Input coordinates into Location Wizard
4. Get accurate zone information for the location

### Compatible Hardware
- NavIC-enabled smartphones (select models)
- Professional GNSS receivers with NavIC support
- Survey equipment with multi-constellation capability

## 📋 Data Compliance

### Survey of India (SoI) Compliance
- All vector data sourced from official SoI digital products
- Product IDs and download dates documented in `data/provenance.md`
- Non-sensitive data classification verified
- Open Government Data License compliance

### ISRO/NRSC Compliance
- Satellite imagery from official ISRO portals only
- Dataset names and acquisition dates documented
- Creative Commons Attribution licensing followed

## 🔧 Development

### Adding New Data Sources
1. Ensure data is from SoI or ISRO/NRSC portals
2. Document source in `data/provenance.md`
3. Convert to GeoJSON format with WGS84 projection
4. Update `core.py` to load new data
5. Add corresponding unit tests

### Extending Functionality
- Add new zone types (cyclone, flood, etc.)
- Implement micro-zonation support
- Add terrain-adjusted wind speeds
- Include soil classification data

## 📖 References

- **IS 1893 (Part 1): 2016** - Criteria for Earthquake Resistant Design
- **IS 875 (Part 3): 2015** - Wind Loads on Buildings and Structures
- **Survey of India**: https://onlinemaps.surveyofindia.gov.in/
- **Bhuvan Portal**: https://bhuvan.nrsc.gov.in/
- **NavIC System**: https://www.isro.gov.in/navic-programme


## 🔄 Version History

- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Added NavIC integration notes
- **v1.2.0**: Enhanced data provenance documentation
- **v1.3.0**: Improved test coverage and validation
