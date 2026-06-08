from modules.ml_pipeline import CropModelPipeline, _DEFAULT_PREDICTION


def test_pipeline_initializes():
    p = CropModelPipeline()
    assert p.model_type == "dummy"
    assert "dummy" in p.get_available_models()


def test_pipeline_predict_known():
    p = CropModelPipeline()
    result = p.predict(20.5, 77.5)
    assert result["crop"] == "cotton"
    assert result["region"] == "Vidarbha"
    assert 80 <= result["confidence"] <= 99


def test_pipeline_predict_unknown():
    p = CropModelPipeline()
    result = p.predict(99.0, 99.0)
    assert result["crop"] == "unknown"
    assert 50 <= result["confidence"] <= 100


def test_pipeline_predict_with_ndvi():
    p = CropModelPipeline()
    result = p.predict(20.5, 77.5, ndvi_health_pct=90.0)
    assert result["crop"] == "cotton"
    assert result["confidence"] >= 88


def test_pipeline_predict_with_area():
    p = CropModelPipeline()
    result = p.predict(20.5, 77.5, area_hectares=5.0)
    assert result["crop"] == "cotton"


def test_pipeline_predict_returns_soil_type():
    p = CropModelPipeline()
    result = p.predict(20.5, 77.5)
    assert "soil_type" in result
    assert result["soil_type"] == "black_cotton"


def test_pipeline_set_model():
    p = CropModelPipeline()
    p.set_model("sklearn")
    assert p.model_type == "sklearn"


def test_pipeline_fallback_on_unavailable_model():
    p = CropModelPipeline()
    p.set_model("sklearn")
    result = p.predict(20.5, 77.5)
    assert result["crop"] == "cotton"


def test_pipeline_load_model_bad_path():
    p = CropModelPipeline()
    p.load_model("/nonexistent/model.pkl")
    assert p._trained_model is None


def test_pipeline_extract_features():
    p = CropModelPipeline()
    feats = p._extract_features(20.5, 77.5)
    assert feats["region"] == "Vidarbha"
    assert feats["soil_type"] == "black_cotton"
    assert feats["matched_zone"] is not None
