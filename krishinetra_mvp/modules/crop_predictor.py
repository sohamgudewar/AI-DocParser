import json
import os
from typing import Optional

from .logger import get_logger
from .ml_pipeline import pipeline as ml_pipeline

logger = get_logger(__name__)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOKUP_PATH = os.path.join(BASE, "data", "crop_lookup.json")

_DEFAULT_RESULT: dict[str, str | float] = {
    "crop": "unknown",
    "variety": "N/A",
    "season": "N/A",
    "region": "Unidentified",
    "emoji": "\u2753",
    "confidence": 0.0,
}


def _load_zones() -> tuple[list[dict], dict]:
    try:
        with open(LOOKUP_PATH, "r") as f:
            data = json.load(f)
        return data["zones"], data.get("demo_locations", {})
    except FileNotFoundError:
        logger.error("Crop lookup file not found at: %s", LOOKUP_PATH)
        return [], {}
    except (json.JSONDecodeError, KeyError) as e:
        logger.error("Invalid crop lookup file: %s", e)
        return [], {}


def predict_crop(
    lat: float,
    lon: float,
    ndvi_health_pct: Optional[float] = None,
    area_hectares: Optional[float] = None,
) -> dict[str, str | float]:
    result = ml_pipeline.predict(lat, lon, ndvi_health_pct, area_hectares)
    base = {
        "crop": result["crop"],
        "variety": result["variety"],
        "season": result["season"],
        "region": result["region"],
        "emoji": result["emoji"],
        "confidence": result["confidence"],
    }
    return base


def get_demo_location(key: str) -> Optional[dict]:
    _, demos = _load_zones()
    return demos.get(key)
