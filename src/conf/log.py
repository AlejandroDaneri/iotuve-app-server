LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'src.misc.requests.RequestIdFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [-] [%(levelname)s] [request_id:%(request_id)s] [func:%(name)s.%(module)s.%(funcName)s] [lineno:%(lineno)d] [message:%(message)s]',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
        'src': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
        'urllib3': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
        'gunicorn.error': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
        'flask_cors': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
    }
}
