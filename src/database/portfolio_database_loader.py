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

GENERATORS = [
    ("Portfolio Summary", generate_portfolio_summary),
    ("Portfolio Risk", generate_portfolio_risk),
    ("Portfolio Exposure", generate_portfolio_exposure),
    ("Portfolio Segmentation", generate_portfolio_segmentation),
    ("Portfolio Trends", generate_portfolio_trends),
    ("Portfolio Opportunities", generate_portfolio_opportunities),
    ]

def load_portfolio_repository(selected_generators=None):
    """
    Builds the Portfolio Analytical Repository.

    Workflow
    --------
    1. Initialise database schema.
    2. Generate analytical datasets.
    3. Populate analytical repository.
    """
    print("=" * 60)
    print("Building Portfolio Analytical Repository")
    print("=" * 60)
    
    initialise_database()

    for name, generator in selected_generators or GENERATORS:
        try:
            print(f"Generating {name}...")
            generator()
            print(f"{name} completed.")
            
        except Exception as ex:
            print(f"{name} failed: {ex}")
            raise

    print("=" * 60)
    print("Portfolio Repository successfully generated.")
    print("=" * 60)

if __name__ == "__main__":
    load_portfolio_repository()
