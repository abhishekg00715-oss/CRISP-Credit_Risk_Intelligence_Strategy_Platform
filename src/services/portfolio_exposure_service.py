"""
portfolio_exposure_service.py

Provides portfolio exposure analytics.

Responsibilities
----------------
- Retrieve portfolio exposure data from PortfolioRepository.
- Analyse exposure across products and geographic dimensions.
- Identify dominant exposure categories.
- Calculate exposure distribution and concentration metrics.
- Provide reusable exposure-level analytical results.

Business calculations and analytical interpretation are implemented
here, while database access is delegated to PortfolioRepository.

The service currently operates on the latest available portfolio
snapshot. The design allows historical snapshot comparison to be
introduced later without changing the repository boundary.
"""

from typing import Any, Dict, List, Optional

from src.database.portfolio_repository import PortfolioRepository


class PortfolioExposureService:
    """
    Service responsible for portfolio exposure analysis.
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
    # Exposure Analysis
    # --------------------------------------------------------------

    def analyze_exposure(self) -> Dict[str, Any]:
        """
        Analyse the latest portfolio exposure snapshot.

        Returns
        -------
        dict
            Portfolio exposure analytical summary.

        Raises
        ------
        ValueError
            If no portfolio exposure data is available.
        """

        rows = self.repository.get_portfolio_exposure()

        if not rows:
            raise ValueError(
                "No portfolio exposure data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        total_exposure = sum(
            row["exposure_amount"]
            for row in latest_snapshot
        )

        return {
            "snapshot_date": latest_snapshot[0]["snapshot_date"],
            "total_exposure": round(total_exposure, 2),
            "exposure_categories": len(latest_snapshot),
            "exposures": latest_snapshot,
        }

    # --------------------------------------------------------------
    # Exposure Distribution
    # --------------------------------------------------------------

    def get_exposure_distribution(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return exposure records enriched with exposure percentages.

        Returns
        -------
        list[dict]
            Exposure distribution across product and state
            combinations.
        """

        rows = self.repository.get_portfolio_exposure()

        if not rows:
            raise ValueError(
                "No portfolio exposure data is available."
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

            exposure = dict(row)

            exposure["exposure_percentage"] = round(
                percentage,
                2,
            )

            distribution.append(exposure)

        return distribution

    # --------------------------------------------------------------
    # Product Exposure
    # --------------------------------------------------------------

    def get_product_exposure(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Aggregate portfolio exposure by product type.

        Returns
        -------
        list[dict]
            Exposure totals by product type.
        """

        rows = self.repository.get_portfolio_exposure()

        if not rows:
            raise ValueError(
                "No portfolio exposure data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        product_exposure: Dict[str, float] = {}

        for row in latest_snapshot:

            product_type = row["product_type"]

            product_exposure[product_type] = (
                product_exposure.get(product_type, 0.0)
                + row["exposure_amount"]
            )

        return [
            {
                "product_type": product_type,
                "exposure_amount": round(
                    exposure_amount,
                    2,
                ),
            }
            for product_type, exposure_amount
            in sorted(
                product_exposure.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]

    # --------------------------------------------------------------
    # Geographic Exposure
    # --------------------------------------------------------------

    def get_geographic_exposure(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Aggregate portfolio exposure by state.

        Returns
        -------
        list[dict]
            Exposure totals by state.
        """

        rows = self.repository.get_portfolio_exposure()

        if not rows:
            raise ValueError(
                "No portfolio exposure data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        state_exposure: Dict[str, float] = {}

        for row in latest_snapshot:

            state = row["state"]

            state_exposure[state] = (
                state_exposure.get(state, 0.0)
                + row["exposure_amount"]
            )

        return [
            {
                "state": state,
                "exposure_amount": round(
                    exposure_amount,
                    2,
                ),
            }
            for state, exposure_amount
            in sorted(
                state_exposure.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]

    # --------------------------------------------------------------
    # Highest Exposure
    # --------------------------------------------------------------

    def get_highest_exposure_category(
        self,
    ) -> Dict[str, Any]:
        """
        Identify the product/state combination with the highest
        exposure.
        """

        rows = self.repository.get_portfolio_exposure()

        if not rows:
            raise ValueError(
                "No portfolio exposure data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        return max(
            latest_snapshot,
            key=lambda row: row["exposure_amount"],
        )

    # --------------------------------------------------------------
    # Exposure Concentration
    # --------------------------------------------------------------

    def get_exposure_concentration(
        self,
    ) -> Dict[str, Any]:
        """
        Identify the largest product and geographic exposure
        concentrations.

        Returns
        -------
        dict
            Concentration metrics for product and state.
        """

        product_exposure = self.get_product_exposure()
        geographic_exposure = self.get_geographic_exposure()

        total_exposure = sum(
            item["exposure_amount"]
            for item in product_exposure
        )

        if total_exposure == 0:
            return {
                "total_exposure": 0.0,
                "largest_product": None,
                "largest_product_percentage": 0.0,
                "largest_state": None,
                "largest_state_percentage": 0.0,
            }

        largest_product = (
            product_exposure[0]
            if product_exposure
            else None
        )

        largest_state = (
            geographic_exposure[0]
            if geographic_exposure
            else None
        )

        return {
            "total_exposure": round(
                total_exposure,
                2,
            ),
            "largest_product": (
                largest_product["product_type"]
                if largest_product
                else None
            ),
            "largest_product_percentage": round(
                (
                    largest_product["exposure_amount"]
                    / total_exposure
                    * 100
                )
                if largest_product
                else 0.0,
                2,
            ),
            "largest_state": (
                largest_state["state"]
                if largest_state
                else None
            ),
            "largest_state_percentage": round(
                (
                    largest_state["exposure_amount"]
                    / total_exposure
                    * 100
                )
                if largest_state
                else 0.0,
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
        rather than depending on repository ordering.
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
