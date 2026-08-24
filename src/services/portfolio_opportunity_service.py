"""
portfolio_opportunity_service.py

Provides portfolio opportunity analytics.

Responsibilities
----------------
- Retrieve portfolio opportunity data from PortfolioRepository.
- Analyse opportunity types.
- Identify highest-value and highest-confidence opportunities.
- Calculate opportunity distributions.
- Provide reusable opportunity analytics for downstream services.

Business calculations are implemented within this service, while
database access remains encapsulated by PortfolioRepository.

This service does not generate customer-facing recommendations.
Recommendation generation belongs to the Recommendation Agent.
"""

from typing import Any, Dict, List, Optional

from src.repository.portfolio_repository import (
    PortfolioRepository,
)


class PortfolioOpportunityService:
    """
    Service responsible for portfolio opportunity analysis.
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
    # Opportunity Analysis
    # --------------------------------------------------------------

    def analyze_opportunities(self) -> Dict[str, Any]:
        """
        Analyse the available portfolio opportunities.

        Returns
        -------
        dict
            Consolidated opportunity analysis.

        Raises
        ------
        ValueError
            If no portfolio opportunity data is available.
        """

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        total_eligible_customers = sum(
            row["eligible_customers"]
            for row in rows
        )

        total_estimated_value = sum(
            row["estimated_value"]
            for row in rows
        )

        average_confidence = (
            sum(
                row["confidence_score"]
                for row in rows
            )
            / len(rows)
        )

        highest_value = max(
            rows,
            key=lambda row: row["estimated_value"],
        )

        highest_confidence = max(
            rows,
            key=lambda row: row["confidence_score"],
        )

        return {
            "snapshot_date": rows[0]["snapshot_date"],
            "opportunity_count": len(rows),
            "total_eligible_customers": (
                total_eligible_customers
            ),
            "total_estimated_value": round(
                total_estimated_value,
                2,
            ),
            "average_confidence_score": round(
                average_confidence,
                2,
            ),
            "highest_value_opportunity": dict(
                highest_value
            ),
            "highest_confidence_opportunity": dict(
                highest_confidence
            ),
        }

    # --------------------------------------------------------------
    # Opportunity Distribution
    # --------------------------------------------------------------

    def get_opportunity_distribution(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return opportunity records enriched with their share of
        the total estimated opportunity value.

        Returns
        -------
        list[dict]
            Opportunity distribution.
        """

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        total_value = sum(
            row["estimated_value"]
            for row in rows
        )

        distribution = []

        for row in rows:

            estimated_value = row["estimated_value"]

            value_percentage = (
                (
                    estimated_value
                    / total_value
                    * 100
                )
                if total_value
                else 0.0
            )

            opportunity = dict(row)

            opportunity[
                "value_percentage"
            ] = round(
                value_percentage,
                2,
            )

            distribution.append(
                opportunity
            )

        return distribution

    # --------------------------------------------------------------
    # Eligible Customers
    # --------------------------------------------------------------

    def get_customer_opportunity_distribution(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return opportunities ranked by eligible customer count.
        """

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        return sorted(
            (
                dict(row)
                for row in rows
            ),
            key=lambda row: row[
                "eligible_customers"
            ],
            reverse=True,
        )

    # --------------------------------------------------------------
    # Estimated Value
    # --------------------------------------------------------------

    def get_value_distribution(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return opportunities ranked by estimated value.
        """

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        return sorted(
            (
                dict(row)
                for row in rows
            ),
            key=lambda row: row[
                "estimated_value"
            ],
            reverse=True,
        )

    # --------------------------------------------------------------
    # Confidence Analysis
    # --------------------------------------------------------------

    def get_confidence_distribution(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return opportunities ranked by confidence score.
        """

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        return sorted(
            (
                dict(row)
                for row in rows
            ),
            key=lambda row: row[
                "confidence_score"
            ],
            reverse=True,
        )

    # --------------------------------------------------------------
    # Highest Value Opportunity
    # --------------------------------------------------------------

    def get_highest_value_opportunity(
        self,
    ) -> Dict[str, Any]:
        """
        Identify the opportunity with the highest estimated value.
        """

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        return dict(
            max(
                rows,
                key=lambda row: row[
                    "estimated_value"
                ],
            )
        )

    # --------------------------------------------------------------
    # Highest Confidence Opportunity
    # --------------------------------------------------------------

    def get_highest_confidence_opportunity(
        self,
    ) -> Dict[str, Any]:
        """
        Identify the opportunity with the highest confidence score.
        """

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        return dict(
            max(
                rows,
                key=lambda row: row[
                    "confidence_score"
                ],
            )
        )

    # --------------------------------------------------------------
    # High-Confidence Opportunities
    # --------------------------------------------------------------

    def get_high_confidence_opportunities(
        self,
        threshold: float = 0.70,
    ) -> List[Dict[str, Any]]:
        """
        Return opportunities meeting the supplied confidence
        threshold.

        Parameters
        ----------
        threshold:
            Minimum confidence score.

        Returns
        -------
        list[dict]
            Opportunities meeting the threshold.
        """

        if not 0 <= threshold <= 1:

            raise ValueError(
                "Confidence threshold must be between "
                "0 and 1."
            )

        rows = self.repository.get_portfolio_opportunities()

        if not rows:
            raise ValueError(
                "No portfolio opportunity data is available."
            )

        return [
            dict(row)
            for row in rows
            if row["confidence_score"] >= threshold
        ]

    # --------------------------------------------------------------
    # Internal Validation
    # --------------------------------------------------------------

    @staticmethod
    def _validate_rows(
        rows: List[Dict[str, Any]],
    ) -> None:
        """
        Validate the minimum analytical fields required by the
        opportunity service.
        """

        required_fields = {
            "snapshot_date",
            "opportunity_type",
            "eligible_customers",
            "estimated_value",
            "confidence_score",
        }

        for row in rows:

            missing_fields = (
                required_fields
                - row.keys()
            )

            if missing_fields:

                raise ValueError(
                    "Portfolio opportunity record is missing "
                    f"required fields: {sorted(missing_fields)}"
                )
