"""
base_generator.py

Shared utility functions for the Portfolio Data Generation pipeline.

Responsibilities
----------------
- Provide database connections.
- Execute reusable SQL operations.
- Support bulk inserts into analytical tables.
- Maintain common ETL helper functions.

Business calculations and analytical transformations are intentionally
implemented within the individual generator modules.


"""

from datetime import datetime
import sqlite3
from typing import Iterable, List, Tuple

from src.database.database_utils import get_connection as get_customer_connection
from src.database.portfolio_database_utils import (
    get_connection as get_portfolio_connection,
)

from src.config.portfolio_config import DEFAULT_DATE_FORMAT


# ------------------------------------------------------------------
# Snapshot Utilities
# ------------------------------------------------------------------

def current_snapshot_date() -> str:
    """
    Returns the current snapshot date.

    Used consistently across all analytical datasets.
    """
    return datetime.now().strftime(DEFAULT_DATE_FORMAT)


# ------------------------------------------------------------------
# Query Execution
# ------------------------------------------------------------------

def execute_query(
    connection: sqlite3.Connection,
    query: str,
    parameters: Tuple = (),
) -> List[sqlite3.Row]:
    """
    Execute a SELECT query and return all rows.
    """

    cursor = connection.cursor()

    cursor.execute(query, parameters)

    return cursor.fetchall()


# ------------------------------------------------------------------
# Table Management
# ------------------------------------------------------------------

def truncate_table(table_name: str) -> None:
    """
    Removes all records from an analytical table.
    """

    with get_portfolio_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM {table_name}")

        connection.commit()


# ------------------------------------------------------------------
# Bulk Insert
# ------------------------------------------------------------------

def insert_rows(
    table_name: str,
    insert_sql: str,
    rows: Iterable[Tuple],
) -> None:
    """
    Bulk insert analytical records into a Portfolio table.
    """

    with get_portfolio_connection() as connection:

        cursor = connection.cursor()

        cursor.executemany(insert_sql, rows)

        connection.commit()


# ------------------------------------------------------------------
# Customer Repository Helper
# ------------------------------------------------------------------

def fetch_rows(
    query: str,
    parameters: Tuple = (),
) -> List[sqlite3.Row]:
    """
    Execute a query against the Customer Operational Repository.
    """

    with get_customer_connection() as connection:

        return execute_query(connection, query, parameters)
