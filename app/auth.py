from app.db import get_any_user
from app.utils.tokens import generate_auth_code, exchange_code, generate_access_token
from config import Config

from flask import Blueprint, jsonify, redirect, request, abort
from sqlite3 import Row

bp = Blueprint('auth', __name__)


@bp.route("/oauth/authorize", methods=["GET"])
def authorize():
    """
    Получение кода авторизации
    """

    client_id: str | None = request.args.get("client_id")
    redirect_uri: str | None = request.args.get("redirect_uri")
    state: str | None = request.args.get("state")

    # Проверка, что client_id совпадает с правильным
    if client_id != Config.OAUTH_CLIENT_ID:
        print('Invalid client_id')
        abort(400)

    # Получение любого пользователя из БД
    user: Row | None = get_any_user()
    if user is None:
        abort(500)

    # Генерация кода авторизации
    code: str = generate_auth_code(user["id"])

    # Перенаправление на redirect_uri с кодом авторизации
    return redirect(f"{redirect_uri}?code={code}&state={state}")


@bp.route("/oauth/token", methods=["POST"])
def token():
    """
    Обмен кода авторизации на токен доступа
    """

    client_id: str | None = request.form.get("client_id")
    client_secret: str | None = request.form.get("client_secret")
    grant_type: str | None = request.form.get("grant_type")

    # Проверка, что все параметры переданы и совпадают с правильными значениями
    if (
        client_id != Config.OAUTH_CLIENT_ID
        or client_secret != Config.OAUTH_CLIENT_SECRET
        or grant_type != "authorization_code"
    ):
        print(f'Invalid parameters: {client_id = }, {client_secret = }, {grant_type = }')
        abort(400)

    code: str | None = request.form.get("code")
    if code is None:
        print('Code is not provided')
        abort(400)

    # Обмен кода авторизации на id пользователя
    user_id: int | None = exchange_code(code)
    if not user_id:
        print('Invalid code')
        abort(400)

    # Генерация токена доступа
    access_token: str = generate_access_token(user_id)

    return jsonify(
        {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": Config.ACCESS_TOKEN_TTL,
        }
    )
