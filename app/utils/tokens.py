import secrets
from config import Config
from app import db


def generate_auth_code(user_id: int) -> str:
    """
    Генерация кода авторизации для пользователя
    
    :param user_id: ID пользователя
    :type user_id: int
    :return: Код авторизации
    :rtype: str
    """
    code: str = secrets.token_urlsafe(32)
    db.save_auth_code(code, user_id, Config.VERIFICATION_TOKEN_TTL)
    return code


def exchange_code(code: str) -> int | None:
    """
    Обмен кода авторизации на ID пользователя
    
    :param code: Код авторизации
    :type code: str
    :return: ID пользователя, если код авторизации валиден, иначе None
    :rtype: int | None
    """
    return db.pop_auth_code(code)


def generate_access_token(user_id: int) -> str:
    """
    Генерация токена доступа для пользователя
    
    :param user_id: ID пользователя
    :type user_id: int
    :return: Токен доступа
    :rtype: str
    """
    token: str = secrets.token_urlsafe(32)
    db.save_access_token(token, user_id, Config.ACCESS_TOKEN_TTL)
    return token


def validate_access_token(token: str) -> bool:
    """
    Проверка токена доступа
    
    :param token: Токен доступа
    :type token: str
    :return: True, если токен валиден, иначе False
    :rtype: bool
    """
    return db.validate_access_token(token)
