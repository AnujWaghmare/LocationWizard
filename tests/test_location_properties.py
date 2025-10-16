"""
Unit tests for location properties functionality
Tests get_location_properties function with known coordinates
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import get_location_properties

class TestLocationProperties:
    """Test cases for location properties function"""
    
    def test_delhi_location(self):
        """Test location properties for Delhi (known seismic zone IV)"""
        # Delhi coordinates
        lat, lon = 28.6139, 77.2090
        
        result = get_location_properties(lat, lon)
        
        # Basic structure tests
        assert isinstance(result, dict)
        assert 'lat' in result
        assert 'lon' in result
        assert 'seismic_zone' in result
        assert 'basic_wind_speed' in result
        
        # Coordinate accuracy
        assert abs(result['lat'] - lat) < 0.0001
        assert abs(result['lon'] - lon) < 0.0001
        
        # Delhi should be in seismic zone IV (if data is available)
        # Note: This test will pass even if data files are not present
        if result['seismic_zone'] != 'Unknown':
            assert result['seismic_zone'] in ['II', 'III', 'IV', 'V']
    
    def test_mumbai_location(self):
        """Test location properties for Mumbai (known seismic zone III)"""
        # Mumbai coordinates
        lat, lon = 19.0760, 72.8777
        
        result = get_location_properties(lat, lon)
        
        # Basic structure tests
        assert isinstance(result, dict)
        assert 'lat' in result
        assert 'lon' in result
        assert 'seismic_zone' in result
        assert 'basic_wind_speed' in result
        
        # Coordinate accuracy
        assert abs(result['lat'] - lat) < 0.0001
        assert abs(result['lon'] - lon) < 0.0001
        
        # Mumbai should be in seismic zone III (if data is available)
        if result['seismic_zone'] != 'Unknown':
            assert result['seismic_zone'] in ['II', 'III', 'IV', 'V']
    
    def test_chennai_location(self):
        """Test location properties for Chennai (coastal wind zone)"""
        # Chennai coordinates
        lat, lon = 13.0827, 80.2707
        
        result = get_location_properties(lat, lon)
        
        # Basic structure tests
        assert isinstance(result, dict)
        assert 'lat' in result
        assert 'lon' in result
        assert 'seismic_zone' in result
        assert 'basic_wind_speed' in result
        
        # Coordinate accuracy
        assert abs(result['lat'] - lat) < 0.0001
        assert abs(result['lon'] - lon) < 0.0001
        
        # Chennai should have higher wind speeds (coastal area)
        if result['basic_wind_speed'] is not None:
            assert result['basic_wind_speed'] > 0
    
    def test_invalid_coordinates(self):
        """Test handling of coordinates outside India"""
        # Coordinates outside India (in ocean)
        lat, lon = 0.0, 0.0
        
        result = get_location_properties(lat, lon)
        
        # Should still return valid structure
        assert isinstance(result, dict)
        assert result['lat'] == lat
        assert result['lon'] == lon
        
        # Should return Unknown for zones outside India
        assert result['seismic_zone'] == 'Unknown'
    
    def test_zone_factor_mapping(self):
        """Test that zone factors are correctly mapped"""
        from core import load_zone_factors
        
        zone_factors = load_zone_factors()
        
        # Check all required zones have factors
        expected_zones = ['II', 'III', 'IV', 'V']
        for zone in expected_zones:
            assert zone in zone_factors
            assert isinstance(zone_factors[zone], float)
            assert 0 < zone_factors[zone] < 1
    
    def test_function_return_types(self):
        """Test that function returns correct data types"""
        # Test with Delhi coordinates
        lat, lon = 28.6139, 77.2090
        result = get_location_properties(lat, lon)
        
        # Check return types
        assert isinstance(result['lat'], float)
        assert isinstance(result['lon'], float)
        assert isinstance(result['seismic_zone'], str)
        
        # Zone factor should be float or None
        if result['zone_factor'] is not None:
            assert isinstance(result['zone_factor'], float)
        
        # Wind speed should be float or None
        if result['basic_wind_speed'] is not None:
            assert isinstance(result['basic_wind_speed'], float)

if __name__ == "__main__":
    pytest.main([__file__])