import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-development-key")
    DATABASE_PATH = str(BASE_DIR / "database" / "cybersakhi.db")
