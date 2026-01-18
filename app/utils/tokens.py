import secrets
from config import Config
from app import db


def generate_auth_code(user_id: int) -> str:
    code = secrets.token_urlsafe(32)
    db.save_auth_code(code, user_id, Config.VERIFICATION_TOKEN_TTL)
    return code


def exchange_code(code: str) -> int | None:
    return db.pop_auth_code(code)


def generate_access_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    db.save_access_token(token, user_id, Config.ACCESS_TOKEN_TTL)
    return token
