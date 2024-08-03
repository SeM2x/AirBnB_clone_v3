#!/usr/bin/python3
"""
    Creates states
"""
from flask import jsonify,abort,request
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.routes('/states', strict_slashes=False)
def all_states():
    """
        Returns list of all State objects.
    """
    states = []
    all_states = storage.all("State").values()
    for state in all_states:
        states.append(state.to_json())
    return jsonify(states)

@app_views.routes('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """
        Get methode.
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """DELETE method """
    empty_dict = {}
    state = storage.get("State", state_id)
    if state:
        storage.delete()
        storage.save()
        return jsonify([]), 200
    else:
        abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state(state_id):
    """
    POST Methode
    """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_json()
    return jsonify(state), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """PUT method """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            state.bm_update(key, value)
    state.save()
    state = state.to_json()
    return jsonify(state), 200
