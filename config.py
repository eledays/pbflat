from cryptography.fernet import Fernet

from dotenv import load_dotenv
import os
import time
from pathlib import Path

load_dotenv()

class Config:
    BASE_DIR = Path(__file__).resolve().parent

    SECRET_KEY = os.getenv('SECRET_KEY')
    OAUTH_CLIENT_ID = os.getenv('CLIENT_ID')
    OAUTH_CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    REFRESH_TOKEN_FILE = 'refresh_token.enc'

    ACCESS_TOKEN_TTL = 3600
    REFRESH_TOKEN_TTL = 60 * 60 * 24 * 30
