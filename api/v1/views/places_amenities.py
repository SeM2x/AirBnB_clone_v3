#!/usr/bin/python3
"""place amenities view"""

from . import app_views
from flask import abort, jsonify, make_response
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities", strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if storage_t == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = place.amenity_ids
    return jsonify(amenities)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if storage_t == "db":
        linked = amenity.id in [obj.id for obj in place.amenities]
    else:
        linked = amenity.id in place.amenity_ids
    if not linked:
        abort(404)
    if storage_t == "db":
        place.amenities = [a for a in place.amenities if a.id != amenity.id]
    else:
        place.amenity_ids = [a for a in place.amenity_ids if a != amenity.id]

    place.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if storage_t == "db":
        linked = amenity.id in [obj.id for obj in place.amenities]
    else:
        linked = amenity.id in place.amenity_ids
    if linked:
        return make_response(jsonify(amenity.to_dict()), 200)

    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
