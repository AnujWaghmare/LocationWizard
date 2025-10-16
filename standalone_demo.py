"""
Standalone demo for Location Wizard - No external dependencies
Uses only Python standard library
"""

import json
import os

def point_in_polygon_simple(lat, lon, polygon_coords):
    """
    Simple point-in-polygon test using ray casting algorithm
    polygon_coords: list of [lon, lat] coordinate pairs
    """
    x, y = lon, lat
    n = len(polygon_coords)
    inside = False
    
    p1x, p1y = polygon_coords[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def load_zone_data():
    """Load zone data from JSON files"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load seismic zones
    seismic_file = os.path.join(data_dir, 'seismic_zones.geojson')
    seismic_data = None
    if os.path.exists(seismic_file):
        with open(seismic_file, 'r') as f:
            seismic_data = json.load(f)
    
    # Load wind zones
    wind_file = os.path.join(data_dir, 'wind_zones.geojson')
    wind_data = None
    if os.path.exists(wind_file):
        with open(wind_file, 'r') as f:
            wind_data = json.load(f)
    
    return seismic_data, wind_data

def get_location_properties_standalone(lat, lon):
    """
    Get location properties using only standard library
    """
    seismic_data, wind_data = load_zone_data()
    
    # Zone factors from IS 1893
    zone_factors = {
        "II": 0.10,
        "III": 0.16,
        "IV": 0.24,
        "V": 0.36
    }
    
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
    
    # Check seismic zones
    if seismic_data:
        for feature in seismic_data.get('features', []):
            geometry = feature.get('geometry', {})
            if geometry.get('type') == 'Polygon':
                coords = geometry.get('coordinates', [[]])[0]  # Get exterior ring
                if point_in_polygon_simple(lat, lon, coords):
                    zone = feature.get('properties', {}).get('zone', 'Unknown')
                    result["seismic_zone"] = zone
                    result["zone_factor"] = zone_factors.get(zone)
                    break
    
    # Check wind zones
    if wind_data:
        for feature in wind_data.get('features', []):
            geometry = feature.get('geometry', {})
            if geometry.get('type') == 'Polygon':
                coords = geometry.get('coordinates', [[]])[0]  # Get exterior ring
                if point_in_polygon_simple(lat, lon, coords):
                    wind_speed = feature.get('properties', {}).get('Vb')
                    if wind_speed:
                        result["basic_wind_speed"] = float(wind_speed)
                    break
    
    # Simple place name lookup for major cities
    major_cities = {
        "Delhi": {"lat_range": (28.4, 28.9), "lon_range": (76.8, 77.3), "state": "Delhi"},
        "Mumbai": {"lat_range": (18.9, 19.3), "lon_range": (72.7, 73.0), "state": "Maharashtra"},
        "Chennai": {"lat_range": (12.9, 13.2), "lon_range": (80.1, 80.4), "state": "Tamil Nadu"},
        "Kolkata": {"lat_range": (22.4, 22.7), "lon_range": (88.2, 88.5), "state": "West Bengal"},
        "Bangalore": {"lat_range": (12.8, 13.1), "lon_range": (77.4, 77.8), "state": "Karnataka"}
    }
    
    for city, bounds in major_cities.items():
        lat_min, lat_max = bounds["lat_range"]
        lon_min, lon_max = bounds["lon_range"]
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            result["place_name"] = city
            result["state"] = bounds["state"]
            break
    
    return result

def demo_locations():
    """Test the location wizard with known coordinates"""
    
    print("🌍 Location-Based Wind & Seismic Zone Wizard Demo")
    print("=" * 50)
    print("📋 Standalone Version - No External Dependencies")
    print()
    
    # Test locations with known properties
    test_locations = [
        {"name": "Delhi", "lat": 28.6139, "lon": 77.2090},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
        {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
        {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
        {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946}
    ]
    
    for location in test_locations:
        print(f" Testing: {location['name']}")
        print(f"   Coordinates: {location['lat']:.4f}°N, {location['lon']:.4f}°E")
        
        try:
            # Get location properties
            result = get_location_properties_standalone(location['lat'], location['lon'])
            
            # Display results
            print(f"   🏗️  Seismic Zone: {result['seismic_zone']}")
            if result['zone_factor']:
                print(f"   📊 Zone Factor (Z): {result['zone_factor']}")
            
            if result['basic_wind_speed']:
                print(f"   💨 Wind Speed (Vb): {result['basic_wind_speed']} m/s")
            else:
                print(f"   💨 Wind Speed: Not available")
            
            if result['place_name'] != 'Unknown':
                print(f"   🏛️  Place: {result['place_name']}")
            
            if result['state'] != 'Unknown':
                print(f"   🗺️  State: {result['state']}")
                
        except Exception as e:
            print(f"    Error: {e}")
        
        print()
    
    print("=" * 50)
    print(" Demo completed!")
    print()
    print(" API Response Example (Delhi):")
    delhi_result = get_location_properties_standalone(28.6139, 77.2090)
    print(json.dumps(delhi_result, indent=2))
    
    print()
    print(" Next Steps:")
    print("1. Install Streamlit: pip install streamlit folium streamlit-folium")
    print("2. Run web app: streamlit run streamlit_app_simple.py")
    print("3. Or use this standalone version for testing")

def interactive_test():
    """Interactive coordinate testing"""
    print("\n Interactive Testing Mode")
    print("Enter coordinates to test (or 'quit' to exit)")
    
    while True:
        try:
            user_input = input("\nEnter lat,lon (e.g., 28.6139,77.2090): ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            lat_str, lon_str = user_input.split(',')
            lat, lon = float(lat_str.strip()), float(lon_str.strip())
            
            result = get_location_properties_standalone(lat, lon)
            print(f"\n Results for {lat:.4f}°N, {lon:.4f}°E:")
            print(f"   Seismic Zone: {result['seismic_zone']}")
            print(f"   Zone Factor: {result['zone_factor']}")
            print(f"   Wind Speed: {result['basic_wind_speed']} m/s" if result['basic_wind_speed'] else "   Wind Speed: Not available")
            print(f"   Location: {result['place_name']}, {result['state']}")
            
        except ValueError:
            print("❌ Invalid format. Use: lat,lon (e.g., 28.6139,77.2090)")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n Goodbye!")

if __name__ == "__main__":
    demo_locations()
    
    # Ask if user wants interactive mode
    try:
        response = input("\n Want to test custom coordinates? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_test()
    except KeyboardInterrupt:
        print("\n Goodbye!")