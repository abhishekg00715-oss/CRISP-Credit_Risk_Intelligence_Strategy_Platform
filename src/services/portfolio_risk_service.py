"""
portfolio_risk_service.py

Provides portfolio-level risk analytics.

Responsibilities
----------------
- Retrieve portfolio risk data from PortfolioRepository.
- Analyse the distribution of customers across risk bands.
- Identify dominant and highest-exposure risk bands.
- Calculate portfolio-level risk distribution metrics.
- Provide reusable risk analytical results for downstream services.

Business calculations and analytical interpretation are implemented
here, while database access is delegated to PortfolioRepository.

The service currently operates on the latest available portfolio
snapshot. The design allows historical snapshot comparison to be
introduced later without changing the repository boundary.
"""

from typing import Any, Dict, List, Optional

from src.database.portfolio_repository import PortfolioRepository


class PortfolioRiskService:
    """
    Service responsible for portfolio risk analysis.
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
    # Risk Distribution
    # --------------------------------------------------------------

    def analyze_risk_distribution(self) -> Dict[str, Any]:
        """
        Analyse the latest portfolio risk distribution.

        Returns
        -------
        dict
            Portfolio risk distribution summary.

        Raises
        ------
        ValueError
            If no portfolio risk data is available.
        """

        rows = self.repository.get_portfolio_risk()

        if not rows:
            raise ValueError(
                "No portfolio risk data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        total_customers = sum(
            row["customer_count"]
            for row in latest_snapshot
        )

        total_exposure = sum(
            row["exposure_amount"]
            for row in latest_snapshot
        )

        return {
            "snapshot_date": latest_snapshot[0]["snapshot_date"],
            "total_customers": total_customers,
            "total_exposure": round(total_exposure, 2),
            "risk_band_count": len(latest_snapshot),
            "risk_bands": latest_snapshot,
        }

    # --------------------------------------------------------------
    # Customer Distribution by Risk Band
    # --------------------------------------------------------------

    def get_customer_distribution(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return risk bands enriched with customer population
        percentages.

        Returns
        -------
        list[dict]
            Risk distribution records.
        """

        rows = self.repository.get_portfolio_risk()

        if not rows:
            raise ValueError(
                "No portfolio risk data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        total_customers = sum(
            row["customer_count"]
            for row in latest_snapshot
        )

        distribution = []

        for row in latest_snapshot:

            customer_count = row["customer_count"]

            percentage = (
                (customer_count / total_customers) * 100
                if total_customers
                else 0.0
            )

            risk_band = dict(row)

            risk_band["customer_percentage"] = round(
                percentage,
                2,
            )

            distribution.append(risk_band)

        return distribution

    # --------------------------------------------------------------
    # Exposure Distribution by Risk Band
    # --------------------------------------------------------------

    def get_exposure_distribution(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return risk bands enriched with exposure percentages.

        Returns
        -------
        list[dict]
            Risk exposure distribution.
        """

        rows = self.repository.get_portfolio_risk()

        if not rows:
            raise ValueError(
                "No portfolio risk data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        total_exposure = sum(
            row["exposure_amount"]
            for row in latest_snapshot
        )

        distribution = []

        for row in latest_snapshot:

            exposure_amount = row["exposure_amount"]

            percentage = (
                (exposure_amount / total_exposure) * 100
                if total_exposure
                else 0.0
            )

            risk_band = dict(row)

            risk_band["exposure_percentage"] = round(
                percentage,
                2,
            )

            distribution.append(risk_band)

        return distribution

    # --------------------------------------------------------------
    # Dominant Risk Band
    # --------------------------------------------------------------

    def get_dominant_risk_band(self) -> Dict[str, Any]:
        """
        Identify the risk band containing the largest number
        of customers.
        """

        rows = self.repository.get_portfolio_risk()

        if not rows:
            raise ValueError(
                "No portfolio risk data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        return max(
            latest_snapshot,
            key=lambda row: row["customer_count"],
        )

    # --------------------------------------------------------------
    # Highest Exposure Risk Band
    # --------------------------------------------------------------

    def get_highest_exposure_risk_band(
        self,
    ) -> Dict[str, Any]:
        """
        Identify the risk band with the highest portfolio exposure.
        """

        rows = self.repository.get_portfolio_risk()

        if not rows:
            raise ValueError(
                "No portfolio risk data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        return max(
            latest_snapshot,
            key=lambda row: row["exposure_amount"],
        )

    # --------------------------------------------------------------
    # Default Risk Summary
    # --------------------------------------------------------------

    def get_default_risk_summary(
        self,
    ) -> Dict[str, Any]:
        """
        Provide a weighted portfolio default-rate summary based
        on the customer population represented by each risk band.

        Returns
        -------
        dict
            Weighted default-rate summary.
        """

        rows = self.repository.get_portfolio_risk()

        if not rows:
            raise ValueError(
                "No portfolio risk data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        total_customers = sum(
            row["customer_count"]
            for row in latest_snapshot
        )

        if total_customers == 0:
            return {
                "snapshot_date": latest_snapshot[0]["snapshot_date"],
                "default_rate": 0.0,
            }

        weighted_default_rate = sum(
            row["default_rate"] * row["customer_count"]
            for row in latest_snapshot
        ) / total_customers

        return {
            "snapshot_date": latest_snapshot[0]["snapshot_date"],
            "default_rate": round(
                weighted_default_rate,
                2,
            ),
        }

    # --------------------------------------------------------------
    # Latest Snapshot
    # --------------------------------------------------------------

    @staticmethod
    def _get_latest_snapshot(
        rows: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Extract records belonging to the latest snapshot date.

        The repository may contain multiple historical snapshots.
        This method explicitly selects the latest available snapshot
        rather than relying on query ordering.
        """

        latest_date = max(
            row["snapshot_date"]
            for row in rows
        )

        return [
            row
            for row in rows
            if row["snapshot_date"] == latest_date
        ]
