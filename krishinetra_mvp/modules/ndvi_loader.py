import os
from typing import Optional, Union
import numpy as np
import numpy.typing as npt
from PIL import Image

from .logger import get_logger
from .gee_client import gee_available, get_ndvi_tile_url

logger = get_logger(__name__)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NDVI_DIR = os.path.join(BASE, "data", "ndvi_overlays")

NDVI_FILES: dict[str, str] = {
    "vidarbha_cotton": "vidarbha_cotton_ndvi.png",
    "nashik_onion": "nashik_onion_ndvi.png",
    "pune_sugarcane": "pune_sugarcane_ndvi.png",
    "marathwada_soybean": "marathwada_soybean_ndvi.png",
    "western_maharashtra_sugarcane": "western_maharashtra_sugarcane_ndvi.png",
    "konkan_rice": "konkan_rice_ndvi.png",
}

_ndvi_cache: dict[str, str] = {}


def get_ndvi_overlay(lat: float, lon: float, use_live: bool = True) -> tuple[Optional[Union[str, bytes]], bool]:
    cache_key = f"{lat:.2f}_{lon:.2f}"
    if cache_key in _ndvi_cache:
        return _ndvi_cache[cache_key], True

    if use_live and gee_available():
        tile_url = get_ndvi_tile_url(lat, lon)
        if tile_url:
            _ndvi_cache[cache_key] = tile_url
            return tile_url, True

    fname = NDVI_FILES.get("vidarbha_cotton")
    if fname:
        path = os.path.join(NDVI_DIR, fname)
        if os.path.exists(path):
            return path, False
    return None, False


def get_ndvi_path(key: str) -> Optional[str]:
    fname = NDVI_FILES.get(key)
    if not fname:
        logger.warning("No NDVI file mapping for key: %s", key)
        return None
    path = os.path.join(NDVI_DIR, fname)
    if not os.path.exists(path):
        logger.warning("NDVI file not found at: %s", path)
        return None
    return path


def analyze_ndvi_pixels(image_path: str) -> dict[str, float]:
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        logger.error("Failed to open NDVI image %s: %s", image_path, e)
        return {"healthy": 0.0, "moderate": 0.0, "stressed": 0.0, "avg_ndvi": 0.5}

    arr: npt.NDArray[np.float32] = np.array(img, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    total = float(np.sum(a > 0))
    if total == 0:
        logger.warning("NDVI image has no visible pixels")
        return {"healthy": 0.0, "moderate": 0.0, "stressed": 0.0, "avg_ndvi": 0.5}

    red_pixels = float(np.sum((r > 200) & (g < 100) & (b < 100) & (a > 0)))
    green_pixels = float(np.sum((g > 150) & (r < 150) & (a > 0)))
    yellow_pixels = float(np.sum((r > 200) & (g > 180) & (b < 100) & (a > 0)))

    stressed = red_pixels / total
    healthy = green_pixels / total
    moderate = yellow_pixels / total
    avg_ndvi = healthy * 0.7 + moderate * 0.4 + stressed * 0.15

    logger.debug("NDVI analysis: healthy=%.1f%%, moderate=%.1f%%, stressed=%.1f%%",
                 healthy * 100, moderate * 100, stressed * 100)

    return {
        "healthy": round(healthy * 100, 1),
        "moderate": round(moderate * 100, 1),
        "stressed": round(stressed * 100, 1),
        "avg_ndvi": round(avg_ndvi, 2),
    }
