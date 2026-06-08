from modules.crop_predictor import predict_crop, get_demo_location


def test_predict_crop_vidarbha():
    result = predict_crop(20.5, 77.5)
    assert result["crop"] == "cotton"
    assert result["region"] == "Vidarbha"
    assert 80 <= result["confidence"] <= 95


def test_predict_crop_nashik():
    result = predict_crop(19.5, 73.5)
    assert result["crop"] == "onion"
    assert result["region"] == "Nashik"


def test_predict_crop_unknown():
    result = predict_crop(99.0, 99.0)
    assert result["crop"] == "unknown"
    assert 50 <= result["confidence"] <= 65


def test_predict_crop_edge():
    result = predict_crop(19.0, 76.0)
    assert isinstance(result, dict)
    assert "crop" in result


def test_predict_crop_returns_required_keys():
    result = predict_crop(18.0, 74.0)
    for key in ("crop", "variety", "season", "region", "emoji", "confidence"):
        assert key in result


def test_get_demo_location_known():
    loc = get_demo_location("vidarbha_cotton")
    assert loc is not None
    assert loc["crop"] == "cotton"


def test_get_demo_location_unknown():
    assert get_demo_location("nonexistent") is None
