import pytest
import os
from selenium import webdriver
from task1_and_ui_tests.databases.SQLite.database import SQLiteDataBase


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


