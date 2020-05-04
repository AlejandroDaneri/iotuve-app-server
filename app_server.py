import os
import logging
from src import create_app

app = create_app()

# Inicializacion de logs - para cuando ejecuta gunicorn + flask
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    # Inicio del server en forma directa
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", os.environ.get("PORT", 8000), os.environ.get("APP_DEBUG", True))
    app.run(host='0.0.0.0', port=os.environ.get("APP_PORT", os.environ.get("PORT", 8000)))
