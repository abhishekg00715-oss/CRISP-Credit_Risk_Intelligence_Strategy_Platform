"""
    portfolio_summary_service.py

    Consolidates portfolio analytics into a reusable executive
    analytical summary.

    Responsibility
    --------------
    - Retrieve the analytical snapshot from PortfolioAnalyticsService.
    - Organize the snapshot into a stable summary contract.
    - Preserve deterministic analytical facts.
    - Provide source/evidence metadata for downstream consumers.

    This service does NOT:
    - perform portfolio calculations;
    - access the portfolio repository directly;
    - generate natural-language narrative;
    - invoke an LLM;
    - determine query intent;
    - selectively invoke individual analytics services.

    Architectural position
    -----------------------
        Portfolio Repository
                ↓
        PortfolioAnalyticsService
                ↓
        PortfolioSummaryService
                ↓
        PortfolioAgent / Reasoning Layer
"""



from typing import Any, Dict

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


class PortfolioSummaryService:
   

    SUMMARY_SOURCE = "PortfolioSummaryService"

    def __init__(
        self,
        analytics_service: PortfolioAnalyticsService,
    ):
        self._analytics_service = analytics_service

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def get_summary(self) -> Dict[str, Any]:
        """
        Return the consolidated analytical portfolio summary.

        The summary is deterministic and contains analytical facts
        only. Natural-language interpretation belongs to the
        PortfolioReasoningService.
        """

        snapshot = (
            self._analytics_service
            .get_analytical_snapshot()
        )

        return self._build_summary(
            snapshot
        )

    # --------------------------------------------------------------
    # Summary Construction
    # --------------------------------------------------------------

    def _build_summary(
        self,
        snapshot: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Convert the analytics snapshot into the stable
        PortfolioSummaryService contract.
        """

        return {
            "summary": {
                "kpis": snapshot.get(
                    "kpis",
                    {},
                ),

                "risk": snapshot.get(
                    "risk",
                    {},
                ),

                "exposure": snapshot.get(
                    "exposure",
                    {},
                ),

                "trends": snapshot.get(
                    "trends",
                    {},
                ),

                "opportunities": snapshot.get(
                    "opportunities",
                    {},
                ),
            },

            "evidence": {
                "source": self.SUMMARY_SOURCE,
                "upstream_source": "PortfolioAnalyticsService",
            },
        }

    # --------------------------------------------------------------
    # Convenience Accessors
    # --------------------------------------------------------------

    def get_kpis(self) -> Dict[str, Any]:
        """
        Return portfolio KPI information from the consolidated
        summary.
        """

        return (
            self.get_summary()
            .get("summary", {})
            .get("kpis", {})
        )

    def get_risk_summary(self) -> Dict[str, Any]:
        """
        Return the consolidated portfolio risk position.
        """

        return (
            self.get_summary()
            .get("summary", {})
            .get("risk", {})
        )

    def get_exposure_summary(self) -> Dict[str, Any]:
        """
        Return the consolidated portfolio exposure position.
        """

        return (
            self.get_summary()
            .get("summary", {})
            .get("exposure", {})
        )

    def get_trend_summary(self) -> Dict[str, Any]:
        """
        Return the consolidated portfolio trend position.
        """

        return (
            self.get_summary()
            .get("summary", {})
            .get("trends", {})
        )

    def get_opportunity_summary(self) -> Dict[str, Any]:
        """
        Return the consolidated portfolio opportunity position.
        """

        return (
            self.get_summary()
            .get("summary", {})
            .get("opportunities", {})
        )
