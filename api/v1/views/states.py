from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """Returns a list of all State objects."""
    states_all = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states_all)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_get(state_id):
    """Handles GET method for a specific State."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_delete(state_id):
    """Handles DELETE method for a specific State."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """Handles POST method to create a new State."""
    data = request.get_json()
    if data is None:
        return abort(400, description="Not a JSON")
    if 'name' not in data:
        return abort(400, description="Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """Handles PUT method to update a State."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
