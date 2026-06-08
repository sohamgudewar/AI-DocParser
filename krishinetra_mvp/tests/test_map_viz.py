from modules.map_viz import (
    create_base_map, add_marker, get_ndvi_bounds, MAHARASHTRA_CENTER
)
import folium


def test_get_ndvi_bounds():
    bounds = get_ndvi_bounds(19.0, 76.0, 10)
    assert len(bounds) == 2
    assert len(bounds[0]) == 2
    assert len(bounds[1]) == 2
    assert bounds[0][0] < bounds[1][0]
    assert bounds[0][1] < bounds[1][1]


def test_get_ndvi_bounds_default_size():
    bounds = get_ndvi_bounds(19.0, 76.0)
    lat_diff = bounds[1][0] - bounds[0][0]
    assert abs(lat_diff - 10/111.0 * 2) < 0.001


def test_get_ndvi_bounds_center():
    bounds = get_ndvi_bounds(19.0, 76.0, 10)
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lon = (bounds[0][1] + bounds[1][1]) / 2
    assert abs(center_lat - 19.0) < 0.001
    assert abs(center_lon - 76.0) < 0.001


def test_create_base_map():
    m = create_base_map(center=[19.0, 76.0], zoom=10)
    assert isinstance(m, folium.Map)


def test_create_base_map_default_center():
    m = create_base_map()
    assert m.location == MAHARASHTRA_CENTER


def test_add_marker():
    m = create_base_map(center=[19.0, 76.0])
    add_marker(m, 19.5, 76.5, "Test Marker", color="red")
    assert len(list(m._children)) > 0
