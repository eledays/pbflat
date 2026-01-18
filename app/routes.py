from sqlite3 import Row
from config import Config
from app.utils.tokens import validate_access_token
from app.db import get_any_user

from flask import Blueprint, jsonify, redirect, request, session, render_template, abort

import requests
from urllib.parse import urlencode
from uuid import uuid4

bp = Blueprint('main', __name__)


@bp.route('/v1.0/user/devices', methods=['GET'])
def yandex_devices():
    authorization: str | None = request.headers.get('Authorization')
    if authorization is None or ' ' not in authorization:
        return abort(403)
    
    access_token: str = authorization.split(' ')[1]
    if access_token is None or not validate_access_token(access_token):
        return abort(403)
    
    url: str = Config.BACKEND_URL + '/get_all_devices.php'
    responce: requests.Response = requests.get(url)

    print(responce.text, responce.status_code)

    if responce.status_code != 200:
        return jsonify({
            "message": "Internal server error"
        }), 500
    
    user: Row | None = get_any_user()
    if user is None:
        return jsonify({
            "message": "Internal server error"
        }), 500

    data = responce.json()
    data["payload"]["user_id"] = str(user["id"])
    return jsonify(data), 200


# @bp.route('/v1.0/user/query', methods=['POST'])
# def yandex_query():
#     data = request.json

#     devices = []
#     for d in data['devices']:
#         devices.append({
#             "id": d['id'],
#             "capabilities": [
#                 {
#                     "type": "devices.capabilities.on_off",
#                     "state": {
#                         "instance": "on",
#                         "value": True
#                     }
#                 }
#             ]
#         })

#     return jsonify({
#         "request_id": data['request_id'],
#         "payload": {
#             "devices": devices
#         }
#     })


# @bp.route('/v1.0/user/action', methods=['POST'])
# def yandex_action():
#     data = request.json

#     result = []
#     for d in data['payload']['devices']:
#         result.append({
#             "id": d['id'],
#             "capabilities": [
#                 {
#                     "type": "devices.capabilities.on_off",
#                     "state": {
#                         "instance": "on",
#                         "action_result": {
#                             "status": "DONE"
#                         }
#                     }
#                 }
#             ]
#         })

#     return jsonify({
#         "request_id": data['request_id'],
#         "payload": {
#             "devices": result
#         }
#     })


@bp.route('/health', methods=['GET'])
@bp.route('/v1.0', methods=['GET'])
def healthcheck():
    return 'ok', 200
