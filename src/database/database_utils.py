"""
database_utils.py

Purpose:
Provides SQLite database utilities
for the Customer Risk Assessment
module.

Author:
Credit Risk Research Agent
"""

import sqlite3

from pathlib import Path

from src.database.schema import DATABASE_SCHEMA


def get_connection(database_name: str = "customer_risk.db") -> sqlite3.Connection:
    """
    Create and return a connection to the Customer Operational database.
    """

    database_path = Path(__file__).parent / database_name

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")

    return connection


class DatabaseManager:
    """
    Generic SQLite database manager.
    """

    def __init__(
        self,
        database_name: str = "customer_risk.db"
    ):

        self.database_path = (

            Path(__file__).parent

            / database_name

        )

        self.connection = None

        self.cursor = None

    # ----------------------------------------
    # Connect Database
    # ----------------------------------------

    def connect(
        self
    ):

        self.connection = sqlite3.connect(

            self.database_path

        )

        self.connection.execute(

            "PRAGMA foreign_keys = ON;"

        )

        self.cursor = self.connection.cursor()

        return self.connection

    # ----------------------------------------
    # Close Database
    # ----------------------------------------

    def close(
        self
    ):

        if self.connection:

            self.connection.close()

    # ----------------------------------------
    # Commit Changes
    # ----------------------------------------

    def commit(
        self
    ):

        if self.connection:

            self.connection.commit()

    # ----------------------------------------
    # Rollback
    # ----------------------------------------

    def rollback(
        self
    ):

        if self.connection:

            self.connection.rollback()

    # ----------------------------------------
    # Execute SQL
    # ----------------------------------------

    def execute(
        self,
        sql: str,
        parameters: tuple = ()
    ):

        self.cursor.execute(

            sql,

            parameters

        )

        return self.cursor

# ----------------------------------------
# Execute Query
# ----------------------------------------

    def query(
        self,
        sql: str,
        parameters: tuple = ()
    ):

        self.execute(

            sql,

            parameters

        )

        return self.fetchall()

    # ----------------------------------------
    # Execute Many
    # ----------------------------------------

    def executemany(
        self,
        sql: str,
        parameters: list
    ):

        self.cursor.executemany(

            sql,

            parameters

        )

    # ----------------------------------------
    # Fetch One
    # ----------------------------------------

    def fetchone(
        self
    ):

        return self.cursor.fetchone()

    # ----------------------------------------
    # Fetch All
    # ----------------------------------------

    def fetchall(
        self
    ):

        return self.cursor.fetchall()

    # ----------------------------------------
    # Create Database Schema
    # ----------------------------------------

    def create_schema(
        self
    ):

        for table_schema in DATABASE_SCHEMA:

            self.execute(
                table_schema
            )

        self.commit()

    # ----------------------------------------
    # Context Manager
    # ----------------------------------------

    def __enter__(
        self
    ):

        self.connect()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        if exc_type:

            self.rollback()

        else:

            self.commit()

        self.close()


# --------------------------------------------------
# Local Testing
# --------------------------------------------------

if __name__ == "__main__":

    with DatabaseManager() as database:

        database.create_schema()

        print()

        print("=" * 50)

        print("SQLite Database Created Successfully")

        print("=" * 50)

        print(

            f"Database : {database.database_path}"

        )

        print(

            f"Tables Created : {len(DATABASE_SCHEMA)}"

        )
