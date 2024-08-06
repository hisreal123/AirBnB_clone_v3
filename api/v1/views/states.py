""" new view for State objects that handles all default RESTFul API actions """

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ get all states """
    states = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ get states by id """
    state = storage.get("State", state_id)
    if not state or None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(state_id):
    """ delete state by id """
    state = storage.get("State", state_id)
    if not state or state_id is None:
        abort(404)
    state.delete()
    state.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response((state.to_dict()), 2001)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_to_state(state_id):
    """ update state by id """
    state = storage.get("State", state_id)
    if state is None or not state_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'created_at', 'updated_at']:
            setattr(state, value, attribute)
    state.save()
    return jsonify(state.to_dict())
