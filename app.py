import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
from io import BytesIO
from functools import lru_cache

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
st.title("GeoPandas Layers with Styling and Filters")

# Create the map with OpenStreetMap as the default basemap
m = leafmap.Map(center=(27.7172, 85.3240), zoom=10)  # Kathmandu centre
m.add_basemap("OPENSTREETMAP")  # Add default basemap

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
geojson_files = {
    "InternationalBoundary": "data/InternationalBoundary.geojson",
    "Province": "data/Province.geojson",
    "District": "data/District.geojson",
    "LocalLevel": "data/LocalLevel.geojson",
    "Ward": "data/Ward.geojson"
}

# Define style functions for each layer
def style_internationalboundary(feature):
    return {
        "fillColor": "transparent",
        "color": "red",
        "weight": 0.6,
        "dashArray": "5, 5, 1, 5"  # Dash Dot Dot Line
    }

def style_province(feature):
    return {
        "fillColor": "transparent",
        "color": "#161aec",
        "weight": 0.5,
        "dashArray": "10, 5"  # Dash Line
    }

def style_district(feature):
    return {
        "fillColor": "transparent",
        "color": "#c814d8",
        "weight": 0.4,
        "dashArray": "4, 4"  # Dot Line
    }

def style_locallevel(feature):
    return {
        "fillColor": "transparent",
        "color": "#232323",
        "weight": 0.3,
        "dashArray": ""  # Solid Line
    }

def style_ward(feature):
    return {
        "fillColor": "transparent",
        "color": "#232323",
        "weight": 0.2,
        "dashArray": ""  # Solid Line
    }

# Function to cache the loading of GeoJSON files
@lru_cache(maxsize=5)
def load_geojson(file_path):
    return gpd.read_file(file_path)

# Function to convert filtered GeoDataFrame to KML and create download link
def download_kml(gdf, layer_name):
    kml_buffer = BytesIO()
    gdf.to_file(kml_buffer, driver="KML")
    kml_buffer.seek(0)
    return kml_buffer

# Sidebar options for layers and filters
for layer_name, file_path in geojson_files.items():
    # Checkbox to toggle layer visibility
    show_layer = st.sidebar.checkbox(layer_name, value=(layer_name in ["InternationalBoundary", "Province"]))

    if show_layer:
        gdf = load_geojson(file_path)

        # Filter UI
        with st.sidebar.expander(f"Filter {layer_name}"):
            attribute_field = st.selectbox(f"Select attribute to filter {layer_name}", gdf.columns, key=f"{layer_name}_attribute")
            unique_values = gdf[attribute_field].unique()
            attribute_value = st.selectbox(f"Select value for {attribute_field}", unique_values, key=f"{layer_name}_value")

            apply_filter = st.button(f"Apply Filter to {layer_name}", key=f"{layer_name}_apply")
            clear_filter = st.button(f"Clear Filter for {layer_name}", key=f"{layer_name}_clear")

            # Apply filter if button is pressed
            if apply_filter:
                gdf = gdf[gdf[attribute_field] == attribute_value]

            # Provide download option if a filter is applied
            if not gdf.empty:
                kml_data = download_kml(gdf, layer_name)
                st.download_button(
                    label=f"Download Filtered {layer_name} as KML",
                    data=kml_data,
                    file_name=f"{layer_name}_filtered.kml",
                    mime="application/vnd.google-earth.kml+xml",
                    key=f"{layer_name}_download"
                )

        # Add the layer to the map with its style function
        style_function = globals()[f"style_{layer_name.replace(' ', '').lower()}"]  # Dynamically get style function
        m.add_gdf(gdf, layer_name=layer_name, style_function=style_function)

# Add a Layer Control widget to allow toggling
m.add_layer_control()

# Display the map in full-screen mode
m.to_streamlit(height=800)