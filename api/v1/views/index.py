#!/usr/bin/python3
"""
    Creates app views
"""

from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def api_status():
    """
    """
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """

    """
    stats = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }

    return jsonify(stats)
