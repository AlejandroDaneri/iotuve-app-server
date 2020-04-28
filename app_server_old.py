import os
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
port = int(os.environ.get("PORT", 5000))


class Hello(Resource):
    def get(self):
        return 'Flask Dockerized and deployed to Heroku'


class Ping(Resource):
    def get(self):
        return "pong!", 200


api.add_resource(Hello, "/")
api.add_resource(Ping, "/ping")


#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=port)
