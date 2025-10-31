# app/models/database.py
import os
import mysql.connector
from decouple import config, UndefinedValueError

def get_connection():
    try:
        host = config("DB_HOST")
        user = config("DB_USER")
        password = config("DB_PASS")
        database = config("DB_NAME")
        port = int(config("DB_PORT", default=3306))
    except UndefinedValueError:
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        database = os.getenv("DB_NAME")
        port = int(os.getenv("DB_PORT", 3306))

    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connection_timeout=10
        )
    except mysql.connector.Error as e:
        raise RuntimeError(f"MySQL connection failed: {e}") from e
