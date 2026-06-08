import json
import math
import os
import pickle
from typing import Optional

from .logger import get_logger

logger = get_logger(__name__)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOKUP_PATH = os.path.join(BASE, "data", "crop_lookup.json")

_DEFAULT_PREDICTION = {
    "crop": "unknown",
    "variety": "N/A",
    "season": "N/A",
    "region": "Unidentified",
    "emoji": "\u2753",
    "confidence": 0.0,
}


_MAHARASHTRA_SOIL_ZONES = {
    "vidarbha": "black_cotton",
    "western_maharashtra": "laterite",
    "marathwada": "shallow_black",
    "nashik": "red_loamy",
    "konkan": "coastal_alluvial",
    "satara_kolhapur": "medium_black",
}


class CropModelPipeline:
    def __init__(self, model_type: str = "dummy"):
        self.model_type = model_type
        self._zones, self._demos = self._load_zones()
        self._trained_model = None

    def _load_zones(self) -> tuple[list[dict], dict]:
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

    def _extract_features(self, lat: float, lon: float) -> dict:
        region_key = None
        matched_zone = None
        for zone in self._zones:
            lat_min, lat_max = zone["lat_range"]
            lon_min, lon_max = zone["lon_range"]
            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                region_key = zone["region"].lower().replace(" ", "_").replace("-", "_")
                matched_zone = zone
                break

        soil_type = _MAHARASHTRA_SOIL_ZONES.get(region_key, "unknown")
        return {
            "lat": lat,
            "lon": lon,
            "region": matched_zone["region"] if matched_zone else "Unidentified",
            "region_key": region_key,
            "soil_type": soil_type,
            "matched_zone": matched_zone,
        }

    def predict(
        self,
        lat: float,
        lon: float,
        ndvi_health_pct: Optional[float] = None,
        area_hectares: Optional[float] = None,
    ) -> dict:
        if self.model_type == "dummy":
            return self._predict_dummy(lat, lon, ndvi_health_pct, area_hectares)
        elif self.model_type == "sklearn" and self._trained_model is not None:
            return self._predict_sklearn(lat, lon, ndvi_health_pct, area_hectares)
        logger.warning("Model type '%s' not available — falling back to dummy", self.model_type)
        return self._predict_dummy(lat, lon, ndvi_health_pct, area_hectares)

    def _predict_dummy(
        self,
        lat: float,
        lon: float,
        ndvi_health_pct: Optional[float] = None,
        area_hectares: Optional[float] = None,
    ) -> dict:
        features = self._extract_features(lat, lon)
        zone = features["matched_zone"]
        if not zone:
            result = _DEFAULT_PREDICTION.copy()
            result["confidence"] = round(50 + (abs(lat) * 7 + abs(lon) * 3) % 15, 1)
            return result

        base_conf = 88.0
        if ndvi_health_pct is not None:
            health_conf = min(ndvi_health_pct / 100, 1.0) * 10
            base_conf = min(base_conf + health_conf, 98.0)
        if area_hectares is not None and area_hectares > 0:
            size_factor = min(area_hectares / 10, 1.0) * 2
            base_conf = min(base_conf + size_factor, 99.0)

        return {
            "crop": zone["crop"],
            "variety": zone["typical_variety"],
            "season": zone["growing_season"],
            "region": features["region"],
            "soil_type": features["soil_type"],
            "emoji": zone["emoji"],
            "confidence": round(base_conf, 1),
            "features": features,
        }

    def _predict_sklearn(
        self,
        lat: float,
        lon: float,
        ndvi_health_pct: Optional[float] = None,
        area_hectares: Optional[float] = None,
    ) -> dict:
        if self._trained_model is None:
            return self._predict_dummy(lat, lon, ndvi_health_pct, area_hectares)
        import numpy as np
        X = np.array([[lat, lon, ndvi_health_pct or 50, area_hectares or 1.0]])
        try:
            pred = self._trained_model.predict(X)
            proba = self._trained_model.predict_proba(X)
            confidence = round(float(proba.max()) * 100, 1)
            return {
                "crop": str(pred[0]),
                "variety": "N/A",
                "season": "N/A",
                "region": "Model-based",
                "soil_type": "N/A",
                "emoji": "\ud83e\uddea",
                "confidence": confidence,
                "model_type": "sklearn",
            }
        except Exception as e:
            logger.error("Sklearn prediction failed: %s — falling back to dummy", e)
            return self._predict_dummy(lat, lon, ndvi_health_pct, area_hectares)

    def set_model(self, model_type: str) -> None:
        self.model_type = model_type
        logger.info("Pipeline model set to: %s", model_type)

    def load_model(self, path: str) -> None:
        try:
            with open(path, "rb") as f:
                self._trained_model = pickle.load(f)
            self.model_type = "sklearn"
            logger.info("Loaded trained model from: %s", path)
        except Exception as e:
            logger.error("Failed to load model from %s: %s", path, e)

    def get_available_models(self) -> list[str]:
        return ["dummy", "sklearn"]


pipeline = CropModelPipeline()
