# Location-Based Wind and Seismic Zone Wizard for OsdagBridge
## Project Report

---

## Project Title
**Location-Based Wind and Seismic Zone Wizard for OsdagBridge**

---

## Area / Domain of Project
**Civil Engineering & Geospatial Technology**
- Structural Engineering Design
- Seismic Risk Assessment
- Wind Load Analysis
- Geographic Information Systems (GIS)
- Building Code Compliance (IS 1893, IS 875)

---

## Introduction
The Location-Based Wind and Seismic Zone Wizard is a FOSS-based interactive application designed to provide instant access to seismic zone classifications and basic wind speed data for any location in India. Built specifically for OsdagBridge, this tool enables structural engineers to quickly determine critical design parameters required for earthquake-resistant and wind-resistant design as per Indian Standards.

The application utilizes Survey of India (SoI) shapefiles and ISRO/NRSC satellite data to provide accurate zone information through an intuitive web-based interface. Users can simply click on an interactive map to retrieve seismic zone classifications (IS 1893), basic wind speeds (IS 875), zone factors, and administrative details.

---

## Motivation
- **Design Efficiency**: Eliminate manual lookup of seismic and wind zones from printed maps
- **Accuracy**: Reduce human errors in zone identification for structural design
- **Compliance**: Ensure adherence to IS 1893 and IS 875 standards
- **Accessibility**: Provide instant access to critical design data anywhere
- **Indigenous Technology**: Promote use of Indian data sources (SoI, ISRO) and NavIC positioning
- **FOSS Advocacy**: Demonstrate capabilities of Free and Open Source Software in engineering applications

---

## Problem Statement
Structural engineers designing buildings and bridges in India face several challenges:

1. **Manual Zone Lookup**: Traditional methods require consulting printed maps and tables
2. **Data Accuracy**: Risk of misreading zone boundaries from paper maps
3. **Time Consumption**: Lengthy process to determine zones for multiple locations
4. **Accessibility**: Limited access to updated seismic and wind zone data
5. **Integration**: Difficulty integrating zone data with modern design workflows
6. **Compliance**: Ensuring correct application of IS 1893 and IS 875 standards

**Primary Objective**: Develop a digital tool that provides instant, accurate seismic and wind zone information for any location in India using official government data sources.

---

## Proposed Work
The project delivers a comprehensive solution comprising:

### Core Functionality
- Interactive map-based interface for location selection
- Point-in-polygon analysis for zone determination
- Real-time lookup of seismic zones (II, III, IV, V)
- Basic wind speed retrieval (Vb values)
- Zone factor calculation as per IS 1893
- Administrative boundary identification

### Technical Implementation
- Web-based application using Streamlit framework
- Spatial data processing with GeoPandas and Shapely
- Interactive mapping with Folium (Leaflet)
- RESTful API for programmatic access
- Comprehensive unit testing with pytest

### Data Integration
- Survey of India (SoI) official shapefiles
- ISRO/NRSC satellite imagery for reference
- Digitized IS 1893 seismic zone boundaries
- Digitized IS 875 wind speed regions
- NavIC positioning system integration framework

---

## Modules

### 1. Core Processing Module (`core.py`)
- **Function**: `get_location_properties(lat, lon)`
- **Purpose**: Main API for zone lookup
- **Features**: Spatial analysis, zone factor calculation, caching

### 2. Web Interface Module (`streamlit_app.py`)
- **Function**: Interactive web application
- **Purpose**: User interface for map-based interaction
- **Features**: Click-to-query, real-time results, data export

### 3. Data Management Module (`data/`)
- **Function**: Spatial data storage and metadata
- **Purpose**: Zone boundaries and administrative data
- **Features**: GeoJSON format, provenance documentation

### 4. Testing Module (`tests/`)
- **Function**: Unit tests and validation
- **Purpose**: Ensure accuracy and reliability
- **Features**: Known location testing, API validation

### 5. Utility Module (`demo.py`, `standalone_demo.py`)
- **Function**: Testing and demonstration
- **Purpose**: Validate functionality without web interface
- **Features**: Command-line testing, interactive mode

---

## Development Environment

### Programming Language
- **Python 3.9+**: Primary development language

### Development Tools
- **IDE**: Visual Studio Code / PyCharm
- **Version Control**: Git
- **Package Management**: pip, virtual environments
- **Testing Framework**: pytest
- **Documentation**: Markdown

### Spatial Processing Tools
- **QGIS 3.28 LTR**: Map digitization and georeferencing
- **GDAL/OGR**: Command-line spatial data processing
- **GeoPandas**: Python spatial data manipulation
- **Shapely**: Geometric operations

---

## Software Requirements

