"""
portfolio_kpi_service.py

Provides portfolio-level KPI analytics.

Responsibilities
----------------
- Retrieve the portfolio summary from PortfolioRepository.
- Expose portfolio-level KPIs in a consistent structure.
- Perform lightweight analytical calculations where required.
- Keep database access outside the analytics layer.

Business calculations and analytical interpretation belong here,
while data retrieval is delegated to PortfolioRepository.

The service currently operates on the latest available portfolio
snapshot. The design does not prevent future historical/snapshot
analysis from being introduced.
"""

from typing import Any, Dict, Optional

from src.repository.portfolio_repository import PortfolioRepository


class PortfolioKPIService:
    """
    Service responsible for portfolio-level KPI analysis.
    """

    def __init__(
        self,
        repository: Optional[PortfolioRepository] = None,
    ) -> None:

        self.repository = (
            repository
            if repository is not None
            else PortfolioRepository()
        )

    # --------------------------------------------------------------
    # Portfolio KPI Analysis
    # --------------------------------------------------------------

    def get_portfolio_kpis(self) -> Dict[str, Any]:
        """
        Retrieve and return the latest portfolio KPI snapshot.

        Returns
        -------
        dict
            Portfolio KPI metrics.

        Raises
        ------
        ValueError
            If no portfolio summary is available.
        """

        rows = self.repository.get_portfolio_summary()

        if not rows:
            raise ValueError(
                "No portfolio summary data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        return {
            "snapshot_date": latest_snapshot["snapshot_date"],
            "active_customers": latest_snapshot["active_customers"],
            "total_portfolio_value": latest_snapshot[
                "total_portfolio_value"
            ],
            "total_credit_exposure": latest_snapshot[
                "total_credit_exposure"
            ],
            "average_credit_score": latest_snapshot[
                "average_credit_score"
            ],
            "average_utilisation": latest_snapshot[
                "average_utilisation"
            ],
            "portfolio_health_score": latest_snapshot[
                "portfolio_health_score"
            ],
            "default_rate": latest_snapshot[
                "default_rate"
            ],
            "delinquency_rate": latest_snapshot[
                "delinquency_rate"
            ],
        }

    # --------------------------------------------------------------
    # Portfolio Health
    # --------------------------------------------------------------

    def get_portfolio_health(self) -> Dict[str, Any]:
        """
        Return the key indicators representing portfolio health.
        """

        kpis = self.get_portfolio_kpis()

        return {
            "snapshot_date": kpis["snapshot_date"],
            "portfolio_health_score": kpis[
                "portfolio_health_score"
            ],
            "average_credit_score": kpis[
                "average_credit_score"
            ],
            "average_utilisation": kpis[
                "average_utilisation"
            ],
            "default_rate": kpis[
                "default_rate"
            ],
            "delinquency_rate": kpis[
                "delinquency_rate"
            ],
        }

    # --------------------------------------------------------------
    # Credit Exposure Ratio
    # --------------------------------------------------------------

    def calculate_exposure_ratio(self) -> float:
        """
        Calculate credit exposure as a percentage of total
        portfolio value.

        Returns
        -------
        float
            Exposure ratio expressed as a percentage.

        Notes
        -----
        The metric is calculated only when total portfolio value
        is greater than zero.
        """

        kpis = self.get_portfolio_kpis()

        portfolio_value = kpis["total_portfolio_value"]
        credit_exposure = kpis["total_credit_exposure"]

        if not portfolio_value:
            return 0.0

        return round(
            (credit_exposure / portfolio_value) * 100,
            2,
        )

    # --------------------------------------------------------------
    # Latest Snapshot
    # --------------------------------------------------------------

    @staticmethod
    def _get_latest_snapshot(
        rows: list[dict],
    ) -> dict:
        """
        Return the latest available portfolio snapshot.

        The repository currently returns the portfolio summary
        ordered by its natural table representation. This method
        explicitly identifies the latest snapshot so that the
        service does not depend on query ordering.
        """

        return max(
            rows,
            key=lambda row: row["snapshot_date"],
        )
