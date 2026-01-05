from flask import Blueprint, jsonify, redirect, request, session

from config import Config

import requests
from urllib.parse import urlencode

bp = Blueprint('auth', __name__)


@bp.route('/oauth/login', methods=['GET'])
def oauth_login():
    params = {
        'response_type': 'code',
        'client_id': Config.CLIENT_ID,
        'redirect_uri': Config.REDIRECT_URI,
        'scope': 'iot:view iot:control'
    }
    url = 'https://oauth.yandex.ru/authorize?' + urlencode(params)
    return redirect(url)


@bp.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return 'No code', 400

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': Config.CLIENT_ID,
        'client_secret': Config.CLIENT_SECRET
    }

    r = requests.post('https://oauth.yandex.ru/token', data=data)
    token = r.json()

    # ⚠️ В реальном проекте — сохранить по user_id
    session['access_token'] = token.get('access_token')

    return 'OAuth OK, you can close this page'