### Core Dependencies
```
streamlit>=1.28.0          # Web application framework
folium>=0.14.0             # Interactive mapping
streamlit-folium>=0.15.0   # Streamlit-Folium integration
geopandas>=0.14.0          # Spatial data processing
shapely>=2.0.0             # Geometric operations
fiona>=1.9.0               # Shapefile I/O
pyproj>=3.6.0              # Coordinate transformations
rtree>=1.0.0               # Spatial indexing
pytest>=7.4.0             # Unit testing
requests>=2.31.0           # HTTP requests
```

### System Requirements
- **Operating System**: Windows 10/11, Linux, macOS
- **Python Version**: 3.9 or higher
- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Storage**: 500MB for application and data
- **Network**: Internet connection for map tiles and reverse geocoding

### Optional Dependencies
- **GDAL**: Advanced spatial data processing
- **Rasterio**: Satellite imagery processing
- **Jupyter**: Interactive development and analysis

---

## Hardware Requirements

### Minimum Configuration
- **Processor**: Intel i3 / AMD equivalent
- **RAM**: 2GB
- **Storage**: 1GB available space
- **Network**: Broadband internet connection
- **Display**: 1024x768 resolution

### Recommended Configuration
- **Processor**: Intel i5 / AMD Ryzen 5 or higher
- **RAM**: 4GB or higher
- **Storage**: 2GB available space (SSD preferred)
- **Network**: High-speed internet for optimal performance
- **Display**: 1920x1080 resolution or higher

### NavIC-Compatible Hardware (Optional)
- **GNSS Receivers**: NavIC-enabled survey equipment
- **Smartphones**: NavIC-capable devices with Indian chipsets
- **Survey Tools**: Multi-constellation GNSS receivers

---

## Deployment Environment

### Local Development
```bash
# Setup virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run streamlit_app.py
```

### Web Deployment Options
- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Cloud platform deployment
- **AWS/Azure**: Enterprise cloud deployment
- **Docker**: Containerized deployment

### Production Considerations
- **Load Balancing**: Multiple application instances
- **Caching**: Redis for spatial query caching
- **Database**: PostGIS for large-scale spatial data
- **CDN**: Content delivery for map tiles
- **SSL**: HTTPS encryption for security

---

## References

### Indian Standards
1. **IS 1893 (Part 1): 2016** - Criteria for Earthquake Resistant Design of Structures, Bureau of Indian Standards
2. **IS 875 (Part 3): 2015** - Code of Practice for Design Loads (Other than Earthquake) for Buildings and Structures - Wind Loads, Bureau of Indian Standards
3. **IS 456: 2000** - Plain and Reinforced Concrete - Code of Practice, Bureau of Indian Standards

### Technical Publications
4. **Seismic Zonation Map of India**, Geological Survey of India, 2016
5. **Wind Speed Map of India**, India Meteorological Department, 2015
6. **NavIC System Overview**, Indian Space Research Organisation, 2023

### Software Documentation
7. **GeoPandas Documentation**, https://geopandas.org/
8. **Streamlit Documentation**, https://docs.streamlit.io/
9. **Folium Documentation**, https://python-visualization.github.io/folium/

---

## Web References

### Official Government Portals
1. **Survey of India Digital Products**: https://onlinemaps.surveyofindia.gov.in/
2. **Bhuvan - ISRO Geoportal**: https://bhuvan.nrsc.gov.in/
3. **MOSDAC - ISRO**: https://mosdac.gov.in/
4. **Bhoonidhi - NRSC**: https://bhoonidhi.nrsc.gov.in/
5. **VEDAS - ISRO SAC**: https://vedas.sac.gov.in/

### Technical Resources
6. **Bureau of Indian Standards**: https://www.bis.gov.in/
7. **National Centre for Seismology**: https://seismo.gov.in/
8. **India Meteorological Department**: https://mausam.imd.gov.in/
9. **NavIC Programme - ISRO**: https://www.isro.gov.in/navic-programme

### Open Source Libraries
10. **GDAL/OGR**: https://gdal.org/
11. **OpenStreetMap**: https://www.openstreetmap.org/
12. **Natural Earth Data**: https://www.naturalearthdata.com/
13. **Nominatim Geocoding**: https://nominatim.org/

### Development Resources
14. **Python.org**: https://www.python.org/
15. **GitHub**: https://github.com/
16. **Stack Overflow**: https://stackoverflow.com/
17. **QGIS**: https://qgis.org/

---

**Project Completion Date**: January 2024  
**Version**: 1.0.0  
**License**: MIT License (Code), Open Government Data License India (Data)  
**Compliance**: FOSS-only implementation, SoI/ISRO data sources, IS standards adherence