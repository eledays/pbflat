import secrets
import time

_codes = {}
_tokens = {}


def generate_code(user_id: str) -> str:
    code = secrets.token_urlsafe(32)
    _codes[code] = {
        "user_id": user_id,
        "expires": time.time() + 300  # 5 минут
    }
    return code


def exchange_code(code: str):
    data = _codes.pop(code, None)
    if not data or data["expires"] < time.time():
        return None
    return data["user_id"]


def generate_token(user_id: str):
    access_token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(32)

    _tokens[access_token] = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }

    return access_token, refresh_token


def validate_token(token: str):
    data = _tokens.get(token)
    if not data or data["expires"] < time.time():
        return None
    return data["user_id"]
