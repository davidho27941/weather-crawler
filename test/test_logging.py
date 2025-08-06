import json
import logging
import sys

from weather_crawler.logger import JsonFormatter


def test_json_formatter_outputs_json():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="hello",
        args=(),
        exc_info=None,
    )
    data = json.loads(formatter.format(record))
    assert data["message"] == "hello"
    assert data["level"] == "INFO"


def test_json_formatter_includes_trace():
    formatter = JsonFormatter()
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=30,
            msg="fail",
            args=(),
            exc_info=sys.exc_info(),
        )
    data = json.loads(formatter.format(record))
    assert data["message"] == "fail"
    assert "trace" in data and any("RuntimeError" in line for line in data["trace"])


def test_json_formatter_handles_extra_args():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=50,
        msg="hello",
        args=("world",),
        exc_info=None,
    )
    data = json.loads(formatter.format(record))
    assert data["message"] == "hello world"


def test_json_formatter_strips_newline():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=70,
        msg="hello\n",
        args=(),
        exc_info=None,
    )
    data = json.loads(formatter.format(record))
    assert data["message"] == "hello"
