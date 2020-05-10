def response_error(status, message, code=0, data=None):
    return {
        "code": code,
        "message": message,
        "data": data
    }, status
