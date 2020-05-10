import os
import time
from flask import Flask, g, request
from flask_restful import Api
from flask_pymongo import PyMongo
from src.conf import APP_PREFIX, MONGO_URI

mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = MONGO_URI

    api = Api(app, prefix=APP_PREFIX)
    mongo.init_app(app)

    from src.misc.requests import request_id
    from src.conf.routes import init_routes

    init_routes(api)

    @app.before_request
    def before_request():
        g.start = time.time()
        g.session_token = None  # value initialized on check_token
        request_id()

    @app.after_request
    def after_request(response):
        diff = time.time() - g.start
        mongo.db.server_stats.insert_one({
            "status": response.status_code,
            "time": diff,
            "full_path": request.full_path,
            "request_id": g.request_id,
            "timestamp": g.start
        })
        response.headers.add('X-Request-ID', g.request_id)
        return response

    mongo.db.server_stats.delete_many({})

    return app
