import os
import hashlib
from typing import Optional

from dotenv import load_dotenv
from .logger import get_logger
from .database import execute, db_available

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

logger = get_logger(__name__)

DEMO_USERS = {
    "admin@krishinetra.in": {"name": "Admin", "role": "admin"},
    "farmer@demo.in": {"name": "Demo Farmer", "role": "farmer"},
}


def hash_email(email: str) -> str:
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()[:16]


def authenticate(email: str) -> Optional[dict]:
    email = email.lower().strip()
    if "@" not in email or "." not in email:
        return None

    if email in DEMO_USERS:
        user = DEMO_USERS[email].copy()
    else:
        user = {"name": email.split("@")[0], "role": "farmer"}

    user["email"] = email
    user["id"] = hash_email(email)

    if db_available():
        try:
            existing = execute("SELECT id, name FROM users WHERE email = %s", (email,))
            if not existing:
                execute(
                    "INSERT INTO users (email, name) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                    (email, user["name"]),
                )
            else:
                user["name"] = existing[0][1] or user["name"]
        except Exception as e:
            logger.warning("DB user lookup failed: %s", e)

    return user
