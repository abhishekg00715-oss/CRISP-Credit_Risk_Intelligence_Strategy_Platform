"""
segmentation_generator.py

Generates the Portfolio Segmentation analytical dataset.

Responsibilities
----------------
- Retrieve customer segmentation data from the operational repository.
- Aggregate portfolio metrics across customer dimensions.
- Populate the Portfolio Segmentation analytical table.

Business calculations are implemented within this generator while
common ETL operations are delegated to base_generator.py.


"""

from collections import defaultdict

from src.database.portfolio_queries import GET_SEGMENTATION_DATA
from src.database.portfolio_schema import PORTFOLIO_SEGMENTATION

from src.database.portfolio_data_generator.base_generator import (
    current_snapshot_date,
    fetch_rows,
    insert_rows,
    truncate_table,
)

# ------------------------------------------------------------------
# Insert Statement
# ------------------------------------------------------------------

INSERT_PORTFOLIO_SEGMENTATION = f"""
INSERT INTO {PORTFOLIO_SEGMENTATION}
(
    snapshot_date,
    customer_segment,
    state,
    employment_type,
    occupation,
    customer_count,
    average_credit_score,
    average_utilisation
)
VALUES
(
    ?, ?, ?, ?, ?, ?, ?, ?
)
"""


# ------------------------------------------------------------------
# Generator
# ------------------------------------------------------------------

def generate_portfolio_segmentation() -> None:
    """
    Generates the Portfolio Segmentation analytical dataset.
    """

    rows = fetch_rows(GET_SEGMENTATION_DATA)

    if not rows:
        return

    segmentation_summary = defaultdict(
        lambda: {
            "customer_count": 0,
            "credit_score_total": 0.0,
            "utilisation_total": 0.0,
        }
    )

    # --------------------------------------------------------------
    # Aggregate Portfolio Segmentation Metrics
    # --------------------------------------------------------------

    for row in rows:

        key = (
            row["customer_segment"],
            row["state"],
            row["employment_type"],
            row["occupation"],
        )

        segmentation_summary[key]["customer_count"] += 1
        segmentation_summary[key]["credit_score_total"] += row["credit_score"]
        segmentation_summary[key]["utilisation_total"] += row["credit_utilisation"]

    # --------------------------------------------------------------
    # Refresh Analytical Dataset
    # --------------------------------------------------------------

    truncate_table(PORTFOLIO_SEGMENTATION)

    snapshot_date = current_snapshot_date()

    analytical_rows = []

    for (
        customer_segment,
        state,
        employment_type,
        occupation,
    ), metrics in segmentation_summary.items():

        customer_count = metrics["customer_count"]

        average_credit_score = round(
            metrics["credit_score_total"] / customer_count,
            2,
        )

        average_utilisation = round(
            metrics["utilisation_total"] / customer_count,
            2,
        )

        analytical_rows.append(
            (
                snapshot_date,
                customer_segment,
                state,
                employment_type,
                occupation,
                customer_count,
                average_credit_score,
                average_utilisation,
            )
        )

    # --------------------------------------------------------------
    # Persist Dataset
    # --------------------------------------------------------------

    insert_rows(
        PORTFOLIO_SEGMENTATION,
        INSERT_PORTFOLIO_SEGMENTATION,
        analytical_rows,
    )

    print("Portfolio Segmentation dataset generated successfully.")
