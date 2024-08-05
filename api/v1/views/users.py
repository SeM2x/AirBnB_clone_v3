#!/usr/bin/python3
"""Users view"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def all_users():
    """ returns list of all User objects """
    all_users = []
    users = storage.all("User").values()
    for user in users:
        all_users.append(user.to_json())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """ GET method """
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """DELETE method """
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """POST method """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """PUT method """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "email", "created_at", "updated_at"]
        if key not in ignore_keys:
            user.bm_update(key, value)
    user.save()
    user = user.to_dict()
    return make_response(jsonify(user), 200)
