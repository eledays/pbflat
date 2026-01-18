from app.utils.tokens import get_refresh_token, save_refresh_token, delete_tokens
from config import Config

from flask import Blueprint, jsonify, redirect, request, session, url_for

import requests
from urllib.parse import urlencode

bp = Blueprint('auth', __name__)


@bp.route('/oauth/login', methods=['GET'])
def oauth_login():
    params = {
        'response_type': 'code',
        'client_id': Config.OAUTH_CLIENT_ID,
        'redirect_uri': '/oauth/yandex/callback',
        'scope': 'iot:view iot:control'
    }
    url = 'https://oauth.yandex.ru/authorize?' + urlencode(params)
    return redirect(url)


@bp.route('/oauth/yandex/callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return 'No code', 400

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': Config.OAUTH_CLIENT_ID,
        'client_secret': Config.OAUTH_CLIENT_SECRET
    }

    r = requests.post('https://oauth.yandex.ru/token', data=data)
    data = r.json()

    access_token = data.get('access_token')
    if not access_token:
        return 'No access token', 400

    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return 'No refresh token', 400
    
    save_refresh_token(refresh_token)

    return redirect('https://pbflat.ru/user.php')


@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    delete_tokens()
    return redirect('/')