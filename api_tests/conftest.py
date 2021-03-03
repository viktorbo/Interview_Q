import pytest
import logging
import sys


@pytest.fixture(scope='class')
def log(request):
    log_format = '[%(name)s][%(levelname)s]: %(message)s'

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(log_format))

    err_handler = logging.StreamHandler(sys.stdout)
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(request.cls.__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(info_handler)

    yield logger