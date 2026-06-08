from typing import Optional, Any
from shapely.geometry import shape
import json

from .logger import get_logger
from .security import geojson_complexity_safe

logger = get_logger(__name__)

M_PER_DEG = 111320.0


def _area_results(perimeter_deg: float, area_deg: float) -> dict[str, float]:
    area_m2 = area_deg * (M_PER_DEG ** 2)
    perimeter_m = abs(perimeter_deg) * M_PER_DEG
    return {
        "area_sq_m": round(area_m2, 2),
        "area_hectares": round(area_m2 / 10000, 4),
        "area_acres": round(area_m2 / 4046.86, 4),
        "perimeter_m": round(abs(perimeter_m), 2),
        "perimeter_km": round(abs(perimeter_m) / 1000, 3),
    }


def calculate_area_from_geojson(geojson_str: str) -> Optional[dict[str, float]]:
    complexity_err = geojson_complexity_safe(geojson_str)
    if complexity_err:
        logger.warning("GeoJSON rejected: %s", complexity_err)
        return None

    try:
        data = json.loads(geojson_str)
        if data.get("type") == "FeatureCollection":
            features = data.get("features", [])
            total = 0.0
            perimeters: list[float] = []
            for feat in features:
                geom = shape(feat["geometry"])
                total += geom.area
                perimeters.append(geom.length)
            return _area_results(sum(perimeters), total)
        elif data.get("type") == "Feature":
            geom = shape(data["geometry"])
            return _area_results(geom.length, geom.area)
        elif data.get("type") == "Polygon":
            geom = shape(data)
            return _area_results(geom.length, geom.area)
        logger.warning("Unrecognized GeoJSON type: %s", data.get("type"))
        return None
    except json.JSONDecodeError as e:
        logger.error("Invalid GeoJSON string: %s", e)
        return None
    except Exception as e:
        logger.error("Failed to parse GeoJSON geometry: %s", e)
        return None


def calculate_sample_area() -> dict[str, float]:
    sample = {
        "type": "Polygon",
        "coordinates": [[
            [73.8, 18.5],
            [73.85, 18.5],
            [73.85, 18.55],
            [73.8, 18.55],
            [73.8, 18.5],
        ]],
    }
    geom = shape(sample)
    return _area_results(geom.length, geom.area)
