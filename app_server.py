#Chotuve - App Server
#Flask + MongoDB - on Gunicorn

#Basado en:
#https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3
#https://medium.com/@riken.mehta/full-stack-tutorial-flask-react-docker-ee316a46e876

#Importacion de librerias necesarias
#OS para leer variables de entorno y logging para escribir los logs
import os, logging, datetime, json
#Flask, para la implementacion del servidor REST
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse
#PyMongo para el manejo de MongoDB
from flask_pymongo import PyMongo

#Version de API y Server
api_version = "1"
server_version = "1.00"

#Agregamos un root para todos los enpoints, con la api version
api_path = "/api/v" + api_version

#Inicializacion de la api
app = Flask(__name__)
api = Api(app)

#Inicializacion de la base de datos, MongoDB
app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + os.environ['MONGODB_DATABASE'] + '?retryWrites=false'
mongo = PyMongo(app)
db = mongo.db
cl = mongo.cx

#Inicializacion de logs - para cuando ejecuta gunicorn + flask
#Ejemplos de logs, para los distintos niveles
#app.logger.debug('This is a DEBUG message!')
#app.logger.info('This is an INFO message!')
#app.logger.warning('This is a WARNING message!')
#app.logger.error('This is an ERROR message!')
#app.logger.critical('This is a CRITICAL message!')
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

#Clase que muestra la info del server, en la home '/'
class Home(Resource):
    def get(self):
        homeResponseGet = "fiuba-taller-2-app-server-v" + server_version
        app.logger.info('Displaying home with server information.')
        app.logger.debug(homeResponseGet)
        app.logger.info("Returned HTTP: " + str(200))
        return homeResponseGet, 200

#Clase que testea la conexion a la base de datos
class TestDB(Resource):
    def get(self):
        app.logger.info('Database info requested.')        
        testDBResponseGet = {
            "code": 0,
            "message": "Server information: " + str(cl.server_info()),
            "data:": None
        }
        app.logger.debug(testDBResponseGet)
        app.logger.info("Returned HTTP: " + str(200))
        return testDBResponseGet, 200

#Clase que devuelve el ping del servidor
class Ping(Resource):
    def get(self):
        app.logger.info('Ping requested.')        
        app.logger.info("Returned HTTP: " + str(200))
        return "Pong!", 200


#Defincion de los endpoints del server
api.add_resource(Home, "/")
api.add_resource(Ping, api_path + "/ping")      
api.add_resource(TestDB, api_path + "/testdb")

# Inicio del server en forma directa - toma el puerto y modo de las variables de entorno
# PORT
# APP_DEBUG - "True, False" 
if __name__ == '__main__':
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", os.environ.get("PORT", 8000), os.environ.get("APP_DEBUG", True))
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT)
