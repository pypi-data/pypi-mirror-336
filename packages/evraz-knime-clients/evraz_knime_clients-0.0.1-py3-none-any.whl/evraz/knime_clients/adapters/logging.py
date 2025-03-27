import logging.config

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOGGING_LEVEL: str = 'DEBUG'
    LOGGING_JSON: bool = True


def configure():
    settings = Settings()

    fmt = '%(asctime)s.%(msecs)03d [%(levelname)s]|[%(name)s]: %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': fmt,
                'datefmt': datefmt,
            },
            'json': {
                'format': fmt,
                'datefmt': datefmt,
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'json_ensure_ascii': False
            },
        },
        'handlers': {
            'default': {
                'level': settings.LOGGING_LEVEL,
                'formatter': 'json' if settings.LOGGING_JSON else 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'root': {
            'handlers': ['default']
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': settings.LOGGING_LEVEL,
                'propagate': False
            }
        }
    }

    logging.config.dictConfig(config)
