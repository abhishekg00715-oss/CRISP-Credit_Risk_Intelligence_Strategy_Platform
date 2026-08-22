"""
portfolio_segment_service.py

Provides portfolio segmentation analytics.

Responsibilities
----------------
- Retrieve portfolio segmentation data from PortfolioRepository.
- Analyse customer distribution across portfolio segments.
- Identify dominant and high-risk segment characteristics.
- Provide reusable segment-level analytical results.
- Keep database access outside the analytics layer.

Business calculations and analytical interpretation are implemented
here, while data retrieval is delegated to PortfolioRepository.

The service currently operates on the latest available portfolio
snapshot. The design allows historical snapshot analysis to be
introduced later without changing the repository boundary.
"""

from typing import Any, Dict, List, Optional

from src.database.portfolio_repository import PortfolioRepository


class PortfolioSegmentService:
    """
    Service responsible for portfolio segment analysis.
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
    # Segment Analysis
    # --------------------------------------------------------------

    def analyze_segments(self) -> Dict[str, Any]:
        """
        Analyse the latest portfolio segmentation snapshot.

        Returns
        -------
        dict
            Segment-level analytical summary.

        Raises
        ------
        ValueError
            If no segmentation data is available.
        """

        rows = self.repository.get_portfolio_segmentation()

        if not rows:
            raise ValueError(
                "No portfolio segmentation data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        total_customers = sum(
            row["customer_count"]
            for row in latest_snapshot
        )

        return {
            "snapshot_date": latest_snapshot[0]["snapshot_date"],
            "total_customers": total_customers,
            "segment_count": len(latest_snapshot),
            "segments": latest_snapshot,
        }

    # --------------------------------------------------------------
    # Dominant Segment
    # --------------------------------------------------------------

    def get_dominant_segment(self) -> Dict[str, Any]:
        """
        Identify the segment with the highest customer count.

        Returns
        -------
        dict
            Segment with the largest customer population.
        """

        rows = self.repository.get_portfolio_segmentation()

        if not rows:
            raise ValueError(
                "No portfolio segmentation data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        return max(
            latest_snapshot,
            key=lambda row: row["customer_count"],
        )

    # --------------------------------------------------------------
    # Highest Utilisation Segment
    # --------------------------------------------------------------

    def get_highest_utilisation_segment(self) -> Dict[str, Any]:
        """
        Identify the segment with the highest average utilisation.

        Returns
        -------
        dict
            Segment with the highest average utilisation.
        """

        rows = self.repository.get_portfolio_segmentation()

        if not rows:
            raise ValueError(
                "No portfolio segmentation data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        return max(
            latest_snapshot,
            key=lambda row: row["average_utilisation"],
        )

    # --------------------------------------------------------------
    # Lowest Credit Score Segment
    # --------------------------------------------------------------

    def get_lowest_credit_score_segment(self) -> Dict[str, Any]:
        """
        Identify the segment with the lowest average credit score.

        Returns
        -------
        dict
            Segment with the lowest average credit score.
        """

        rows = self.repository.get_portfolio_segmentation()

        if not rows:
            raise ValueError(
                "No portfolio segmentation data is available."
            )

        latest_snapshot = self._get_latest_snapshot(rows)

        return min(
            latest_snapshot,
            key=lambda row: row["average_credit_score"],
        )

    # --------------------------------------------------------------
    # Customer Distribution
    # --------------------------------------------------------------

    def get_customer_distribution(self) -> List[Dict[str, Any]]:
        """
        Return segment records with customer population percentage.

        Returns
        -------
        list[dict]
            Segmentation records enriched with customer percentage.
        """

        rows = self.repository.get_portfolio_segmentation()

        if not rows:
            raise ValueError(
                "No portfolio segmentation data is available."
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

            segment = dict(row)

            segment["customer_percentage"] = round(
                percentage,
                2,
            )

            distribution.append(segment)

        return distribution

    # --------------------------------------------------------------
    # Latest Snapshot
    # --------------------------------------------------------------

    @staticmethod
    def _get_latest_snapshot(
        rows: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Extract records belonging to the latest snapshot date.

        The repository returns segmentation records across snapshots.
        This method deliberately identifies the latest snapshot rather
        than depending on repository ordering.
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
