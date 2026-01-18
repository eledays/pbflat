from cryptography.fernet import Fernet

from dotenv import load_dotenv
import os
import time
from pathlib import Path

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
    OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')

    REFRESH_TOKEN_FILE = 'refresh_token.enc'

    ACCESS_TOKEN_TTL = 3600
    REFRESH_TOKEN_TTL = 60 * 60 * 24 * 30
    VERIFICATION_TOKEN_TTL = 300

    BACKEND_URL: str = os.getenv('BACKEND_URL', 'http://192.168.0.10/sf')

    BASE_DIR: Path = Path(__file__).resolve().parent
    DB_PATH: Path = BASE_DIR / "app.db"

