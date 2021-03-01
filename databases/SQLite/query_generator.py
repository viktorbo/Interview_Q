class SQLiteQueryGenerator:
    @staticmethod
    def create_table(table_name, descripted_columns: dict) -> str:
        columns = ''
        for column, description in descripted_columns.items():
            columns += f"'{column}' {description}".replace('\'', '"') + ", "
        columns = columns[:-2]  # remove ', ' symbols from the end of the string
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        return query

    @staticmethod
    def add_records_to_table(table_name, column_names: list or tuple, values: list or tuple) -> str:
        str_values = ''
        for value in values:
            str_values += f"{value}, "
        str_values = str_values[:-2]  # remove ', ' symbols from the end of the string

        fixed_column_names = ', '.join([f'"{obj}"' for obj in column_names])
        query = f"INSERT INTO {table_name} ({fixed_column_names}) VALUES {str_values};".replace('\'', '"')
        return query

    @staticmethod
    def add_record_to_table(table_name, column_names: list or tuple, value):
        return SQLiteQueryGenerator.add_records_to_table(table_name=table_name, column_names=column_names,
                                                         values=[value])
