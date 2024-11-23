import json
import mysql.connector
from mysql.connector import Error


class SeminarDatabase:
    def __init__(self, config_file_path):
        self.config = None
        self.connection = None
        self.cursor = None
        self._set_config(config_file_path)
        self._connect()

    def _set_config(self, config_file_path):
        try:
            with open(config_file_path, "r") as config_file:
                self.config = json.load(config_file)
        except Exception as e:
            print("[ERROR] Failed to load config file: ", e)

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config['DB_HOST'],
                database=self.config['DB_NAME'],
                user=self.config['DB_USER'],
                password=self.config['DB_PASSWORD']
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Connected to MySQL Server")
        except Error as e:
            print("[ERROR] Failed to connect to the server: ", e)

    def start_transaction(self):
        self.connection.start_transaction()

    def commit_transaction(self):
        self.connection.commit()

    def insert(self, table: str, columns: list, values: list):
        if not self.connection or not self.connection.is_connected():
            print("[ERROR] Database connection is not valid.")
            return
        if len(columns) != len(values):
            print("[ERROR] The number of columns and values do not match.")
            return

        try:
            formatted_columns = [str(column) if isinstance(column, int) else f'{column}' for column in columns]
            formatted_values = [str(value) if isinstance(value, int) else f"'{value}'" for value in values]
            joined_columns = ", ".join(formatted_columns)
            joined_values = ", ".join(formatted_values)

            query = f"INSERT INTO {table} ({joined_columns}) VALUES ({joined_values})"
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print("[ERROR] Failed to insert data: ", e)

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed.")
