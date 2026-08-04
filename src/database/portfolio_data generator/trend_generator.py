"""
trend_generator.py

Generates the Portfolio Trends analytical dataset.

Responsibilities
----------------
- Retrieve operational portfolio activity metrics.
- Aggregate portfolio-level trend metrics.
- Populate the Portfolio Trends analytical table.

This generator captures periodic portfolio measurements.
Trend interpretation and analysis are performed by the
Portfolio Analytics Service (CRA-13).

"""

from src.database.portfolio_queries import (
    GET_TRANSACTION_TRENDS,
    GET_DIGITAL_ACTIVITY,
)

from src.database.portfolio_schema import PORTFOLIO_TRENDS

from src.database.portfolio_data_generator.base_generator import (
    current_snapshot_date,
    fetch_rows,
    insert_rows,
    truncate_table,
)

# ------------------------------------------------------------------
# Insert Statement
# ------------------------------------------------------------------

INSERT_PORTFOLIO_TRENDS = f"""
INSERT INTO {PORTFOLIO_TRENDS}
(
    snapshot_date,
    metric_name,
    metric_value,
    reporting_period
)
VALUES
(
    ?, ?, ?, ?
)
"""


# ------------------------------------------------------------------
# Generator
# ------------------------------------------------------------------

def generate_portfolio_trends() -> None:
    """
    Generates the Portfolio Trends analytical dataset.
    """

    transaction_rows = fetch_rows(GET_TRANSACTION_TRENDS)
    digital_rows = fetch_rows(GET_DIGITAL_ACTIVITY)

    truncate_table(PORTFOLIO_TRENDS)

    snapshot_date = current_snapshot_date()

    analytical_rows = []

    # --------------------------------------------------------------
    # Transaction Metrics
    # --------------------------------------------------------------

    total_transaction_value = sum(
        row["transaction_amount"] or 0.0
        for row in transaction_rows
    )

    transaction_count = len(transaction_rows)

    average_transaction_value = (
        round(total_transaction_value / transaction_count, 2)
        if transaction_count
        else 0.0
    )

    analytical_rows.extend(
        [
            (
                snapshot_date,
                "Transaction Count",
                transaction_count,
                "Current Snapshot",
            ),
            (
                snapshot_date,
                "Total Transaction Value",
                round(total_transaction_value, 2),
                "Current Snapshot",
            ),
            (
                snapshot_date,
                "Average Transaction Value",
                average_transaction_value,
                "Current Snapshot",
            ),
        ]
    )

    # --------------------------------------------------------------
    # Digital Activity Metrics
    # --------------------------------------------------------------

    total_logins = sum(
        row["login_count"] or 0
        for row in digital_rows
    )

    active_customers = len(
        {
            row["customer_id"]
            for row in digital_rows
        }
    )

    average_logins = (
        round(total_logins / active_customers, 2)
        if active_customers
        else 0.0
    )

    analytical_rows.extend(
        [
            (
                snapshot_date,
                "Digital Login Count",
                total_logins,
                "Current Snapshot",
            ),
            (
                snapshot_date,
                "Active Digital Customers",
                active_customers,
                "Current Snapshot",
            ),
            (
                snapshot_date,
                "Average Logins Per Customer",
                average_logins,
                "Current Snapshot",
            ),
        ]
    )

    # --------------------------------------------------------------
    # Persist Dataset
    # --------------------------------------------------------------

    insert_rows(
        PORTFOLIO_TRENDS,
        INSERT_PORTFOLIO_TRENDS,
        analytical_rows,
    )

    print("Portfolio Trends dataset generated successfully.")
