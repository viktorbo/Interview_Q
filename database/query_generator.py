class QueryGenerator:
    @staticmethod
    def create_table(table_name, descripted_columns: dict) -> str:
        columns = ''
        for column, description in descripted_columns.items():
            columns += f"{column} {description}, "
        columns = columns[:-2]  # remove ', ' symbols from the end of the string
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        return query

    @staticmethod
    def add_records_to_table(table_name, column_names: list or tuple, values: list or tuple) -> str:
        str_values = ''
        for value in values:
            str_values += f"{value}, "
        str_values = str_values[:-2]  # remove ', ' symbols from the end of the string
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES {str_values};"
        return query

