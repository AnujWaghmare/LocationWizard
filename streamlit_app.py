"""
Enhanced Streamlit app for Location-Based Wind and Seismic Zone Wizard
Features: Search functionality, improved UI, interactive sidebar, nearby cities
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from core import get_location_properties, search_location, get_nearby_cities, get_reverse_geocoding, get_search_suggestions

# Page configuration
st.set_page_config(
    page_title="Location Wizard - OsdagBridge",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1f4e79, #2e8b57, #4169e1);
        color: white;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .search-container {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 2px solid #dee2e6;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #1f4e79;
    }
    .zone-high { 
        background: linear-gradient(135deg, #ff4444, #cc0000);
        color: white; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(255,68,68,0.3);
    }
    .zone-medium { 
        background: linear-gradient(135deg, #ff8800, #e67300);
        color: white; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(255,136,0,0.3);
    }
    .zone-low { 
        background: linear-gradient(135deg, #44aa44, #2d7d2d);
        color: white; 
        padding: 1rem; 
        border-radius: 10px; 
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(68,170,68,0.3);
    }
    .sidebar-section {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    .quick-city-btn {
        width: 100%;
        margin: 0.2rem 0;
        padding: 0.5rem;
        border-radius: 8px;
        border: none;
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        font-weight: bold;
    }
    .nearby-city {
        background: #e3f2fd;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        border-left: 3px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🌍 Location-Based Wind & Seismic Zone Wizard</h1>
    <h3>For OsdagBridge - Advanced Geospatial Analysis Tool</h3>
    <p>🔍 Search by address or coordinates | 🗺️ Interactive mapping | 📊 Real-time analysis</p>
</div>
""", unsafe_allow_html=True)

# Enhanced search functionality
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.markdown("### 🔍 Location Search & Navigation")

col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

