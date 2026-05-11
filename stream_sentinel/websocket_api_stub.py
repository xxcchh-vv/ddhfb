from flask import Blueprint, jsonify

from ws_log_stub import runtime_logs

websocket_stub = Blueprint('websocket_stub', __name__)


@websocket_stub.route('/api/runtime-logs')
def runtime_log_feed():
    return jsonify(runtime_logs.dump())
