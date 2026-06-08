from typing import Optional
import folium
from folium.plugins import Draw, Fullscreen

MAHARASHTRA_CENTER: list[float] = [19.5, 76.0]


def create_base_map(center: Optional[list[float]] = None, zoom: int = 7) -> folium.Map:
    if center is None:
        center = MAHARASHTRA_CENTER
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        control_scale=True,
    )
    folium.TileLayer("OpenStreetMap", name="Street Map", control=True).add_to(m)
    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        name="Topographic",
        attr="OpenTopoMap",
        control=True,
    ).add_to(m)
    Draw(export=True, filename="drawn_polygon.geojson").add_to(m)
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)
    return m


def add_marker(m: folium.Map, lat: float, lon: float, label: str, color: str = "green") -> None:
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(label, max_width=300),
        tooltip=label,
        icon=folium.Icon(color=color, icon="leaf", prefix="fa"),
    ).add_to(m)


def add_ndvi_overlay(
    m: folium.Map,
    image_path: str,
    bounds: list[list[float]],
    opacity: float = 0.6,
    name: str = "NDVI",
):
    img_overlay = folium.raster_layers.ImageOverlay(
        image=image_path,
        bounds=bounds,
        opacity=opacity,
        name=name,
        overlay=True,
        control=True,
    )
    img_overlay.add_to(m)
    return img_overlay


def add_ndvi_tile_layer(
    m: folium.Map,
    tile_url: str,
    name: str = "NDVI (Live)",
    opacity: float = 0.55,
):
    tile = folium.TileLayer(
        tiles=tile_url,
        name=name,
        overlay=True,
        control=True,
        opacity=opacity,
        attr="Google Earth Engine",
    )
    tile.add_to(m)
    return tile


def get_ndvi_bounds(lat: float, lon: float, size_km: float = 10) -> list[list[float]]:
    deg = size_km / 111.0
    return [[lat - deg, lon - deg], [lat + deg, lon + deg]]
