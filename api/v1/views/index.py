#!/usr/bin/python3
"""
create a route /status
"""
from api.v1.views import app_views
from flask import jsonify
@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON"""
    return jsonify({"status": "OK"})