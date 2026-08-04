"""
risk_generator.py

Generates the Portfolio Risk analytical dataset.

Responsibilities
----------------
- Retrieve customer credit risk information.
- Classify customers into portfolio risk bands.
- Aggregate portfolio risk metrics.
- Populate the Portfolio Risk analytical table.

"""

from collections import defaultdict

from src.database.portfolio_queries import GET_CUSTOMER_RISK_DATA
from src.database.portfolio_schema import PORTFOLIO_RISK

from src.database.portfolio_data_generator.base_generator import (
    current_snapshot_date,
    fetch_rows,
    insert_rows,
    truncate_table,
)


INSERT_PORTFOLIO_RISK = f"""
INSERT INTO {PORTFOLIO_RISK}
(
    snapshot_date,
    risk_band,
    customer_count,
    exposure_amount,
    average_credit_score,
    default_rate
)
VALUES (?, ?, ?, ?, ?, ?)
"""


# ------------------------------------------------------------------
# Risk Classification
# ------------------------------------------------------------------

def classify_risk_band(credit_score: float) -> str:
    """
    Classify a customer into a portfolio risk band.

    Placeholder business rules.
    """

    if credit_score >= 750:
        return "Low"

    if credit_score >= 650:
        return "Medium"

    return "High"


# ------------------------------------------------------------------
# Generator
# ------------------------------------------------------------------

def generate_portfolio_risk() -> None:
    """
    Generates the Portfolio Risk analytical dataset.
    """

    rows = fetch_rows(GET_CUSTOMER_RISK_DATA)

    if not rows:
        return

    risk_summary = defaultdict(
        lambda: {
            "customers": 0,
            "credit_score": 0,
            "defaults": 0,
            "exposure": 0.0,
        }
    )

    for row in rows:

        band = classify_risk_band(row["credit_score"])

        risk_summary[band]["customers"] += 1
        risk_summary[band]["credit_score"] += row["credit_score"]
        risk_summary[band]["defaults"] += row["default_history"]

        #
        # Exposure will be enhanced in Exposure Generator.
        #
        risk_summary[band]["exposure"] += 0.0

    truncate_table(PORTFOLIO_RISK)

    snapshots = []

    snapshot_date = current_snapshot_date()

    for band, metrics in risk_summary.items():

        customer_count = metrics["customers"]

        average_credit_score = round(
            metrics["credit_score"] / customer_count,
            2,
        )

        default_rate = round(
            (metrics["defaults"] / customer_count) * 100,
            2,
        )

        snapshots.append(
            (
                snapshot_date,
                band,
                customer_count,
                metrics["exposure"],
                average_credit_score,
                default_rate,
            )
        )

    insert_rows(
        PORTFOLIO_RISK,
        INSERT_PORTFOLIO_RISK,
        snapshots,
    )

    print("Portfolio Risk dataset generated successfully.")
