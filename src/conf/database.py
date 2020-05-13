from flask_mongoengine import MongoEngine
from src.conf import MONGODB_SETTINGS

db = MongoEngine()


def init_db(app):
    app.config["MONGODB_SETTINGS"] = MONGODB_SETTINGS
    db.init_app(app)
