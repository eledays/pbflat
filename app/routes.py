from config import Config

from flask import Blueprint, jsonify, redirect, request, session, render_template

import requests
from urllib.parse import urlencode
from uuid import uuid4

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    try:
        return render_template('index.html', logged_in=True)
    except ValueError:
        return render_template('index.html', logged_in=False)


@bp.route('/v1.0/user/devices', methods=['GET'])
def yandex_devices():
    print(request.headers)
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


@bp.route('/health', methods=['GET'])
@bp.route('/v1.0', methods=['GET'])
def healthcheck():
    return 'ok', 200
