"""
portfolio_pipeline_smoke_test.py

Smoke test for the Portfolio Data Generation Pipeline.

Purpose
-------
Validates the end-to-end Portfolio ETL pipeline by:

1. Building the Portfolio Analytical Repository.
2. Executing all analytical data generators.
3. Reading analytical datasets through PortfolioRepository.
4. Displaying a concise validation summary.

This smoke test is intended as a lightweight developer
verification tool rather than a formal unit test.

"""

from src.database.portfolio_database_loader import (
    load_portfolio_repository,
)

from src.repository.portfolio_repository import (
    PortfolioRepository,
)


# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------

def print_header() -> None:
    """Prints the smoke test header."""

    print("\n" + "=" * 65)
    print("PORTFOLIO PIPELINE SMOKE TEST")
    print("=" * 65)


def print_footer(success: bool) -> None:
    """Prints the smoke test result."""

    print("=" * 65)

    if success:
        print("Portfolio ETL Pipeline : PASSED")
    else:
        print("Portfolio ETL Pipeline : FAILED")

    print("=" * 65)


def validate_dataset(name: str, rows: list[dict]) -> bool:
    """
    Displays dataset statistics.

    Returns
    -------
    bool
        True if the dataset contains records.
    """

    count = len(rows)

    status = "PASS" if count > 0 else "FAIL"

    print(
        f"{name:<30}"
        f"{count:>8} rows"
        f"    [{status}]"
    )

    return count > 0


# ------------------------------------------------------------------
# Smoke Test
# ------------------------------------------------------------------

def run_smoke_test() -> None:
    """
    Executes the Portfolio ETL smoke test.
    """

    print_header()

    try:

        print("\nBuilding Portfolio Repository...\n")

        load_portfolio_repository()

        repository = PortfolioRepository()

        print("\nValidating Analytical Repository\n")

        results = [

            validate_dataset(
                "Portfolio Summary",
                repository.get_portfolio_summary(),
            ),

            validate_dataset(
                "Portfolio Risk",
                repository.get_portfolio_risk(),
            ),

            validate_dataset(
                "Portfolio Exposure",
                repository.get_portfolio_exposure(),
            ),

            validate_dataset(
                "Portfolio Segmentation",
                repository.get_portfolio_segmentation(),
            ),

            validate_dataset(
                "Portfolio Trends",
                repository.get_portfolio_trends(),
            ),

            validate_dataset(
                "Portfolio Opportunities",
                repository.get_portfolio_opportunities(),
            ),
        ]

        print()

        print_footer(all(results))

    except Exception as exception:

        print("\nSmoke Test Failed\n")
        print(exception)

        print_footer(False)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

if __name__ == "__main__":
    run_smoke_test()
