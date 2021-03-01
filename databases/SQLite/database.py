import os
import sqlite3
from pathlib import Path
from sqlite3 import Error
from databases.SQLite.query_generator import SQLiteQueryGenerator as q_gen

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

    # OPERATIONS
    def create_table(self, table_name, descripted_columns: dict):
        self.execute_query(query=q_gen.create_table(table_name=table_name, descripted_columns=descripted_columns))

    def add_record(self, table_name, columns_names, val):
        self.execute_query(query=q_gen.add_record_to_table(table_name=table_name, column_names=columns_names, value=val))

    def add_records(self, table_name, columns_names, val: list or tuple):
        self.execute_query(query=q_gen.add_records_to_table(table_name=table_name, column_names=columns_names, values=val))

