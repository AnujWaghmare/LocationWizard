"""
Core module for Location-Based Wind and Seismic Zone Wizard
Implements get_location_properties function using SoI shapefiles
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os
import json
from typing import Dict, Optional

# Global variables for cached data
_seismic_gdf = None
_wind_gdf = None
_admin_gdf = None
_zone_factors = None

def load_zone_factors():
    """Load seismic zone factors from IS 1893"""
    global _zone_factors
    if _zone_factors is None:
        _zone_factors = {
            "II": 0.10,
            "III": 0.16,
            "IV": 0.24,
            "V": 0.36
        }
    return _zone_factors

def load_shapefiles():
    """Load SoI shapefiles with caching"""
    global _seismic_gdf, _wind_gdf, _admin_gdf
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load seismic zones (digitized from IS 1893)
    seismic_file = os.path.join(data_dir, 'seismic_zones.geojson')
    if _seismic_gdf is None and os.path.exists(seismic_file):
        _seismic_gdf = gpd.read_file(seismic_file)
        if _seismic_gdf.crs != 'EPSG:4326':
            _seismic_gdf = _seismic_gdf.to_crs('EPSG:4326')
    
    # Load wind zones (digitized from IS 875)
    wind_file = os.path.join(data_dir, 'wind_zones.geojson')
    if _wind_gdf is None and os.path.exists(wind_file):
        _wind_gdf = gpd.read_file(wind_file)
        if _wind_gdf.crs != 'EPSG:4326':
            _wind_gdf = _wind_gdf.to_crs('EPSG:4326')
    
    # Load administrative boundaries (SoI data)
    admin_file = os.path.join(data_dir, 'admin_boundaries.geojson')
    if _admin_gdf is None and os.path.exists(admin_file):
        _admin_gdf = gpd.read_file(admin_file)
        if _admin_gdf.crs != 'EPSG:4326':
            _admin_gdf = _admin_gdf.to_crs('EPSG:4326')

def get_location_properties(lat: float, lon: float) -> Dict:
    """
    Get seismic and wind zone properties for a given location
    
    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
    
    Returns:
        Dictionary with location properties including seismic zone and wind speed
    """
    load_shapefiles()
    load_zone_factors()
    
    # Create point geometry
    point = Point(lon, lat)
    
    # Initialize result
    result = {
        "lat": lat,
        "lon": lon,
        "seismic_zone": "Unknown",
        "zone_factor": None,
        "basic_wind_speed": None,
        "place_name": "Unknown",
        "state": "Unknown"
    }
    
    # Check seismic zone
    if _seismic_gdf is not None:
        seismic_match = _seismic_gdf[_seismic_gdf.geometry.contains(point)]
        if not seismic_match.empty:
            zone = seismic_match.iloc[0]['zone']
            result["seismic_zone"] = zone
            result["zone_factor"] = _zone_factors.get(zone)
    
    # Check wind zone
    if _wind_gdf is not None:
        wind_match = _wind_gdf[_wind_gdf.geometry.contains(point)]
        if not wind_match.empty:
            result["basic_wind_speed"] = float(wind_match.iloc[0]['Vb'])
    
    # Check administrative boundaries
    if _admin_gdf is not None:
        admin_match = _admin_gdf[_admin_gdf.geometry.contains(point)]
        if not admin_match.empty:
            result["place_name"] = admin_match.iloc[0].get('NAME', 'Unknown')
            result["state"] = admin_match.iloc[0].get('STATE', 'Unknown')
    
    return result

def search_location(query: str) -> Optional[Dict]:
    """Search for location by address or coordinates"""
    try:
        import requests
        
        # Check if coordinates
        if ',' in query:
            try:
                lat, lon = map(float, query.split(','))
                if 6.0 <= lat <= 37.0 and 68.0 <= lon <= 97.0:
                    return {'lat': lat, 'lon': lon, 'display_name': f"Coordinates: {lat:.6f}, {lon:.6f}"}
            except ValueError:
                pass
        
        # Search by address
        response = requests.get("https://nominatim.openstreetmap.org/search", {
            'q': query + ', India', 'format': 'json', 'limit': 1, 'countrycodes': 'in'
        }, headers={'User-Agent': 'LocationWizard/1.0'}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                result = data[0]
                return {'lat': float(result['lat']), 'lon': float(result['lon']), 'display_name': result.get('display_name', query)}
    except Exception:
        pass
    return None

def get_reverse_geocoding(lat: float, lon: float) -> Optional[str]:
    """
    Optional reverse geocoding using Nominatim (FOSS service)
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        Place name or None if service unavailable
    """
    try:
        import requests
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'addressdetails': 1
        }
        headers = {'User-Agent': 'LocationWizard/1.0'}
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', 'Unknown')
    except Exception:
        pass
    
    return None

def get_nearby_cities(lat: float, lon: float, radius_km: float = 50) -> list:
    """Get nearby major cities within specified radius"""
    import math
    cities = {
        "Delhi": {"lat": 28.6139, "lon": 77.2090}, "Mumbai": {"lat": 19.0760, "lon": 72.8777},
        "Chennai": {"lat": 13.0827, "lon": 80.2707}, "Kolkata": {"lat": 22.5726, "lon": 88.3639},
        "Bangalore": {"lat": 12.9716, "lon": 77.5946}, "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
        "Pune": {"lat": 18.5204, "lon": 73.8567}, "Ahmedabad": {"lat": 23.0225, "lon": 72.5714}
    }
    
    nearby = []
    for city, coords in cities.items():
        lat1, lon1 = math.radians(lat), math.radians(lon)
        lat2, lon2 = math.radians(coords['lat']), math.radians(coords['lon'])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        distance = 6371 * 2 * math.asin(math.sqrt(a))
        
        if distance <= radius_km:
            nearby.append({'city': city, 'distance': round(distance, 1), 'lat': coords['lat'], 'lon': coords['lon']})
    
    return sorted(nearby, key=lambda x: x['distance'])

def get_search_suggestions(query: str) -> list:
    """Get search suggestions for autocomplete"""
    suggestions = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
    if not query:
        return suggestions[:5]
    return [city for city in suggestions if query.lower() in city.lower()][:5]