#!/usr/bin/python3
"""Places reviews view"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def list_all_review_of_places(place_id):
    """List of all Place objects of a City"""
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    list_reviews = [obj.to_dict() for obj in storage.all("Review").values()
                    if place_id == obj.place_id]
    return jsonify(list_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Creates a Review'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    id_user = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing id_usertext')
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == id_user]
    if user_obj == []:
        abort(404)
    reviews = []
    new_review = Review(text=request.json['text'], place_id=place_id,
                        user_id=id_user)
    storage.new(new_review)
    storage.save()
    reviews.append(new_review.to_dict())
    return make_response(jsonify(reviews[0]), 201)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    '''Get a Review object '''
    all_reviews = storage.all("Review").values()
    obj_review = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if obj_review == []:
        abort(404)
    return make_response(jsonify(obj_review[0]))


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''Deletes a Review object'''
    all_reviews = storage.all("Review").values()
    obj_review = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if obj_review == []:
        abort(404)
    obj_review.remove(obj_review[0])
    for obj in all_reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    '''Updates a Review object'''
    all_reviews = storage.all("Review").values()
    obj_review = [obj.to_dict() for obj in all_reviews if obj.id == review_id]
    if obj_review == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' in request.get_json():
        obj_review[0]['text'] = request.json['text']
        for obj in all_reviews:
            if obj.id == review_id:
                obj.text = request.json['text']
        storage.save()
    return make_response(jsonify(obj_review[0]), 200)
