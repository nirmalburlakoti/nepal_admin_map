import streamlit as st
import leafmap.foliumap as leafmap

# Configure Streamlit layout to maximise map area
st.set_page_config(layout="wide")

# Hide Streamlit's default header and footer
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title (Optional)
st.title("Full-Screen Web Map Application with XYZ Tiles")

# Create the map with a default basemap (OpenStreetMap active by default)
m = leafmap.Map(center=(27.7172, 85.3240), zoom=10)  # Kathmandu centre

# Add OpenStreetMap basemap (enabled by default)
m.add_basemap("OPENSTREETMAP")

# Add Google Maps (disabled by default)
m.add_tile_layer(
    url="https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}",
    name="Google Maps",
    attribution="© Google",
    control=True,  # Adds this layer to the layer control
    shown=False    # Keeps this layer turned off by default
)

# Add Google Satellite (disabled by default)
m.add_tile_layer(
    url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    name="Google Satellite",
    attribution="© Google",
    control=True,  # Adds this layer to the layer control
    shown=False    # Keeps this layer turned off by default
)

# Paths to GeoJSON files
geojson_1_path = "data/InternationalBoundary.geojson"  # Replace with your file path
geojson_2_path = "data/Province.geojson"  # Replace with your file path

# Add GeoJSON layers to the map
m.add_geojson(
    geojson_1_path, 
    layer_name="Nepal"
)

m.add_geojson(
    geojson_2_path, 
    layer_name="Province"
)

# Add a Layer Control widget
m.add_layer_control()  # Ensures only one base layer is active at a time

# Display the map in full-screen mode
m.to_streamlit(height=800)
