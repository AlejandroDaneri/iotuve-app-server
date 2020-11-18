import os

API_AUTH_CLIENT_ID = os.environ.get("API_AUTH_CLIENT_ID", "")
API_MEDIA_CLIENT_ID = os.environ.get("API_MEDIA_CLIENT_ID", "")
API_FIREBASE_KEY = os.environ.get("API_FIREBASE_KEY", "")

API_AUTH_CLIENT_URL = os.environ.get("API_AUTH_CLIENT_URL", "https://fiuba-taller-2-auth-server-st.herokuapp.com/api/v1/")
API_MEDIA_CLIENT_URL = os.environ.get("API_MEDIA_CLIENT_URL", "https://fiuba-taller-2-media-server-st.herokuapp.com/api/v1/")
API_FIREBASE_CLIENT_URL = os.environ.get("API_FIREBASE_CLIENT_URL", "https://fcm.googleapis.com/fcm/send")

APP_VERSION = "v1"
APP_NAME = "Choutuve Application Server API (%s)" % APP_VERSION.upper()
APP_HOST = '0.0.0.0'
APP_PORT = str(os.environ.get("APP_PORT", os.environ.get("PORT", 8000)))
APP_DEBUG = os.environ.get("APP_DEBUG", True)
APP_PREFIX = "/api/" + APP_VERSION

LOG_LEVEL = str(os.environ.get("GUNICORN_LOG_LEVEL", "debug"))

MONGO_DB = os.environ.get('MONGODB_DATABASE', 'app-server-db')
MONGO_HOST = os.environ.get('MONGODB_HOSTNAME', 'app-server-mongodb')
MONGO_PORT = os.environ.get('MONGODB_PORT', '27017')
MONGO_USERNAME = os.environ.get('MONGODB_USERNAME', 'appserveruser')
MONGO_PASSWORD = os.environ.get('MONGODB_PASSWORD', '123456')

MONGO_URI = 'mongodb+srv://' + MONGO_USERNAME + ':' + MONGO_PASSWORD + '@' + MONGO_HOST + '/' + MONGO_DB + '?retryWrites=false'

MONGODB_SETTINGS = {
    'host': MONGO_URI
}
