import os

API_AUTH_CLIENT_ID = "407f7dbf-57d5-4aea-bfbd-d317ae872428"
API_MEDIA_CLIENT_ID = "407f7dbf-57d5-4aea-bfbd-d317ae872428"

API_AUTH_CLIENT_URL = 'https://fiuba-taller-2-auth-server-st.herokuapp.com/api/v1/'
API_MEDIA_CLIENT_URL = 'https://fiuba-taller-2-auth-server-st.herokuapp.com/api/v1/'

APP_HOST = '0.0.0.0'
APP_PORT = str(os.environ.get("APP_PORT", os.environ.get("PORT", 8000)))
APP_DEBUG = os.environ.get("APP_DEBUG", True)
APP_PREFIX = "/api/v1"

LOG_LEVEL = str(os.environ.get("GUNICORN_LOG_LEVEL", "debug"))

MONGO_URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':' + os.environ['MONGODB_PORT'] + '/' + os.environ['MONGODB_DATABASE'] + '?retryWrites=false'
