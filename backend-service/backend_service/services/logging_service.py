import logging
from functools import cache
from typing import Any

import orjson


@cache
def get_logger(debug: bool = False) -> logging.Logger:
    """
    Returns the default logge for the application.

    The logger is cached, so it is only created once for each debug mode.

    The logger logs in json format for structured logging.

    :param debug: Whether to enable debug logging
    :type debug: bool

    :return: The logger
    :rtype: logging.Logger
    """

    def json_make_record(
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: Any,
        *args: Any,
        **kwargs: Any,
    ) -> logging.LogRecord:
        """
        Returns a log record with the message converted to json.
        """
        msg = orjson.dumps(msg).decode('utf-8')
        return original_make_record(name, level, fn, lno, msg, *args, **kwargs)

    logger = logging.getLogger(__name__ + '_debug' * debug)

    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

    metadata_format = orjson.dumps({
        'level': '${levelname}',
        'timestamp': '${asctime}',
        'module': '${module}',
    }).decode('utf-8')
    log_format = '{"metadata":' + metadata_format + ',"message":${message}}'
    formatter = logging.Formatter(fmt=log_format, style='$')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    original_make_record = logger.makeRecord
    setattr(logger, 'makeRecord', json_make_record)

    logger.addHandler(handler)

    return logger
