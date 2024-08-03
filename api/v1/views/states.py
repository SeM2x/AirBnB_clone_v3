#!/usr/bin/python3
"""
    Creates states
"""
from flask import jsonify
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