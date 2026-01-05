from cryptography.fernet import Fernet

from dotenv import load_dotenv
import os
import time

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI')

    REFRESH_TOKEN_FILE = 'refresh_token.enc'

    ACCESS_TOKEN = None
    ACCESS_TOKEN_EXPIRES_AT = 0


assert Config.SECRET_KEY is not None
assert Config.CLIENT_ID is not None
assert Config.CLIENT_SECRET is not None
assert Config.REDIRECT_URI is not None