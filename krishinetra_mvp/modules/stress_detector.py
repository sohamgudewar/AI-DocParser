from typing import Any


def generate_stress_zones(lat: float, lon: float, ndvi_stats: dict[str, float]) -> dict[str, Any]:
    total_area_hectares = 10.0
    stressed_pct = ndvi_stats.get("stressed", 0)
    moderate_pct = ndvi_stats.get("moderate", 0)
    healthy_pct = ndvi_stats.get("healthy", 0)

    deg_step = 0.015
    offsets = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, -1), (1, -1), (-1, 1),
    ]
    labels = ["Healthy Zone", "Moderate Stress", "High Stress"]
    colors = ["#32CD32", "#FFD700", "#FF4444"]
    pcts = [healthy_pct, moderate_pct, stressed_pct]

    zones = []
    for i, (dx, dy) in enumerate(offsets):
        clat = lat + dx * deg_step
        clon = lon + dy * deg_step
        pct = pcts[i % 3]
        area_ha = round(total_area_hectares * pct / 100 / 3, 2)
        zone = {
            "type": "Feature",
            "properties": {
                "zone": labels[i % 3],
                "color": colors[i % 3],
                "area_ha": area_ha,
                "area_acres": round(area_ha * 2.471, 2),
                "severity": "high" if i % 3 == 2 else ("moderate" if i % 3 == 1 else "low"),
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [clon - 0.02, clat - 0.02],
                    [clon + 0.02, clat - 0.02],
                    [clon + 0.02, clat + 0.02],
                    [clon - 0.02, clat + 0.02],
                    [clon - 0.02, clat - 0.02],
                ]],
            },
        }
        zones.append(zone)

    if stressed_pct > 30:
        recommendation = "Immediate irrigation required"
    elif stressed_pct > 15:
        recommendation = "Monitor soil moisture"
    else:
        recommendation = "Crop health is good"

    return {
        "type": "FeatureCollection",
        "features": zones,
        "summary": {
            "total_analyzed_ha": round(total_area_hectares, 2),
            "healthy_ha": round(total_area_hectares * healthy_pct / 100, 2),
            "moderate_ha": round(total_area_hectares * moderate_pct / 100, 2),
            "stressed_ha": round(total_area_hectares * stressed_pct / 100, 2),
            "recommendation": recommendation,
        },
    }


def format_recommendation(ndvi_stats: dict[str, float]) -> str:
    s = ndvi_stats.get("stressed", 0)
    h = ndvi_stats.get("healthy", 0)
    if s > 30:
        return f"\u26a0\ufe0f **Critical**: {s:.1f}% stressed — immediate irrigation needed"
    elif s > 15:
        return f"\U0001f7e1 **Warning**: {s:.1f}% stressed — monitor soil moisture"
    elif h > 60:
        return f"\U0001f7e2 **Good**: {h:.1f}% healthy — crop thriving"
    else:
        return "\U0001f535 **Moderate**: Routine monitoring recommended"
