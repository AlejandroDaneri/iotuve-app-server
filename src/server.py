from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Hello(Resource):
    def get(self):
        return 'Flask Dockerized and deployed to Heroku'


class Ping(Resource):
    def get(self):
        return "pong!", 200


api.add_resource(Hello, "/")
api.add_resource(Ping, "/ping")
