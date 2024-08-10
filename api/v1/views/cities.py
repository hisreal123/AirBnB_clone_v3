#!/usr/bin/python3
"""
View for Cities that handles all RESTful API actions.
"""

from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State  # Ensure State model is imported
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_all(state_id):
    """Returns a list of all City objects linked to a given State."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities_all = [city.to_dict() for city in state.cities]
    return jsonify(cities_all)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def city_get(city_id):
    """Handles GET method for a single City."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    """Handles DELETE method for a single City."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """Handles POST method to create a new City."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if 'name' not in data:
        return abort(400, "Missing name")
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """Handles PUT method to update a City."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)  # Use setattr to update attributes
    city.save()
    return jsonify(city.to_dict()), 200
