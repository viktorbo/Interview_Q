from sqlite3 import Error


class QueryExecutor:
    @staticmethod
    def execute_query(database, query):
        cursor = database.connection.cursor()
        try:
            cursor.execute(query)
            database.connection.commit()
            # print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    def execute_read_query(database, query):
        cursor = database.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
