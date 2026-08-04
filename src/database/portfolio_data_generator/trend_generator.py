"""
trend_generator.py

Generates the Portfolio Trends analytical dataset.

Responsibilities
----------------
- Analyse portfolio behavioural indicators from the available
  operational data.
- Produce trend-oriented portfolio metrics.
- Populate the Portfolio Trends analytical table.

The current implementation analyses the latest portfolio snapshot
produced by the ETL pipeline. The design intentionally remains
extensible to support historical portfolio snapshots in future
iterations without changing the generator interface.


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
    # Transaction Behaviour Indicators
    # --------------------------------------------------------------

    transaction_count = len(transaction_rows)

    total_transaction_value = sum(
        row["transaction_amount"] or 0.0
        for row in transaction_rows
    )

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
    # Digital Behaviour Indicators
    # --------------------------------------------------------------

    active_digital_customers = len(
        {
            row["customer_id"]
            for row in digital_rows
        }
    )

    total_logins = sum(
        row["login_count"] or 0
        for row in digital_rows
    )

    average_logins = (
        round(total_logins / active_digital_customers, 2)
        if active_digital_customers
        else 0.0
    )

    analytical_rows.extend(
        [
            (
                snapshot_date,
                "Active Digital Customers",
                active_digital_customers,
                "Current Snapshot",
            ),
            (
                snapshot_date,
                "Total Digital Logins",
                total_logins,
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
    # Persist Analytical Dataset
    # --------------------------------------------------------------

    insert_rows(
        PORTFOLIO_TRENDS,
        INSERT_PORTFOLIO_TRENDS,
        analytical_rows,
    )

    print("Portfolio Trends dataset generated successfully.")
