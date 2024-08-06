#!/usr/bin/python3
"""
Create a route /status
"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON response ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Returns stats (number of objects by type)"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats), 200


if __name__ == "__main__":
    pass
