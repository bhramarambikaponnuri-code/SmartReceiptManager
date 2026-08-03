import sqlite3
from pathlib import Path

from database.create_tables import create_tables

DATABASE_NAME = Path("receipt.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)

    create_tables(connection)

    return connection