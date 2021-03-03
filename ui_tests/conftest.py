import pytest
import os
import sys
from selenium import webdriver
from ui_tests.databases.SQLite.database import SQLiteDataBase
import logging


@pytest.fixture(scope='module')
def log():
    # log_format = '%(asctime)s [%(levelname)s]: %(message)s'
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

    yield logger


@pytest.fixture(scope='class')
def chrome_driver():
    driver = webdriver.Chrome(executable_path=os.getenv('DRIVER_PATH'))
    yield driver
    driver.quit()


@pytest.fixture(scope='class')
def database():
    database = SQLiteDataBase()
    database.create_connection('checkme_db')
    yield database
    database.close_connection()


