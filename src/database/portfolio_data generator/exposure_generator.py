"""
exposure_generator.py

Generates the Portfolio Exposure analytical dataset.

Responsibilities
----------------
- Retrieve loan and credit card exposure information.
- Aggregate exposure by Product and State.
- Calculate concentration percentages.
- Populate the Portfolio Exposure analytical table.

Business calculations are implemented here while common ETL
operations are delegated to base_generator.py.


"""

from collections import defaultdict

from src.database.portfolio_queries import (
    GET_CARD_EXPOSURE_DATA,
    GET_LOAN_EXPOSURE_DATA,
)

from src.database.portfolio_schema import PORTFOLIO_EXPOSURE

from src.database.portfolio_data_generator.base_generator import (
    current_snapshot_date,
    fetch_rows,
    insert_rows,
    truncate_table,
)

# ------------------------------------------------------------------
# Insert Statement
# ------------------------------------------------------------------

INSERT_PORTFOLIO_EXPOSURE = f"""
INSERT INTO {PORTFOLIO_EXPOSURE}
(
    snapshot_date,
    product_type,
    state,
    exposure_amount,
    concentration_percentage
)
VALUES
(
    ?, ?, ?, ?, ?
)
"""


# ------------------------------------------------------------------
# Generator
# ------------------------------------------------------------------

def generate_portfolio_exposure() -> None:
    """
    Generates the Portfolio Exposure analytical dataset.
    """

    loan_rows = fetch_rows(GET_LOAN_EXPOSURE_DATA)
    card_rows = fetch_rows(GET_CARD_EXPOSURE_DATA)

    if not loan_rows and not card_rows:
        return

    exposure_summary = defaultdict(float)

    total_exposure = 0.0

    # --------------------------------------------------------------
    # Aggregate Loan Exposure
    # --------------------------------------------------------------

    for row in loan_rows:

        exposure = row["outstanding_balance"] or 0.0

        key = (
            row["loan_type"],
            row["state"],
        )

        exposure_summary[key] += exposure

        total_exposure += exposure

    # --------------------------------------------------------------
    # Aggregate Credit Card Exposure
    # --------------------------------------------------------------

    for row in card_rows:

        exposure = row["current_balance"] or 0.0

        key = (
            row["card_type"],
            row["state"],
        )

        exposure_summary[key] += exposure

        total_exposure += exposure

    # --------------------------------------------------------------
    # Refresh Analytical Dataset
    # --------------------------------------------------------------

    truncate_table(PORTFOLIO_EXPOSURE)

    snapshot_date = current_snapshot_date()

    analytical_rows = []

    for (product_type, state), exposure_amount in exposure_summary.items():

        if total_exposure > 0:

            concentration = round(
                (exposure_amount / total_exposure) * 100,
                2,
            )

        else:

            concentration = 0.0

        analytical_rows.append(
            (
                snapshot_date,
                product_type,
                state,
                round(exposure_amount, 2),
                concentration,
            )
        )

    # --------------------------------------------------------------
    # Persist Dataset
    # --------------------------------------------------------------

    insert_rows(
        PORTFOLIO_EXPOSURE,
        INSERT_PORTFOLIO_EXPOSURE,
        analytical_rows,
    )

    print("Portfolio Exposure dataset generated successfully.")
