from config import Config

from cryptography.fernet import Fernet, InvalidToken
import requests

import time
from logging import getLogger
import os

logger = getLogger(__name__)


def save_refresh_token(refresh_token):
    """Шифрование и сохранение refresh_token"""
    if Config.SECRET_KEY is None:
        logger.error('SECRET_KEY is not set')
        raise ValueError('SECRET_KEY is not set')

    f = Fernet(Config.SECRET_KEY)
    encrypted_token = f.encrypt(refresh_token.encode())
    with open(Config.REFRESH_TOKEN_FILE, 'wb') as f:
        f.write(encrypted_token)


def get_refresh_token():
    """Чтение и расшифровка refresh_token"""
    if Config.SECRET_KEY is None:
        logger.error('SECRET_KEY is not set')
        raise ValueError('SECRET_KEY is not set')

    if not os.path.exists(Config.REFRESH_TOKEN_FILE):
        logger.error(f'{Config.REFRESH_TOKEN_FILE} не найден')
        raise ValueError(f'{Config.REFRESH_TOKEN_FILE} не найден')

    with open(Config.REFRESH_TOKEN_FILE, 'rb') as f:
        encrypted_token = f.read()

    f = Fernet(Config.SECRET_KEY)
    try:
        decrypted_token = f.decrypt(encrypted_token)
    except InvalidToken:
        logger.error('Неверный ключ шифрования')
        raise ValueError('Неверный ключ шифрования')
    return decrypted_token.decode()


def refresh_access_token():
    """Обновление access_token"""
    REFRESH_TOKEN = get_refresh_token()

    response = requests.post("https://oauth.yandex.ru/token", data={
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET
    })
    data = response.json()

    ACCESS_TOKEN = data.get('access_token')
    EXPIRES_IN = data.get('expires_in')

    if ACCESS_TOKEN is None:
        logger.error('Не удалось получить access_token')
        raise ValueError('Не удалось получить access_token')

    if EXPIRES_IN is None:
        logger.error('Не удалось получить expires_in')
        raise ValueError('Не удалось получить expires_in')

    Config.ACCESS_TOKEN = ACCESS_TOKEN
    Config.ACCESS_TOKEN_EXPIRES_AT = time.time() + data['expires_in'] - 5

    logger.info('Обновлен access_token')


def get_access_token():
    """Получение access_token и обновление в случае, если истек"""
    if Config.ACCESS_TOKEN is None or time.time() >= Config.ACCESS_TOKEN_EXPIRES_AT:
        refresh_access_token()
    logger.info('Получен access_token')
    return Config.ACCESS_TOKEN
