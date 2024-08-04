#!/usr/bin/python3
from . import app_views
from flask import jsonify, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    res = jsonify({})
    res.status_code = 200
    return res


@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """"""
    res = jsonify()
    res.status_code = 404
    return {res}


@app_views.route('/cities/<city_id>', methods=['PUT'])
def delete_city(city_id):
    """"""
    res = jsonify()
    res.status_code = 404
    return {res}
