#!/usr/bin/python3

"""
Create Flask app app_views
"""
from flask import jsonify
from api.v1.views import app_view

@app_view.route('/status')
def api_status():
    """
    
    """

    response = {'status' : "OK"}
    return jsonify(response)
