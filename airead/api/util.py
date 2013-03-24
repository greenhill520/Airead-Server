from flask import jsonify, request
from flask import current_app as app
import json

def api_response(success, data=None, error_code=None, error_message=None):
    if success is True:
        if data is not None:
            return jsonify(success=True, data=data)
        else:
            return jsonify(success=True)
    else:
        return jsonify(success=False, error_code=error_code,
                error_message=error_message)


def get_request_json():
    info = None
    if hasattr(request, "json") and request.json is not None:
        info = json.loads(request.json)
        return info
    if hasattr(request, "data") and request.data is not None:
        info = json.loads(request.data)
        return info
    return None
