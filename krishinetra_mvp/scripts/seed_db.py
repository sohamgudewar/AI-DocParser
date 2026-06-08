"""Migrate JSON data to PostgreSQL. Run after db is up: python scripts/seed_db.py"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.database import execute, get_connection

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOKUP_PATH = os.path.join(BASE, "data", "crop_lookup.json")


def seed_crop_zones():
    try:
        with open(LOOKUP_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("crop_lookup.json not found — skipping seed")
        return

    zones = data.get("zones", [])
    for zone in zones:
        lat_min, lat_max = zone["lat_range"]
        lon_min, lon_max = zone["lon_range"]
        execute(
            """INSERT INTO crop_zones
               (region, crop, variety, growing_season, lat_min, lat_max, lon_min, lon_max, emoji)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT DO NOTHING""",
            (zone["region"], zone["crop"], zone["typical_variety"],
             zone["growing_season"], lat_min, lat_max, lon_min, lon_max,
             zone.get("emoji")),
        )
    print(f"Seeded {len(zones)} crop zones")


def main():
    conn = get_connection()
    if not conn:
        print("Database not available. Is PostgreSQL running?")
        sys.exit(1)
    seed_crop_zones()
    print("Seed complete")


if __name__ == "__main__":
    main()
