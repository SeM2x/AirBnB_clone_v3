#!/usr/bin/python3

"""
    App
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_view

app = Flask(__name__)

app.register_blueprint(app_view)


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST','0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT','5000'))
    app.run(host=HOST, port=PORT,threaded=True)
