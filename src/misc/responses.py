def response_error(status, message, code=-1, data=None):
    return {
        "code": code,
        "message": message,
        "data": data
    }, status


def response_ok(status, message, code=0, data=None):
    return {
        "code": code,
        "message": message,
        "data": data
    }, status