with col1:
    search_query = st.text_input(
        "Search Location",
        placeholder="🏙️ Enter city name (e.g., 'Delhi') or coordinates (e.g., '28.6139, 77.2090')",
        help="Search by address, landmark, or coordinates (latitude, longitude)",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

with col3:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

with col4:
    my_location = st.button("📍 My Location", use_container_width=True, help="Center map on India")

# Search suggestions
if search_query:
    suggestions = get_search_suggestions(search_query)
    if suggestions:
        st.markdown("**💡 Suggestions:**")
        suggestion_cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            with suggestion_cols[i]:
                if st.button(suggestion, key=f"suggest_{suggestion}"):
                    st.session_state.search_query = suggestion
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced sidebar with multiple sections
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.header("🛠️ Control Panel")
    
    # Map customization
    st.subheader("🗺️ Map Settings")
    map_style = st.selectbox(
        "Map Style",
        ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark_Matter", "Stamen Terrain", "Stamen Toner"],
        help="Choose your preferred map visualization style"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        show_markers = st.checkbox("🏙️ City Markers", value=True)
        show_zones = st.checkbox("🌐 Zone Overlay", value=False)
    with col2:
        show_grid = st.checkbox("📐 Coordinate Grid", value=False)
        auto_zoom = st.checkbox("🔍 Auto Zoom", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis options
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("📊 Analysis Options")
    
    show_nearby = st.checkbox("🏙️ Show Nearby Cities", value=True)
    if show_nearby:
        nearby_radius = st.slider("Search Radius (km)", 10, 200, 50, 10)
    
    auto_geocode = st.checkbox("🌐 Auto Reverse Geocoding", value=True)
    show_risk_assessment = st.checkbox("⚠️ Risk Assessment", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick access to major cities
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("🏙️ Quick Access Cities")
    
    quick_cities = {
        "🏛️ Delhi (Capital)": (28.6139, 77.2090),
        "🏢 Mumbai (Financial)": (19.0760, 72.8777),
        "🌊 Chennai (Coastal)": (13.0827, 80.2707),
        "🎭 Kolkata (Cultural)": (22.5726, 88.3639),
        "💻 Bangalore (Tech)": (12.9716, 77.5946),
        "💎 Hyderabad (Pharma)": (17.3850, 78.4867),
        "🏭 Pune (Industrial)": (18.5204, 73.8567),
        "🌟 Ahmedabad (Textile)": (23.0225, 72.5714)
    }
    
    for city, coords in quick_cities.items():
        if st.button(city, key=f"quick_{city}", use_container_width=True):
            st.session_state.selected_location = coords
            st.session_state.search_performed = True
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Information and help
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("ℹ️ Information & Help")
    
    with st.expander("📋 Data Sources & Standards"):
        st.markdown("""
        **Official Data Sources:**
        - 🏛️ **Survey of India (SoI)** - Administrative boundaries
        - 🏗️ **IS 1893:2016** - Seismic zone classifications
        - 💨 **IS 875:2015** - Wind load specifications  
        - 🛰️ **ISRO/NRSC** - Satellite imagery & mapping
        
        **Zone Classifications:**
        - **Zone V:** Very High Damage Risk
        - **Zone IV:** High Damage Risk  
        - **Zone III:** Moderate Damage Risk
        - **Zone II:** Low Damage Risk
        """)
    
    with st.expander("🚀 Features & Capabilities"):
        st.markdown("""
        **Core Features:**
        - 🔍 **Smart Search** - Address & coordinate lookup
        - 🗺️ **Interactive Maps** - Multiple map styles
        - 📊 **Real-time Analysis** - Instant zone identification
        - 🏙️ **Nearby Cities** - Distance-based city finder
        - 📤 **Data Export** - Multiple export formats
        
        **Advanced Features:**
        - 🎯 **Precision Mapping** - High-accuracy coordinates
        - ⚠️ **Risk Assessment** - Automated risk classification
        - 🌐 **Geocoding** - Address-to-coordinate conversion
        """)
    
    with st.expander("🛰️ NavIC Integration"):
        st.markdown("""
        **NavIC System Benefits:**
        - 🎯 **High Accuracy:** 1-5 meter precision in India
        - 🇮🇳 **Indigenous Technology:** Indian satellite constellation
        - 🔒 **Enhanced Security:** Encrypted positioning signals
        - 🌐 **Regional Coverage:** Optimized for Indian subcontinent
        
        **Compatible Hardware:**
        - 📱 NavIC-enabled smartphones
        - 📡 Professional GNSS receivers
        - 🚗 Automotive navigation systems
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Handle search functionality
if search_button and search_query:
    with st.spinner("🔍 Searching location..."):
        search_result = search_location(search_query)
        if search_result:
            st.session_state.selected_location = (search_result['lat'], search_result['lon'])
            st.session_state.search_performed = True
            st.session_state.search_result = search_result
            st.success(f"✅ **Found:** {search_result['display_name']}")
        else:
            st.error("❌ **Location not found.** Try different keywords or check spelling.")

if clear_button:
    for key in ['selected_location', 'search_performed', 'search_result', 'location_props']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

if my_location:
    st.session_state.selected_location = [20.5937, 78.9629]  # Center of India
    st.info("📍 Map centered on India")

# Main content area with enhanced layout
col1, col2 = st.columns([2.2, 1.8])

with col1:
    st.subheader("🗺️ Interactive Geospatial Map")
    
    # Enhanced map creation
    map_center = st.session_state.get('selected_location', [20.5937, 78.9629])
    
    # Map style configuration
    tile_mapping = {
        "OpenStreetMap": "OpenStreetMap",
        "CartoDB Positron": "CartoDB positron", 
        "CartoDB Dark_Matter": "CartoDB dark_matter",
        "Stamen Terrain": "Stamen Terrain",
        "Stamen Toner": "Stamen Toner"
    }
    
    m = folium.Map(
        location=map_center,
        zoom_start=5 if 'selected_location' not in st.session_state else (10 if auto_zoom else 6),
        tiles=tile_mapping.get(map_style, "OpenStreetMap"),
        control_scale=True
    )
    
    # Add enhanced markers
    if show_markers:
        major_cities = {
            "Delhi": {"coords": [28.6139, 77.2090], "color": "red"},
            "Mumbai": {"coords": [19.0760, 72.8777], "color": "blue"},
            "Chennai": {"coords": [13.0827, 80.2707], "color": "green"},
            "Kolkata": {"coords": [22.5726, 88.3639], "color": "purple"},
            "Bangalore": {"coords": [12.9716, 77.5946], "color": "orange"},
            "Hyderabad": {"coords": [17.3850, 78.4867], "color": "darkred"}
        }
        
        for city, info in major_cities.items():
            folium.Marker(
                info["coords"],
                popup=folium.Popup(f"<b>📍 {city}</b><br>Click to analyze", max_width=200),
                tooltip=f"🏙️ {city}",
                icon=folium.Icon(color=info["color"], icon='info-sign')
            ).add_to(m)
    
    # Add search result marker with enhanced styling
    if 'search_result' in st.session_state:
        result = st.session_state.search_result
        folium.Marker(
            [result['lat'], result['lon']],
            popup=folium.Popup(f"<b>🎯 Search Result</b><br>{result['display_name']}", max_width=300),
            tooltip="🔍 Search Result",
            icon=folium.Icon(color='darkgreen', icon='star', prefix='fa')
        ).add_to(m)
    
    # Add coordinate grid if enabled
    if show_grid:
        # Add a simple coordinate reference
        folium.plugins.MeasureControl().add_to(m)
    
    # Display map with enhanced interaction
    map_data = st_folium(m, width=700, height=550, returned_objects=["last_clicked"])

with col2:
    st.subheader("📊 Comprehensive Location Analysis")
    
    # Initialize session state
    if 'last_clicked' not in st.session_state:
        st.session_state.last_clicked = None
    
    # Handle location selection (map click or search)
    current_location = None
    
    if 'selected_location' in st.session_state and st.session_state.get('search_performed'):
        current_location = st.session_state.selected_location
    elif map_data['last_clicked'] is not None:
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lng = map_data['last_clicked']['lng']
        
        if st.session_state.last_clicked != (clicked_lat, clicked_lng):
            st.session_state.last_clicked = (clicked_lat, clicked_lng)
            current_location = (clicked_lat, clicked_lng)
    
    if current_location:
        lat, lon = current_location
        
        with st.spinner("🔄 Analyzing location properties..."):
            # Get comprehensive location properties
            props = get_location_properties(lat, lon)
            
            # Enhanced reverse geocoding
            if auto_geocode:
                try:
                    place_name = get_reverse_geocoding(lat, lon)
                    if place_name and len(place_name) > len(props.get('place_name', '')):
                        props['place_name'] = place_name
                except:
                    pass
            
            # Store results in session
            st.session_state.location_props = props
    
    # Display comprehensive results
    if hasattr(st.session_state, 'location_props'):
        props = st.session_state.location_props
        
        # Enhanced coordinate display
        st.markdown("### 📍 Geographic Coordinates")
        coord_col1, coord_col2 = st.columns(2)
        with coord_col1:
            st.metric("🌐 Latitude", f"{props['lat']:.6f}°", help="North-South position")
        with coord_col2:
            st.metric("🌐 Longitude", f"{props['lon']:.6f}°", help="East-West position")
        
        # Enhanced seismic analysis with risk assessment
        st.markdown("### 🏗️ Seismic Zone Analysis")
        seismic_zone = props.get('seismic_zone', 'Unknown')
        zone_factor = props.get('zone_factor')
        
        if seismic_zone != 'Unknown':
            # Color-coded zone display
            if seismic_zone in ['V']:
                zone_class = "zone-high"
                risk_level = "🔴 Very High Risk"
                risk_desc = "Severe earthquake damage expected"
            elif seismic_zone in ['IV']:
                zone_class = "zone-high" 
                risk_level = "🟠 High Risk"
                risk_desc = "Major earthquake damage possible"
            elif seismic_zone == 'III':
                zone_class = "zone-medium"
                risk_level = "🟡 Moderate Risk"
                risk_desc = "Moderate earthquake damage possible"
            else:
                zone_class = "zone-low"
                risk_level = "🟢 Low Risk"
                risk_desc = "Minor earthquake damage expected"
            
            st.markdown(f'<div class="{zone_class}">🏗️ Seismic Zone: {seismic_zone}</div>', unsafe_allow_html=True)
            
            if zone_factor:
                st.info(f"📊 **Zone Factor (Z):** {zone_factor} (IS 1893:2016)")
            
            if show_risk_assessment:
                st.markdown(f"**⚠️ Risk Assessment:** {risk_level}")
                st.caption(risk_desc)
        else:
            st.warning("⚠️ Seismic zone data not available for this location")
        
        # Enhanced wind analysis
        st.markdown("### 💨 Wind Load Analysis")
        wind_speed = props.get('basic_wind_speed')
        
        if wind_speed:
            st.success(f"💨 **Basic Wind Speed (Vb):** {wind_speed} m/s")
            
            # Wind classification with detailed categories
            if wind_speed >= 50:
                wind_class = "🌪️ Very High - Cyclonic Areas"
                wind_color = "🔴"
            elif wind_speed >= 47:
                wind_class = "🌊 High - Coastal Regions"  
                wind_color = "🟠"
            elif wind_speed >= 44:
                wind_class = "🌾 Moderate - Plains & Valleys"
                wind_color = "🟡"
            elif wind_speed >= 39:
                wind_class = "🏔️ Low - Hilly Regions"
                wind_color = "🟢"
            else:
                wind_class = "🛡️ Very Low - Protected Areas"
                wind_color = "🔵"
            
            st.info(f"{wind_color} **Classification:** {wind_class}")
            st.caption("Based on IS 875 Part 3:2015 - Wind Loads")
        else:
            st.warning("⚠️ Wind speed data not available for this location")
        
        # Enhanced administrative information
        st.markdown("### 🏛️ Administrative Details")
        place_name = props.get('place_name', 'Unknown')
        state = props.get('state', 'Unknown')
        
        if place_name != 'Unknown':
            st.info(f"📍 **Location:** {place_name}")
        if state != 'Unknown':
            st.info(f"🗺️ **State/UT:** {state}")
        
        # Nearby cities analysis
        if show_nearby:
            st.markdown("### 🏙️ Nearby Major Cities")
            try:
                nearby_cities = get_nearby_cities(props['lat'], props['lon'], nearby_radius)
                
                if nearby_cities:
                    st.markdown(f"**Found {len(nearby_cities)} cities within {nearby_radius} km:**")
                    for i, city in enumerate(nearby_cities[:8]):  # Show top 8
                        direction = "📍"
                        st.markdown(f'<div class="nearby-city">{direction} <b>{city["city"]}</b> - {city["distance"]} km away</div>', unsafe_allow_html=True)
                else:
                    st.info(f"ℹ️ No major cities found within {nearby_radius} km radius")
            except Exception as e:
                st.warning("⚠️ Unable to calculate nearby cities")
        
        # Enhanced export functionality
        st.markdown("### 📤 Data Export & Sharing")
        
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            if st.button("📋 Copy Summary", use_container_width=True):
                summary = f"""📍 Location Analysis Report
Coordinates: {props['lat']:.6f}°N, {props['lon']:.6f}°E
Seismic Zone: {seismic_zone} (Factor: {zone_factor or 'N/A'})
Wind Speed: {wind_speed or 'N/A'} m/s
Location: {place_name}, {state}
Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"""
                st.code(summary, language="text")
        
        with export_col2:
            if st.button("📄 JSON Data", use_container_width=True):
                st.json(props)
        
        with export_col3:
            if st.button("🔗 Share Link", use_container_width=True):
                share_url = f"?lat={props['lat']:.6f}&lon={props['lon']:.6f}"
                st.code(f"Location: {props['lat']:.6f}, {props['lon']:.6f}")
    
    else:
        # Enhanced welcome message with instructions
        st.markdown("### 👋 Welcome to Location Wizard")
        st.info("🔍 **Search for a location** using the search bar above, or **click anywhere on the map** to get detailed seismic and wind zone analysis.")
        
        # Show sample analysis data
        st.markdown("### 📊 Sample Analysis Data")
        sample_data = pd.DataFrame({
            "City": ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore"],
            "Seismic Zone": ["IV", "III", "III", "III", "II"],
            "Zone Factor": [0.24, 0.16, 0.16, 0.16, 0.10],
            "Wind Speed (m/s)": [44, 44, 47, 44, 33],
            "Risk Level": ["High", "Moderate", "Moderate", "Moderate", "Low"]
        })
        st.dataframe(sample_data, use_container_width=True)
        
        # Quick tips
        with st.expander("💡 Quick Tips"):
            st.markdown("""
            - **Search Examples:** 'Delhi', 'IIT Bombay', '28.6139, 77.2090'
            - **Map Navigation:** Zoom with mouse wheel, drag to pan
            - **Quick Access:** Use sidebar buttons for major cities
            - **Export Data:** Copy results or download as JSON
            """)

# Enhanced footer with comprehensive information
st.markdown("---")