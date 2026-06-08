import os
import re
from typing import Optional

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
PDF_MAGIC = b"%PDF"
COORD_MIN_LAT = 15.0
COORD_MAX_LAT = 22.0
COORD_MIN_LON = 72.0
COORD_MAX_LON = 81.0
GEOJSON_MAX_POINTS = 50000


def validate_pdf_upload(content: bytes, filename: str) -> Optional[str]:
    if len(content) > MAX_FILE_SIZE_BYTES:
        return f"File too large ({len(content) / 1024 / 1024:.1f} MB). Max: {MAX_FILE_SIZE_BYTES / 1024 / 1024:.0f} MB"
    if not content.startswith(PDF_MAGIC):
        return "File does not appear to be a valid PDF"
    if not filename or ".." in filename or "/" in filename or "\\" in filename:
        return "Invalid filename"
    return None


def sanitize_filename(filename: str) -> str:
    safe = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return safe[:255]


def validate_coordinates(lat: float, lon: float) -> Optional[str]:
    if not (COORD_MIN_LAT <= lat <= COORD_MAX_LAT):
        return f"Latitude {lat} outside Maharashtra bounds ({COORD_MIN_LAT}–{COORD_MAX_LAT})"
    if not (COORD_MIN_LON <= lon <= COORD_MAX_LON):
        return f"Longitude {lon} outside Maharashtra bounds ({COORD_MIN_LON}–{COORD_MAX_LON})"
    return None


def geojson_complexity_safe(geojson_str: str) -> Optional[str]:
    try:
        point_count = geojson_str.count("[")
        if point_count > GEOJSON_MAX_POINTS:
            return f"GeoJSON too complex ({point_count} nodes). Max allowed: {GEOJSON_MAX_POINTS}"
    except Exception:
        return "Invalid GeoJSON"
    return None
