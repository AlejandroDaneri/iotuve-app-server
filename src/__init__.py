import time
from flask import Flask, g, request
from flask_restful import Api
from flask_cors import cross_origin


def create_app():
    app = Flask(__name__)

    with app.app_context():

        api = Api(app)

        from src.misc.requests import request_id, is_admin, user_agent
        from src.conf.database import init_db
        from src.conf.jobs import init_jobs
        from src.conf.routes import init_routes

        init_db(app)
        init_jobs(app)
        init_routes(api)

    @app.before_request
    def before_request():
        g.start = time.time()
        g.request_id = None  # value initialized on request_id()
        g.user_agent = None  # value initialized on user_agent()
        g.session_token = None  # values initialized on check_token()
        g.session_admin = None  # values initialized on is_admin()
        request_id()
        user_agent()
        is_admin()

    @app.after_request
    @cross_origin()
    def after_request(response):
        import datetime
        from src.conf import APP_VERSION
        from src.models.stat import Stat
        diff = time.time() - g.start
        stat = Stat(
            timestamp=datetime.datetime.fromtimestamp(g.start),
            version=APP_VERSION,
            status=response.status_code,
            time=diff,
            request_id=g.request_id,
            remote_ip=request.remote_addr,
            method=request.method,
            host=str(request.host.split(":", 1)[0]),
            path=request.path,
            full_path=request.full_path,
            headers=request.headers)
        stat.save()
        response.headers.add('X-Request-ID', g.request_id)
        return response

    return app
