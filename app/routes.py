from flask import Blueprint, jsonify, redirect, request, session

from config import Config

import requests
from urllib.parse import urlencode
from uuid import uuid4

bp = Blueprint('main', __name__)

# =======================
# OAuth
# =======================


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


# =======================
# Yandex Smart Home API
# =======================

@bp.route('/v1.0/user/devices', methods=['GET'])
def yandex_devices():
    return jsonify({
        "request_id": str(uuid4()),
        "payload": {
            "devices": [
                {
                    "id": "lamp-1",
                    "name": "Свет в коридоре",
                    "type": "devices.types.light",
                    "capabilities": [
                        {
                            "type": "devices.capabilities.on_off",
                            "retrievable": True,
                            "parameters": {}
                        }
                    ]
                }
            ]
        }
    })


@bp.route('/v1.0/user/query', methods=['POST'])
def yandex_query():
    data = request.json

    devices = []
    for d in data['devices']:
        devices.append({
            "id": d['id'],
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "state": {
                        "instance": "on",
                        "value": True
                    }
                }
            ]
        })

    return jsonify({
        "request_id": data['request_id'],
        "payload": {
            "devices": devices
        }
    })


@bp.route('/v1.0/user/action', methods=['POST'])
def yandex_action():
    data = request.json

    result = []
    for d in data['payload']['devices']:
        result.append({
            "id": d['id'],
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "state": {
                        "instance": "on",
                        "action_result": {
                            "status": "DONE"
                        }
                    }
                }
            ]
        })

    return jsonify({
        "request_id": data['request_id'],
        "payload": {
            "devices": result
        }
    })


# =======================
# Service
# =======================

@bp.route('/health', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"})
