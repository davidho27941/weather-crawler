import json
import logging
import traceback
from logging import config


class JsonFormatter(logging.Formatter):
    """Format log records as JSON strings."""

    def format(self, record):  # type: ignore[override]
        try:
            message = record.getMessage()
        except (TypeError, ValueError):
            parts = [str(record.msg)]
            if record.args:
                if isinstance(record.args, tuple):
                    parts.extend(str(a) for a in record.args)
                else:
                    parts.append(str(record.args))
            message = " ".join(parts)

        message = message.rstrip("\n")

        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": message,
        }
        if record.exc_info:
            trace_list = traceback.format_exception(*record.exc_info)
            log_record["trace"] = [line.rstrip("\n") for line in trace_list]
        return json.dumps(log_record, ensure_ascii=False)


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
            "console": {"class": "logging.StreamHandler", "formatter": "json"},
            "file": {
                "class": "logging.FileHandler",
                "formatter": "json",
                "filename": "weather_crawler.log",
                "encoding": "utf-8",
            },
        },
        "formatters": {
            "json": {
                "()": JsonFormatter,
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            }
        },
    }

    config.dictConfig(logging_config)
    return logging.getLogger(name)
