import logging.config
from src import create_app
from src.conf import APP_HOST, APP_PORT, APP_DEBUG
from src.conf.log import LOG_CONFIG

app = create_app()

# Inicializacion de logs - para cuando ejecuta gunicorn + flask
if __name__ != '__main__':
    logging.config.dictConfig(LOG_CONFIG)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    # Inicio del server en forma directa
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
