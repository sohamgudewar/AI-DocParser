import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.security import validate_coordinates
from modules.crop_predictor import predict_crop
from modules.ndvi_loader import get_ndvi_path, analyze_ndvi_pixels
from modules.stress_detector import generate_stress_zones, format_recommendation
from modules.area_calculator import calculate_sample_area
from modules.doc_extractor import _fallback_extract, verify_document, _parse_gps
from modules.auth import authenticate
from modules.ml_pipeline import CropModelPipeline


def test_full_analysis_pipeline_vidarbha():
    lat, lon = 20.5, 77.5
    assert validate_coordinates(lat, lon) is None

    crop = predict_crop(lat, lon)
    assert crop["crop"] == "cotton"
    assert crop["region"] == "Vidarbha"
    assert 80 <= crop["confidence"] <= 99

    ndvi_path = get_ndvi_path("vidarbha_cotton")
    assert ndvi_path is not None
    assert os.path.exists(ndvi_path)

    ndvi = analyze_ndvi_pixels(ndvi_path)
    for key in ("healthy", "moderate", "stressed", "avg_ndvi"):
        assert key in ndvi

    stress = generate_stress_zones(lat, lon, ndvi)
    assert "summary" in stress
    assert "stressed_ha" in stress["summary"]

    rec = format_recommendation(ndvi)
    assert isinstance(rec, str) and len(rec) > 0

    area = calculate_sample_area()
    assert "area_hectares" in area
    assert area["area_hectares"] > 0


def test_full_analysis_pipeline_nashik():
    lat, lon = 19.5, 73.5
    assert validate_coordinates(lat, lon) is None

    crop = predict_crop(lat, lon)
    assert crop["crop"] == "onion"

    ndvi_path = get_ndvi_path("nashik_onion")
    assert ndvi_path is not None

    ndvi = analyze_ndvi_pixels(ndvi_path)
    assert 0 <= ndvi["avg_ndvi"] <= 1


def test_unknown_coordinates_graceful():
    lat, lon = 99.0, 99.0
    err = validate_coordinates(lat, lon)
    assert err is not None

    crop = predict_crop(lat, lon)
    assert crop["crop"] == "unknown"


def test_full_document_verification_flow():
    doc = _fallback_extract("patil_record.pdf")
    assert doc["owner_name"] == "Rajesh Vitthal Patil"

    verify = verify_document(doc, 18.52, 73.85)
    assert "checks" in verify
    assert "GPS Coordinates" in verify["checks"]


def test_document_verify_coord_mismatch():
    doc = _fallback_extract("patil_record.pdf")
    verify = verify_document(doc, 20.0, 77.0)
    assert verify["all_match"] is False
    assert verify["checks"]["GPS Coordinates"]["status"] == "mismatch"


def test_auth_flow():
    user = authenticate("admin@krishinetra.in")
    assert user is not None
    assert user["email"] == "admin@krishinetra.in"
    assert user["role"] == "admin"

    user2 = authenticate("farmer@demo.in")
    assert user2 is not None
    assert user2["role"] == "farmer"

    bad = authenticate("invalid")
    assert bad is None

    unknown = authenticate("newuser@test.com")
    assert unknown is not None
    assert unknown["email"] == "newuser@test.com"
    assert unknown["role"] == "farmer"


def test_pipeline_with_ml_pipeline():
    pipe = CropModelPipeline()
    result = pipe.predict(20.5, 77.5, ndvi_health_pct=85.0, area_hectares=3.0)
    assert result["crop"] == "cotton"
    assert result["confidence"] > 90


def test_parse_gps_formats():
    assert _parse_gps("18.5204 N, 73.8567 E") == (18.5204, 73.8567)
    assert _parse_gps("20.9 N, 77.7 E") == (20.9, 77.7)
    assert _parse_gps("") is None
    assert _parse_gps("not a coord") is None


def test_ndvi_pipeline_demo_locations():
    for key in ("vidarbha_cotton", "nashik_onion", "pune_sugarcane"):
        path = get_ndvi_path(key)
        assert path is not None, f"NDVI path missing for {key}"
        assert os.path.exists(path), f"NDVI file not found for {key}"
        ndvi = analyze_ndvi_pixels(path)
        assert 0 <= ndvi["avg_ndvi"] <= 1
