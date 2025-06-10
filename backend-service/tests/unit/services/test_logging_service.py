import io
import logging

import orjson

from backend_service.services.logging_service import get_logger


def test_get_logger():
    logger_debug = get_logger(debug=True)
    assert logger_debug.level == logging.DEBUG

    logger_info = get_logger(debug=False)
    assert logger_info.level == logging.INFO

    assert logger_debug is not logger_info
    assert logger_debug is get_logger(debug=True)
    assert logger_info is get_logger(debug=False)


def test_structured_logging(faker):
    structured_logger = get_logger(debug=True)
    log = faker.pydict()

    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    structured_logger.addHandler(handler)

    structured_logger.info(log)

    assert orjson.dumps(log).decode('utf-8') in stream.getvalue()
