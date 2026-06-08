import os
import tempfile
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from .logger import get_logger

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

logger = get_logger(__name__)

_GEE_INITIALIZED = False


def initialize() -> bool:
    global _GEE_INITIALIZED
    if _GEE_INITIALIZED:
        return True

    try:
        import ee
        ee.Authenticate()
        ee.Initialize(project="ee-default")
        _GEE_INITIALIZED = True
        logger.info("Google Earth Engine initialized")
        return True
    except Exception as e:
        logger.warning("GEE initialization failed: %s — using pre-computed data", e)
        return False


def gee_available() -> bool:
    return _GEE_INITIALIZED or initialize()


def fetch_sentinel2(lat: float, lon: float, days_back: int = 30) -> Optional[object]:
    if not gee_available():
        return None
    try:
        import ee
        point = ee.Geometry.Point([lon, lat])
        end = datetime.now()
        start = end - timedelta(days=days_back)
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(point)
            .filterDate(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
            .sort("CLOUDY_PIXEL_PERCENTAGE")
        )
        image = collection.first()
        if image is None:
            logger.warning("No Sentinel-2 imagery found for (%.4f, %.4f)", lat, lon)
            return None
        logger.info("Fetched Sentinel-2 image for (%.4f, %.4f)", lat, lon)
        return image
    except Exception as e:
        logger.error("Failed to fetch Sentinel-2 imagery: %s", e)
        return None


def compute_ndvi(image) -> Optional[str]:
    try:
        import ee
        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
        vis_params = {
            "min": -0.2, "max": 0.8,
            "palette": ["red", "yellow", "green"],
        }
        map_id = ndvi.getMapId(vis_params)
        return map_id["tile_fetcher"].url_format
    except Exception as e:
        logger.error("Failed to compute NDVI: %s", e)
        return None


def get_ndvi_tile_url(lat: float, lon: float) -> Optional[str]:
    image = fetch_sentinel2(lat, lon)
    if not image:
        return None
    return compute_ndvi(image)
