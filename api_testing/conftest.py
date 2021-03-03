import pytest
import logging
import sys


@pytest.fixture(scope='module')
def log():
    log_format = '[%(levelname)s]: %(message)s'

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(log_format))

    err_handler = logging.StreamHandler(sys.stdout)
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(log_format)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(info_handler)
    logger.addHandler(err_handler)

    yield logger