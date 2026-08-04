"""
opportunity_generator.py

Generates the Portfolio Opportunities analytical dataset.

Responsibilities
----------------
- Analyse customer portfolio data to identify measurable
  portfolio opportunities.
- Aggregate opportunity metrics.
- Populate the Portfolio Opportunities analytical table.

The generated dataset represents analytical opportunities only.
Recommendation prioritisation and narrative generation are
performed by the Recommendation Agent.

Backlog
-------
CRA-12 - Portfolio Repository & Portfolio Data Foundation
"""

from collections import defaultdict

from src.database.portfolio_queries import GET_OPPORTUNITY_DATA
from src.database.portfolio_schema import PORTFOLIO_OPPORTUNITIES

from src.database.portfolio_data_generator.base_generator import (
    current_snapshot_date,
    fetch_rows,
    insert_rows,
    truncate_table,
)

# ------------------------------------------------------------------
# Opportunity Thresholds
# ------------------------------------------------------------------

HIGH_CREDIT_SCORE = 750
LOW_UTILISATION = 30.0
HIGH_UTILISATION = 80.0
NO_DEFAULT_HISTORY = 0

# ------------------------------------------------------------------
# Insert Statement
# ------------------------------------------------------------------

INSERT_PORTFOLIO_OPPORTUNITIES = f"""
INSERT INTO {PORTFOLIO_OPPORTUNITIES}
(
    snapshot_date,
    opportunity_type,
    eligible_customers,
    estimated_value,
    confidence_score
)
VALUES
(
    ?, ?, ?, ?, ?
)
"""

# ------------------------------------------------------------------
# Generator
# ------------------------------------------------------------------

def generate_portfolio_opportunities() -> None:
    """
    Generates the Portfolio Opportunities analytical dataset.
    """

    rows = fetch_rows(GET_OPPORTUNITY_DATA)

    if not rows:
        return

    opportunity_summary = defaultdict(
        lambda: {
            "eligible_customers": 0,
            "estimated_value": 0.0,
            "confidence_score": 0.0,
        }
    )

    # --------------------------------------------------------------
    # Analyse Portfolio Opportunities
    # --------------------------------------------------------------

    for row in rows:

        # ------------------------------------------
        # Credit Limit Enhancement
        # ------------------------------------------

        if (
            row["credit_score"] >= HIGH_CREDIT_SCORE
            and row["credit_utilization"] <= LOW_UTILISATION
            and row["defaults"] == NO_DEFAULT_HISTORY
        ):

            opportunity_summary["Credit Limit Enhancement"][
                "eligible_customers"
            ] += 1

            opportunity_summary["Credit Limit Enhancement"][
                "estimated_value"
            ] += row["credit_limit"] * 0.20

            opportunity_summary["Credit Limit Enhancement"][
                "confidence_score"
            ] += 0.95

        # ------------------------------------------
        # Credit Utilisation Review
        # ------------------------------------------

        elif row["credit_utilization"] >= HIGH_UTILISATION:

            opportunity_summary["Credit Utilisation Review"][
                "eligible_customers"
            ] += 1

            opportunity_summary["Credit Utilisation Review"][
                "estimated_value"
            ] += row["outstanding_balance"]

            opportunity_summary["Credit Utilisation Review"][
                "confidence_score"
            ] += 0.85

    # --------------------------------------------------------------
    # Refresh Analytical Dataset
    # --------------------------------------------------------------

    truncate_table(PORTFOLIO_OPPORTUNITIES)

    snapshot_date = current_snapshot_date()

    analytical_rows = []

    for opportunity_type, metrics in opportunity_summary.items():

        eligible_customers = metrics["eligible_customers"]

        confidence_score = (
            round(
                metrics["confidence_score"] / eligible_customers,
                2,
            )
            if eligible_customers
            else 0.0
        )

        analytical_rows.append(
            (
                snapshot_date,
                opportunity_type,
                eligible_customers,
                round(metrics["estimated_value"], 2),
                confidence_score,
            )
        )

    # --------------------------------------------------------------
    # Persist Analytical Dataset
    # --------------------------------------------------------------

    insert_rows(
        PORTFOLIO_OPPORTUNITIES,
        INSERT_PORTFOLIO_OPPORTUNITIES,
        analytical_rows,
    )

    print("Portfolio Opportunities dataset generated successfully.")
