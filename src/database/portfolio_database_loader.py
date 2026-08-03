"""
portfolio_database_loader.py

Orchestrates the Portfolio Data Generation pipeline.

Responsibilities
----------------
- Initialise the Portfolio Analytical Repository.
- Execute all portfolio analytical data generators.
- Populate analytical datasets.

Business calculations are delegated to the individual
generator modules.


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


def load_portfolio_repository() -> None:
    """
    Builds the Portfolio Analytical Repository.

    Workflow
    --------
    1. Initialise database schema.
    2. Generate analytical datasets.
    3. Populate analytical repository.
    """

    print("Initialising Portfolio Repository...")

    initialise_database()

    print("Generating Portfolio Summary...")
    generate_portfolio_summary()

    print("Generating Portfolio Risk...")
    generate_portfolio_risk()

    print("Generating Portfolio Exposure...")
    generate_portfolio_exposure()

    print("Generating Portfolio Segmentation...")
    generate_portfolio_segmentation()

    print("Generating Portfolio Trends...")
    generate_portfolio_trends()

    print("Generating Portfolio Opportunities...")
    generate_portfolio_opportunities()

    print("Portfolio Repository successfully populated.")


if __name__ == "__main__":
    load_portfolio_repository()
