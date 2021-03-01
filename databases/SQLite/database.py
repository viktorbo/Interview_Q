import os
import sqlite3
from pathlib import Path
from sqlite3 import Error


class SQLiteDataBase:

    def __init__(self):
        self.connection = None

    def create_connection(self, database_name):
        self.database_name = database_name
        self.database_path = (Path(os.getenv('DATABASE_DIR')) / f'{self.database_name}.sqlite').as_posix()
        try:
            self.connection = sqlite3.connect(self.database_path)
        except Error as e:
            raise Error(e)

    def close_connection(self):
        try:
            self.connection = self.connection.close()
            del self.database_name
            del self.database_path
        except Error as e:
            raise Error(e)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            raise Error(e)

    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            raise Error(e)
