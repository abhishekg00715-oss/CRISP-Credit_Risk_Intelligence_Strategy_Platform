"""
summary_generator.py

Generates the Portfolio Summary analytical dataset.

Responsibilities
----------------
- Retrieve operational portfolio data.
- Calculate portfolio-level summary metrics.
- Populate the Portfolio Summary analytical table.

Business calculations are intentionally implemented here rather
than within SQL to maintain separation of concerns.


"""

from datetime import datetime

from src.database.portfolio_queries import GET_CUSTOMER_PORTFOLIO_DATA

from src.database.portfolio_schema import PORTFOLIO_SUMMARY

from src.database.portfolio_data generator.base_generator import (
    fetch_rows,
    truncate_table,
    insert_rows,
    current_snapshot_date,
)


INSERT_PORTFOLIO_SUMMARY = f"""
INSERT INTO {PORTFOLIO_SUMMARY}
(
    snapshot_date,
    active_customers,
    total_portfolio_value,
    total_credit_exposure,
    average_credit_score,
    average_utilisation,
    portfolio_health_score,
    default_rate,
    delinquency_rate,
    created_at
)
VALUES
(
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
)
"""


def calculate_portfolio_health_score(
    average_credit_score: float,
    average_utilisation: float,
    default_rate: float,
) -> float:
    """
    Calculates a simple Portfolio Health Score.

    Placeholder implementation.

    The calculation can later evolve into a weighted business model
    without impacting the ETL pipeline.
    """

    return round(
        (
            (average_credit_score / 850) * 60
            + (100 - average_utilisation) * 0.25
            + (100 - default_rate) * 0.15
        ),
        2,
    )


def generate_portfolio_summary() -> None:
    """
    Generates the Portfolio Summary dataset.
    """

    rows = fetch_rows(GET_CUSTOMER_PORTFOLIO_DATA)

    if not rows:
        return

    active_customers = len(rows)

    total_credit_score = 0
    total_utilisation = 0
    total_defaults = 0

    # Placeholder values until exposure generators are implemented.
    total_portfolio_value = 0.0
    total_credit_exposure = 0.0
    delinquency_rate = 0.0

    for row in rows:

        total_credit_score += row["credit_score"]

        total_utilisation += row["credit_utilisation"]

        total_defaults += row["default_history"]

    average_credit_score = round(
        total_credit_score / active_customers,
        2,
    )

    average_utilisation = round(
        total_utilisation / active_customers,
        2,
    )

    default_rate = round(
        (total_defaults / active_customers) * 100,
        2,
    )

    portfolio_health_score = calculate_portfolio_health_score(
        average_credit_score,
        average_utilisation,
        default_rate,
    )

    snapshot = (
        current_snapshot_date(),
        active_customers,
        total_portfolio_value,
        total_credit_exposure,
        average_credit_score,
        average_utilisation,
        portfolio_health_score,
        default_rate,
        delinquency_rate,
        datetime.now().isoformat(),
    )

    truncate_table(PORTFOLIO_SUMMARY)

    insert_rows(
        PORTFOLIO_SUMMARY,
        INSERT_PORTFOLIO_SUMMARY,
        [snapshot],
    )

    print("Portfolio Summary generated successfully.")
