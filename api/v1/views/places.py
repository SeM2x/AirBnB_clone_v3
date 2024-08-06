#!/usr/bin/python3
"""places view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, description='Missing name')

    place = Place(**data)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, description='Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """Search for places"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, description='Not a JSON')
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    if not states and not cities and not amenities:
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places)
    places = []
    # for place in storage.all(Place).values():

    for state in states:
        for city in storage.all(City).values():
            if city.state_id == state:
                for place in city.places:
                    for amenity in amenities:
                        if amenity not in [amenity.id for
                                           amenity in place.amenities]:
                            break
                    else:
                        if place not in places:
                            places.append(place)

    for city in cities:
        city = storage.get(City, city)
        if city:
            for place in city.places:
                for amenity in amenities:
                    if amenity not in [amenity.id for
                                       amenity in place.amenities]:
                        break
                else:
                    if place not in places:
                        places.append(place)

    return jsonify([place.to_dict() for place in places])
