from app.db import get_any_user
from app.utils.tokens import generate_auth_code, exchange_code, generate_access_token
from config import Config

from flask import Blueprint, jsonify, redirect, request, abort

bp = Blueprint('auth', __name__)


@bp.route("/oauth/authorize", methods=["GET"])
def authorize():
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")
    state = request.args.get("state")

    if client_id != Config.OAUTH_CLIENT_ID:
        print('Invalid client_id')
        abort(400)

    user = get_any_user()
    if not user:
        abort(500)

    code = generate_auth_code(user["id"])
    return redirect(f"{redirect_uri}?code={code}&state={state}")


@bp.route("/oauth/token", methods=["POST"])
def token():
    if (
        request.form.get("client_id") != Config.OAUTH_CLIENT_ID
        or request.form.get("client_secret") != Config.OAUTH_CLIENT_SECRET
        or request.form.get("grant_type") != "authorization_code"
    ):
        abort(400)

    code = request.form.get("code")
    if code is None:
        abort(400)

    user_id = exchange_code(code)
    if not user_id:
        abort(400)

    access_token = generate_access_token(user_id)
    return jsonify(
        {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": Config.ACCESS_TOKEN_TTL,
        }
    )
