from modules.stress_detector import generate_stress_zones, format_recommendation


def test_generate_stress_zones_structure():
    stats = {"healthy": 50.0, "moderate": 30.0, "stressed": 20.0}
    result = generate_stress_zones(19.0, 76.0, stats)
    assert result["type"] == "FeatureCollection"
    assert len(result["features"]) == 8
    assert "summary" in result


def test_generate_stress_zones_summary():
    stats = {"healthy": 50.0, "moderate": 30.0, "stressed": 20.0}
    result = generate_stress_zones(19.0, 76.0, stats)
    s = result["summary"]
    assert s["healthy_ha"] == 5.0
    assert s["moderate_ha"] == 3.0
    assert s["stressed_ha"] == 2.0
    assert s["total_analyzed_ha"] == 10.0


def test_generate_stress_zones_features():
    stats = {"healthy": 100.0, "moderate": 0.0, "stressed": 0.0}
    result = generate_stress_zones(19.0, 76.0, stats)
    for feat in result["features"]:
        assert feat["type"] == "Feature"
        assert feat["properties"]["zone"] in ("Healthy Zone", "Moderate Stress", "High Stress")
        assert "geometry" in feat


def test_generate_stress_zones_defaults():
    result = generate_stress_zones(19.0, 76.0, {})
    s = result["summary"]
    assert s["healthy_ha"] == 0.0
    assert s["stressed_ha"] == 0.0


def test_format_recommendation_critical():
    rec = format_recommendation({"stressed": 35, "healthy": 20})
    assert "Critical" in rec
    assert "35.0%" in rec


def test_format_recommendation_warning():
    rec = format_recommendation({"stressed": 20, "healthy": 40})
    assert "Warning" in rec
    assert "20.0%" in rec


def test_format_recommendation_good():
    rec = format_recommendation({"stressed": 5, "healthy": 70})
    assert "Good" in rec
    assert "70.0%" in rec


def test_format_recommendation_moderate():
    rec = format_recommendation({"stressed": 10, "healthy": 40})
    assert "Moderate" in rec
