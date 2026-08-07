"""
portfolio_database_loader.py

Portfolio Analytical Repository Builder

Purpose
-------
Builds and refreshes the Portfolio Analytical Repository from the
Customer Operational Repository.

Responsibilities
----------------
- Initialise the Portfolio Analytical Repository.
- Execute all Portfolio Data Generators.
- Produce a complete analytical snapshot.

This module is the canonical entry point for the Portfolio ETL pipeline.

Typical Usage
-------------
Development
    python portfolio_database_loader.py

Smoke Testing
    load_portfolio_repository()

Future Production
    Invoked by a scheduler or orchestration workflow.

"""

from src.database.portfolio_database_utils import initialise_database

from src.database.portfolio_data_generator.summary_generator import (
    generate_portfolio_summary,
)
from src.database.portfolio_data_generator.risk_generator import (
    generate_portfolio_risk,
)
from src.database.portfolio_data_generator.exposure_generator import (
    generate_portfolio_exposure,
)
from src.database.portfolio_data_generator.segmentation_generator import (
    generate_portfolio_segmentation,
)
from src.database.portfolio_data_generator.trend_generator import (
    generate_portfolio_trends,
)
from src.database.portfolio_data_generator.opportunity_generator import (
    generate_portfolio_opportunities,
)


# ------------------------------------------------------------------
# Registered Portfolio Generators
# ------------------------------------------------------------------

PORTFOLIO_GENERATORS = [

    ("Portfolio Summary", generate_portfolio_summary),

    ("Portfolio Risk", generate_portfolio_risk),

    ("Portfolio Exposure", generate_portfolio_exposure),

    ("Portfolio Segmentation", generate_portfolio_segmentation),

    ("Portfolio Trends", generate_portfolio_trends),

    ("Portfolio Opportunities", generate_portfolio_opportunities),
]


# ------------------------------------------------------------------
# Portfolio Repository Builder
# ------------------------------------------------------------------

def load_portfolio_repository() -> None:
    """
    Builds or refreshes the Portfolio Analytical Repository.

    Workflow
    --------
    1. Initialise analytical database.
    2. Execute all analytical generators.
    3. Populate analytical repository.

    Raises
    ------
    RuntimeError
        If any generator fails.
    """

    print()
    print("=" * 65)
    print("Building Portfolio Analytical Repository")
    print("=" * 65)

    initialise_database()

    for generator_name, generator in PORTFOLIO_GENERATORS:

        print(f"Generating {generator_name}...")

        try:

            generator()

        except Exception as ex:

            raise RuntimeError(
                f"{generator_name} generation failed."
            ) from ex

    print()
    print("=" * 65)
    print("Portfolio Analytical Repository Successfully Built")
    print("=" * 65)


# ------------------------------------------------------------------
# Local Execution
# ------------------------------------------------------------------

if __name__ == "__main__":

    load_portfolio_repository()
