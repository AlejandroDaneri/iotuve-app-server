import os
import logging
from flask import Flask, g
from flask_restful import Api
from flask_pymongo import PyMongo

api_version = "1"
api_name = "fiuba-taller-2-app-server-v" + api_version
api_path = "/api/v" + api_version

def create_app():
    app = Flask(__name__)

    api = Api(app)

    app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
        'MONGODB_PASSWORD'] + '@' + \
                              os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + os.environ[
                                  'MONGODB_DATABASE'] + '?retryWrites=false'
    mongo = PyMongo(app)
    app.db = mongo.db
    app.cl = mongo.cx

    from .resources.routes import initialize_routes

    initialize_routes(api, api_path)

    return app
