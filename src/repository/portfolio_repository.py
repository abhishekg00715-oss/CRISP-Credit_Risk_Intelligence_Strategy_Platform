"""
portfolio_repository.py

Repository responsible for retrieving analytical portfolio datasets.

Responsibilities
----------------
- Provide reusable access to the Portfolio Analytical Repository.
- Encapsulate SQL queries.
- Return analytical datasets for downstream services.

Business calculations and analytical interpretation are intentionally
excluded from this repository and are handled by the
Portfolio Analytics Service.

"""

import sqlite3

from src.config.portfolio_config import (
    PORTFOLIO_DATABASE_PATH,
)

from src.database.portfolio_schema import (
    PORTFOLIO_SUMMARY,
    PORTFOLIO_RISK,
    PORTFOLIO_EXPOSURE,
    PORTFOLIO_SEGMENTATION,
    PORTFOLIO_TRENDS,
    PORTFOLIO_OPPORTUNITIES,
)


class PortfolioRepository:
    """
    Repository providing access to portfolio analytical datasets.
    """

    def __init__(self) -> None:
        self.database_path = PORTFOLIO_DATABASE_PATH

    # --------------------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------------------

    def _fetch_all(self, query: str, parameters: tuple = ()) -> list[dict]:
        """
        Executes a SELECT query and returns rows as dictionaries.
        """

        with sqlite3.connect(self.database_path) as connection:

            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            cursor.execute(query, parameters)

            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    # --------------------------------------------------------------
    # Portfolio Summary
    # --------------------------------------------------------------

    def get_portfolio_summary(self) -> list[dict]:
        """
        Returns portfolio summary metrics.
        """

        return self._fetch_all(
            f"""
            SELECT *
            FROM {PORTFOLIO_SUMMARY}
            """
        )

    # --------------------------------------------------------------
    # Portfolio Risk
    # --------------------------------------------------------------

    def get_portfolio_risk(self) -> list[dict]:
        """
        Returns portfolio risk distribution.
        """

        return self._fetch_all(
            f"""
            SELECT *
            FROM {PORTFOLIO_RISK}
            ORDER BY risk_band
            """
        )

    # --------------------------------------------------------------
    # Portfolio Exposure
    # --------------------------------------------------------------

    def get_portfolio_exposure(self) -> list[dict]:
        """
        Returns portfolio exposure metrics.
        """

        return self._fetch_all(
            f"""
            SELECT *
            FROM {PORTFOLIO_EXPOSURE}
            ORDER BY exposure_amount DESC
            """
        )

    # --------------------------------------------------------------
    # Portfolio Segmentation
    # --------------------------------------------------------------

    def get_portfolio_segmentation(self) -> list[dict]:
        """
        Returns customer portfolio segmentation metrics.
        """

        return self._fetch_all(
            f"""
            SELECT *
            FROM {PORTFOLIO_SEGMENTATION}
            ORDER BY customer_count DESC
            """
        )

    # --------------------------------------------------------------
    # Portfolio Trends
    # --------------------------------------------------------------

    def get_portfolio_trends(self) -> list[dict]:
        """
        Returns portfolio trend indicators.
        """

        return self._fetch_all(
            f"""
            SELECT *
            FROM {PORTFOLIO_TRENDS}
            ORDER BY metric_name
            """
        )

    # --------------------------------------------------------------
    # Portfolio Opportunities
    # --------------------------------------------------------------

    def get_portfolio_opportunities(self) -> list[dict]:
        """
        Returns portfolio opportunity metrics.
        """

        return self._fetch_all(
            f"""
            SELECT *
            FROM {PORTFOLIO_OPPORTUNITIES}
            ORDER BY eligible_customers DESC
            """
        )
