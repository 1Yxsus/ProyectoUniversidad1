import mysql.connector
from mysql.connector import Error
from decouple import config, UndefinedValueError

class DatabaseConnection:
    def __init__(self):
        self.host = config("DB_HOST")
        self.user = config("DB_USER")
        self.password = config("DB_PASS")
        self.database = config("DB_NAME")

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except Error as e:
            print(f"Error al conectar con MySQL: {e}")
            return None
