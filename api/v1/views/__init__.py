#!/usr/bin/python3

"""
    Createview Flask app
"""

from flask import Blueprint

app_view = Blueprint('app_views', __name__,url_prefix='/api/v1')

from api.v1.views.index import *
