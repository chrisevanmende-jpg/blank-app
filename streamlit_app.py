import streamlit as st
import folium
import geopandas as gpd
import requests
from shapely import wkt
from shapely.geometry import mapping
from streamlit_folium import st_folium

# Seite konfigurieren
st.set_page_config(page_title="PolygonViewer_by_CM", page_icon="🗺️", layout="wide")

st.title("PolygonViewer")

# Polygon eingeben
wkt_input = st.text_area(
    "Gib deine WKT:",
    "POLYGON((13.375 52.52, 13.405 52.52, 13.405 52.535, 13.375 52.535, 13.375 52.52))",
    height=150
)

# PLZ GeoJSON von OpenDataSoft laden
url = "https://public.opendatasoft.com/explore/dataset/georef-germany-postleitzahl/download/?format=geojson"
response = requests.get(url)
plz_data = response.json()

# OpenStreetMap
folium.TileLayer(
    tiles="https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
    name='OSM DE',
    overlay=False,
    control=True
).add_to(m)

# Karte anzeigen
if st.button("Karte anzeigen"):
    try:
        # WKT in Geometrie umwandeln
        geom = wkt.loads(wkt_input)

        # Karte erstellen
        m = folium.Map(location=[52.52, 13.4], zoom_start=12)

        # WKT-Polygon zur Karte hinzufügen
        folium.GeoJson(
            mapping(geom),
            style_function=lambda x: {"fillColor": "blue", "color": "red", "weight": 2, "fillOpacity": 0.3},
            tooltip="Dein Polygon"
        ).add_to(m)

        # Überlappende PLZ-Polygone finden
        for feature in plz_data["features"]:
            plz_polygon = shape(feature["geometry"])
            if geom.intersects(plz_polygon):
                plz_code = feature["properties"]["plz"]
                folium.GeoJson(
                    feature,
                    style_function=lambda x: {"fillColor": "yellow", "color": "orange", "weight": 1, "fillOpacity": 0.2},
                    tooltip=f"PLZ: {plz_code}"
                ).add_to(m)

        # Karte in Streamlit anzeigen
        st_folium(m, width=800, height=600)

    except Exception as e:
        st.error(f"Fehler: {e}")
