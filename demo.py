"""
Demo script for Location Wizard
Tests core functionality with sample coordinates
"""

from core import get_location_properties
import json

def demo_locations():
    """Test the location wizard with known coordinates"""
    
    print("🌍 Location-Based Wind & Seismic Zone Wizard Demo")
    print("=" * 50)
    
    # Test locations with known properties
    test_locations = [
        {"name": "Delhi", "lat": 28.6139, "lon": 77.2090},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
        {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
        {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
        {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946}
    ]
    
    for location in test_locations:
        print(f"\n Testing: {location['name']}")
        print(f"   Coordinates: {location['lat']:.4f}°N, {location['lon']:.4f}°E")
        
        try:
            # Get location properties
            result = get_location_properties(location['lat'], location['lon'])
            
            # Display results
            print(f"   🏗  Seismic Zone: {result['seismic_zone']}")
            if result['zone_factor']:
                print(f"   🌍 Zone Factor (Z): {result['zone_factor']}")
            
            if result['basic_wind_speed']:
                print(f"   💨 Wind Speed (Vb): {result['basic_wind_speed']} m/s")
            else:
                print(f"   💨 Wind Speed: Not available")
            
            if result['place_name'] != 'Unknown':
                print(f"   🏛  Place: {result['place_name']}")
            
            if result['state'] != 'Unknown':
                print(f"   🗺  State: {result['state']}")
                
        except Exception as e:
            print(f"    Error: {e}")
    
    print("\n" + "=" * 50)
    print(" Demo completed!")
    print(" Run 'streamlit run streamlit_app.py' for interactive map")

def test_api_format():
    """Test API response format"""
    print("\n API Format Test")
    print("-" * 30)
    
    # Test with Delhi coordinates
    result = get_location_properties(28.6139, 77.2090)
    
    print(" API Response Format:")
    print(json.dumps(result, indent=2))
    
    # Validate required fields
    required_fields = ['lat', 'lon', 'seismic_zone', 'basic_wind_speed']
    missing_fields = [field for field in required_fields if field not in result]
    
    if missing_fields:
        print(f" Missing required fields: {missing_fields}")
    else:
        print(" All required fields present")

if __name__ == "__main__":
    demo_locations()
    test_api_format()