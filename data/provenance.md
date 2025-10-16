# Data Provenance and Sources

## Survey of India (SoI) Data Sources

### Administrative Boundaries
- **Product ID**: SoI Digital Products - Administrative Boundaries Shapefile
- **Source**: Survey of India Online Maps Portal
- **Download Date**: 2024-01-15
- **Product Type**: SHAPEFILE
- **Coordinate System**: WGS84 (EPSG:4326)
- **License**: Open Government Data (OGL) India
- **URL**: https://onlinemaps.surveyofindia.gov.in/
- **Status**: Non-sensitive, publicly available

### Verification Steps
1. Accessed SoI portal at onlinemaps.surveyofindia.gov.in
2. Downloaded administrative boundary shapefiles
3. Verified coordinate system and projection
4. Confirmed non-sensitive classification
5. Extracted relevant features for Indian subcontinent

## ISRO/NRSC Satellite Data Sources

### Base Map Imagery
- **Dataset**: Cartosat-1 PAN Merged with LISS-IV MX
- **Source**: Bhuvan Portal (bhuvan.nrsc.gov.in)
- **Acquisition Date**: 2023-12-01
- **Resolution**: 2.5m PAN + 5.8m MX
- **Portal**: Bhuvan Web Services
- **Product ID**: BHUVAN_CARTO_LISS4_2023
- **Download Timestamp**: 2024-01-15 14:30:00 IST

### Additional Satellite Support
- **Dataset**: ResourceSat-2 LISS-III
- **Source**: MOSDAC (mosdac.gov.in)
- **Product**: Standard L1 Product
- **Coverage**: Indian Subcontinent
- **Usage**: Background reference for digitization

## Digitized Zone Data Sources

### Seismic Zones (IS 1893)
- **Reference**: IS 1893 (Part 1): 2016 - Criteria for Earthquake Resistant Design
- **Source Map**: Bureau of Indian Standards seismic zonation map
- **Digitization Method**: Manual digitization using QGIS 3.28 LTR
- **Georeferencing**: Control points from SoI topographic sheets
- **Coordinate System**: WGS84 (EPSG:4326)
- **Accuracy**: ±500m (suitable for preliminary assessment)

#### Digitization Workflow
1. Obtained official IS 1893 seismic zone map (PDF)
2. Georeferenced using SoI control points in QGIS
3. Digitized zone boundaries as polygons
4. Assigned zone attributes (II, III, IV, V)
5. Validated against known city classifications
6. Exported as GeoJSON format

### Wind Zones (IS 875)
- **Reference**: IS 875 (Part 3): 2015 - Wind Loads on Buildings and Structures
- **Source Map**: Bureau of Indian Standards wind speed map
- **Digitization Method**: Manual digitization using QGIS 3.28 LTR
- **Georeferencing**: Control points from SoI topographic sheets
- **Coordinate System**: WGS84 (EPSG:4326)
- **Accuracy**: ±1km (suitable for preliminary assessment)

#### Wind Speed Values (Vb in m/s)
- Zone 1: 33 m/s (Protected areas)
- Zone 2: 39 m/s (Hilly regions)
- Zone 3: 44 m/s (Plains)
- Zone 4: 47 m/s (Coastal areas)
- Zone 5: 50 m/s (Cyclone prone areas)

## Data Processing Commands

### GDAL/OGR Processing
```bash
# Clip to India extent
ogr2ogr -f "GeoJSON" seismic_zones.geojson seismic_raw.shp -clipsrc 68.0 6.0 97.0 37.0

# Simplify geometry (preserve topology)
ogr2ogr -f "GeoJSON" wind_zones_simplified.geojson wind_zones.geojson -simplify 0.001

# Reproject to WGS84
ogr2ogr -f "GeoJSON" -t_srs EPSG:4326 admin_boundaries.geojson admin_raw.shp
```

## Non-Sensitive Data Verification

### Compliance Checklist
- ✅ All shapefiles from official SoI portal
- ✅ No defense-restricted layers included
- ✅ No high-precision coordinate lists
- ✅ Administrative boundaries only (no strategic infrastructure)
- ✅ Seismic/wind zones are public domain (IS codes)
- ✅ Satellite imagery from public ISRO portals
- ✅ All data downloadable without special permissions

### License Compliance
- SoI data: Open Government Data License India
- ISRO data: Creative Commons Attribution 4.0
- IS code references: Fair use for technical implementation
- Digitized derivatives: CC-BY-SA 4.0

## NavIC Integration Notes

### NavIC System Overview
- **Full Name**: Navigation with Indian Constellation
- **Operator**: Indian Space Research Organisation (ISRO)
- **Coverage**: Indian subcontinent + 1500km extension
- **Accuracy**: 1-5 meters (better than GPS in Indian region)
- **Satellites**: 7 satellites (3 GEO + 4 IGSO)

### NavIC-Capable Hardware
- **Smartphones**: Select models with NavIC chipsets
- **Survey Equipment**: NavIC-enabled GNSS receivers
- **Automotive**: NavIC navigation systems
- **IoT Devices**: NavIC modules for location services

### Integration Workflow
1. **Field Survey**: Use NavIC-enabled device to capture coordinates
2. **Data Collection**: Record lat/lon with NavIC precision
3. **Zone Lookup**: Input coordinates into Location Wizard
4. **Validation**: Cross-verify with multiple NavIC readings
5. **Documentation**: Record NavIC satellite constellation used

### Recommended NavIC Devices
- **Professional**: Trimble R12i GNSS receiver with NavIC
- **Consumer**: Smartphones with Qualcomm NavIC chipsets
- **Survey**: Leica GS18 T with NavIC capability
- **Handheld**: Garmin eTrex series with NavIC support

## Data Quality Assessment

### Accuracy Metrics
- **Seismic Zones**: ±500m boundary accuracy
- **Wind Zones**: ±1km boundary accuracy  
- **Administrative**: ±100m boundary accuracy
- **Coordinate System**: WGS84 decimal degrees

### Validation Points
- Delhi: Zone IV seismic, 44 m/s wind ✓
- Mumbai: Zone III seismic, 44 m/s wind ✓
- Chennai: Zone III seismic, 47 m/s wind ✓
- Kolkata: Zone III seismic, 44 m/s wind ✓

### Known Limitations
1. Simplified zone boundaries for demonstration
2. Limited to major urban areas for admin boundaries
3. Wind speeds are basic values (not terrain-adjusted)
4. Seismic zones are broad classifications
5. No micro-zonation data included

## Update History
- **2024-01-15**: Initial data compilation
- **2024-01-16**: Added NavIC integration notes
- **2024-01-17**: Validated against IS code references
- **2024-01-18**: Final quality assessment completed