import os
from typing import Optional, Any
import json

from dotenv import load_dotenv
from .logger import get_logger

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

logger = get_logger(__name__)

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "krishinetra_v2"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

_conn = None


def get_connection():
    global _conn
    if _conn is not None:
        try:
            _conn.cursor().execute("SELECT 1")
            return _conn
        except Exception:
            _conn = None

    try:
        import psycopg2
        import psycopg2.extras
        _conn = psycopg2.connect(**DB_CONFIG)
        _conn.autocommit = True
        logger.info("Connected to PostgreSQL database")
        return _conn
    except Exception as e:
        logger.warning("Database unavailable: %s — running without DB", e)
        return None


def db_available() -> bool:
    return get_connection() is not None


def execute(query: str, params: tuple = ()) -> Optional[Any]:
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                return cur.fetchall()
            return None
    except Exception as e:
        logger.error("Query failed: %s — %s", query[:80], e)
        return None


def insert_analysis(
    field_name: str,
    crop_type: str,
    crop_variety: str,
    ndvi_stats: dict[str, float],
    recommendation: str,
    lat: float,
    lon: float,
) -> bool:
    field = execute(
        "SELECT id FROM fields WHERE name = %s", (field_name,)
    )
    if not field:
        execute(
            "INSERT INTO fields (name, location) VALUES (%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))",
            (field_name, lon, lat),
        )
        field_id = execute(
            "SELECT id FROM fields WHERE name = %s", (field_name,)
        )
        if not field_id:
            return False
        field_id = field_id[0][0]
    else:
        field_id = field[0][0]

    execute(
        """INSERT INTO analysis
           (field_id, crop_type, crop_variety, ndvi_avg, ndvi_healthy,
            ndvi_moderate, ndvi_stressed, recommendation)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (field_id, crop_type, crop_variety, ndvi_stats.get("avg_ndvi"),
         ndvi_stats.get("healthy"), ndvi_stats.get("moderate"),
         ndvi_stats.get("stressed"), recommendation),
    )
    return True


def insert_land_record(record: dict) -> bool:
    if not record.get("owner_name"):
        logger.warning("Cannot insert land record without owner_name")
        return False
    execute(
        """INSERT INTO land_records
           (owner_name, survey_number, area_hectares, crop_type,
            gps_coordinates, district, taluka, village, irrigation_type)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (record.get("owner_name"), record.get("survey_number"),
         record.get("area_hectares"), record.get("crop_type"),
         record.get("gps_coordinates"), record.get("district"),
         record.get("taluka"), record.get("village"),
         record.get("irrigation_type")),
    )
    return True
