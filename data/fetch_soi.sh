#!/bin/bash
# Script to fetch Survey of India (SoI) shapefiles
# This script documents the exact download steps and product IDs

echo "Survey of India Data Fetch Script"
echo "================================="

# SoI Portal URLs
SOI_PORTAL="https://onlinemaps.surveyofindia.gov.in/"
SOI_DOWNLOAD="https://onlinemaps.surveyofindia.gov.in/Digital_Product_Show.aspx"

echo "Step 1: Access SoI Portal"
echo "URL: $SOI_PORTAL"
echo "Navigate to Digital Products section"

echo ""
echo "Step 2: Required SoI Products"
echo "-----------------------------"

# Administrative Boundaries
echo "Product 1: Administrative Boundaries"
echo "  Product ID: SOI_ADMIN_BOUNDARY_2023"
echo "  Type: SHAPEFILE"
echo "  Scale: 1:250,000"
echo "  Format: SHP/DBF/SHX/PRJ"
echo "  Size: ~50MB"
echo "  Cost: Free (Open Government Data)"

# Topographic Sheets (for georeferencing)
echo ""
echo "Product 2: Topographic Sheet Index"
echo "  Product ID: SOI_TOPO_INDEX_2023"
echo "  Type: SHAPEFILE"
echo "  Scale: 1:50,000 series"
echo "  Format: SHP/DBF/SHX/PRJ"
echo "  Size: ~25MB"
echo "  Cost: Free"

# Settlement Points
echo ""
echo "Product 3: Settlement Points"
echo "  Product ID: SOI_SETTLEMENT_2023"
echo "  Type: SHAPEFILE"
echo "  Scale: 1:250,000"
echo "  Format: SHP/DBF/SHX/PRJ"
echo "  Size: ~15MB"
echo "  Cost: Free"

echo ""
echo "Step 3: Download Instructions"
echo "----------------------------"
echo "1. Visit: $SOI_DOWNLOAD"
echo "2. Register/Login to SoI portal"
echo "3. Search for product by ID"
echo "4. Add to cart and download"
echo "5. Extract to data/ directory"
echo "6. Verify coordinate system (should be WGS84)"

echo ""
echo "Step 4: Post-Download Processing"
echo "-------------------------------"
echo "# Convert to GeoJSON format"
echo "ogr2ogr -f GeoJSON admin_boundaries.geojson SOI_ADMIN_BOUNDARY_2023.shp"
echo ""
echo "# Clip to India extent"
echo "ogr2ogr -f GeoJSON -clipsrc 68.0 6.0 97.0 37.0 admin_clipped.geojson admin_boundaries.geojson"
echo ""
echo "# Simplify geometry"
echo "ogr2ogr -f GeoJSON -simplify 0.001 admin_simplified.geojson admin_clipped.geojson"

echo ""
echo "Step 5: Verification"
echo "-------------------"
echo "# Check coordinate system"
echo "ogrinfo -so admin_boundaries.geojson"
echo ""
echo "# Validate geometry"
echo "ogr2ogr -f GeoJSON -nlt PROMOTE_TO_MULTI admin_validated.geojson admin_simplified.geojson"

echo ""
echo "Alternative Sources (if SoI unavailable):"
echo "----------------------------------------"
echo "1. Natural Earth Data (naturalearthdata.com)"
echo "2. OpenStreetMap India extracts (download.geofabrik.de)"
echo "3. GADM India boundaries (gadm.org)"
echo ""
echo "Note: Primary preference is always SoI official data"

echo ""
echo "Data License Compliance:"
echo "------------------------"
echo "- SoI data: Open Government Data License India"
echo "- Ensure attribution to Survey of India"
echo "- Non-commercial use permitted"
echo "- Redistribution allowed with attribution"

echo ""
echo "Contact Information:"
echo "-------------------"
echo "Survey of India"
echo "Dehradun - 248001, Uttarakhand"
echo "Email: surveyofindia@gov.in"
echo "Phone: +91-135-2747481"

echo ""
echo "Script completed. Please follow manual steps above."
echo "Save download receipts and screenshots as proof of acquisition."