#!/usr/bin/python3
"""states view"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def all_states():
    """
        Returns list of all State objects.
    """
    states = []
    all_states = storage.all(State).values()
    for state in all_states:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """
        Get methode.
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """DELETE method """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    POST Methode
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    state = State(**data)
    state.save()
    state = state.to_dict()
    return make_response(jsonify(state), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """PUT method """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    state = state.to_dict()
    return make_response(jsonify(state), 200)
