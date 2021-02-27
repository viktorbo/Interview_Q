import os
import sqlite3
from pathlib import Path
from sqlite3 import Error


class DataBase:

    def __init__(self):
        self.connection = None

    def create_connection(self, database_name):
        self.database_name = database_name
        self.database_path = (Path(os.getenv('DB_DIR')) / f'{self.database_name}.sqlite').as_posix()
        try:
            self.connection = sqlite3.connect(self.database_path)
            print("Connection to SQLite DB successful \n"
                  f"    DB name: {self.database_name} \n"
                  f"    Path to DB: {self.database_path}")
        except Error as e:
            print(f"The error '{e}' occurred")
