from modules.area_calculator import (
    calculate_area_from_geojson, calculate_sample_area
)


SAMPLE_POLYGON = """{
    "type": "Polygon",
    "coordinates": [[
        [73.8, 18.5],
        [73.85, 18.5],
        [73.85, 18.55],
        [73.8, 18.55],
        [73.8, 18.5]
    ]]
}"""

SAMPLE_FEATURE = """{
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [73.8, 18.5],
            [73.85, 18.5],
            [73.85, 18.55],
            [73.8, 18.55],
            [73.8, 18.5]
        ]]
    },
    "properties": {}
}"""

SAMPLE_COLLECTION = """{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [73.8, 18.5],
                    [73.85, 18.5],
                    [73.85, 18.55],
                    [73.8, 18.55],
                    [73.8, 18.5]
                ]]
            },
            "properties": {}
        }
    ]
}"""


def test_calculate_area_from_geojson_polygon():
    result = calculate_area_from_geojson(SAMPLE_POLYGON)
    assert result is not None
    assert "area_hectares" in result
    assert "area_acres" in result
    assert "perimeter_m" in result
    assert result["area_hectares"] > 0


def test_calculate_area_from_geojson_feature():
    result = calculate_area_from_geojson(SAMPLE_FEATURE)
    assert result is not None
    assert result["area_hectares"] > 0


def test_calculate_area_from_geojson_collection():
    result = calculate_area_from_geojson(SAMPLE_COLLECTION)
    assert result is not None
    assert result["area_hectares"] > 0


def test_calculate_area_from_geojson_bad_json():
    assert calculate_area_from_geojson("not json") is None


def test_calculate_area_from_geojson_unknown_type():
    result = calculate_area_from_geojson('{"type": "Point", "coordinates": [0, 0]}')
    assert result is None


def test_sample_area():
    result = calculate_sample_area()
    assert result["area_hectares"] > 0
    assert isinstance(result["area_hectares"], float)
