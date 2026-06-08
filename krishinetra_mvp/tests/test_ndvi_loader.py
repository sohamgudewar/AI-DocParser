import os
from modules.ndvi_loader import (
    get_ndvi_path, analyze_ndvi_pixels, NDVI_FILES, NDVI_DIR
)


def test_get_ndvi_path_known_key():
    path = get_ndvi_path("vidarbha_cotton")
    if os.path.exists(os.path.join(NDVI_DIR, NDVI_FILES["vidarbha_cotton"])):
        assert path is not None
        assert path.endswith("vidarbha_cotton_ndvi.png")
    else:
        assert path is None


def test_get_ndvi_path_unknown_key():
    assert get_ndvi_path("nonexistent_key") is None


def test_analyze_ndvi_pixels_healthy(test_ndvi_png):
    result = analyze_ndvi_pixels(test_ndvi_png)
    assert isinstance(result, dict)
    assert "healthy" in result
    assert "moderate" in result
    assert "stressed" in result
    assert "avg_ndvi" in result
    assert result["healthy"] >= 0
    assert result["avg_ndvi"] >= 0


def test_analyze_ndvi_pixels_stressed(test_stressed_ndvi_png):
    result = analyze_ndvi_pixels(test_stressed_ndvi_png)
    assert result["stressed"] > result["healthy"]


def test_analyze_ndvi_pixels_empty(test_empty_ndvi_png):
    result = analyze_ndvi_pixels(test_empty_ndvi_png)
    assert result["healthy"] == 0
    assert result["avg_ndvi"] == 0.5


def test_analyze_ndvi_pixels_nonexistent():
    result = analyze_ndvi_pixels("nonexistent.png")
    assert result["healthy"] == 0
    assert result["avg_ndvi"] == 0.5


def test_ndvi_files_dict():
    assert isinstance(NDVI_FILES, dict)
    assert len(NDVI_FILES) >= 3
    assert "vidarbha_cotton" in NDVI_FILES
