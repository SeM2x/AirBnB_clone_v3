#!/usr/bin/python3
"""Creates a flask app"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": ["0.0.0.0"], }})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """handler for 404 errors"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HOST, port=PORT, threaded=True)
