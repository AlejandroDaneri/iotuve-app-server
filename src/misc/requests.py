import logging
import uuid
from flask import g, has_request_context
from flask import request


# Check header X-Admin
def is_admin():
    g.session_admin = request.headers.get("X-Admin", "").lower() == "true"


# Returns the current request ID or a new one if there is none
def request_id():
    if getattr(g, 'request_id', None):
        return g.request_id

    headers = request.headers

    original_request_id = headers.get("X-Request-ID")
    g.request_id = str(original_request_id or uuid.uuid4())

    return g.request_id


class RequestIdFilter(logging.Filter):
    # This is a logging filter that makes the request ID available for use in
    # the logging format. Note that we're checking if we're in a request
    # context, as we may want to log things before Flask is fully loaded.
    def filter(self, record):
        record.request_id = request_id() if has_request_context() else ''
        return True
