"""
portfolio_database_utils.py

Utility functions for managing the Portfolio Analytical Repository.

Responsibilities
----------------
- Create Portfolio Analytics database
- Initialise analytical schema
- Provide SQLite connections
- Support database reset for testing

Business logic, analytical calculations and data loading are intentionally
kept outside this module.


"""

from pathlib import Path
import sqlite3

from src.database.portfolio_schema import SCHEMA_DEFINITION
from src.config.portfolio_config import (
    DATABASE_DIRECTORY,
    DATABASE_PATH,
)



# ------------------------------------------------------------------
# Connection Management
# ------------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the Portfolio Analytics database.
    """

    DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ------------------------------------------------------------------
# Database Creation
# ------------------------------------------------------------------

def create_database() -> None:
    """
    Create the Portfolio Analytics database schema.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        for ddl in SCHEMA_DEFINITION:
            cursor.execute(ddl)

        connection.commit()


# ------------------------------------------------------------------
# Database Initialisation
# ------------------------------------------------------------------

def initialise_database() -> None:
    """
    Initialise the Portfolio Analytics repository.

    Safe to execute multiple times.
    """

    create_database()


# ------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------

def database_exists() -> bool:
    """
    Returns True if the Portfolio Analytics database exists.
    """

    return DATABASE_PATH.exists()


def drop_database() -> None:
    """
    Remove the Portfolio Analytics database.

    Primarily used by automated tests.
    """

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()


def recreate_database() -> None:
    """
    Recreate the Portfolio Analytics repository.

    Intended for development and testing.
    """

    drop_database()

    create_database()
