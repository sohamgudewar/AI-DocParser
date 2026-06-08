import os
from typing import Optional

from celery import Celery
from dotenv import load_dotenv

from .logger import get_logger

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

logger = get_logger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "krishinetra",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)


def celery_available() -> bool:
    try:
        conn = celery_app.connection()
        conn.ensure_connection(timeout=2)
        conn.close()
        return True
    except Exception:
        return False


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def run_ndvi_analysis(self, lat: float, lon: float, ndvi_key: str) -> dict:
    from .crop_predictor import predict_crop
    from .ndvi_loader import get_ndvi_path, analyze_ndvi_pixels
    from .stress_detector import generate_stress_zones, format_recommendation
    from .area_calculator import calculate_sample_area

    crop_result = predict_crop(lat, lon)
    ndvi_path = get_ndvi_path(ndvi_key)
    ndvi_stats = {"healthy": 0.0, "moderate": 0.0, "stressed": 0.0, "avg_ndvi": 0.5}
    if ndvi_path:
        ndvi_stats = analyze_ndvi_pixels(ndvi_path)
    stress_data = generate_stress_zones(lat, lon, ndvi_stats)
    sample_area = calculate_sample_area()
    recommendation = format_recommendation(ndvi_stats)

    return {
        "crop_result": crop_result,
        "ndvi_stats": ndvi_stats,
        "stress_data": stress_data,
        "sample_area": sample_area,
        "recommendation": recommendation,
    }


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def extract_document(self, pdf_bytes: bytes, filename: str) -> dict:
    from .doc_extractor import extract_from_pdf_gemini
    return extract_from_pdf_gemini(pdf_bytes, filename)
