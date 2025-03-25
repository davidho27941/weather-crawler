import logging
from logging import config


def get_logger(name):

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "fastapi": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "weather_crawler": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "detailed"},
            "file": {
                "class": "logging.FileHandler",
                "formatter": "detailed",
                "filename": "weather_crawler.log",
            },
        },
        "formatters": {
            "detailed": {
                "format": "%(asctime)s %(name)-15s %(levelname)-8s %(message)s"
            }
        },
    }

    config.dictConfig(logging_config)
    return logging.getLogger(name)
