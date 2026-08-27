"""
portfolio_reasoning_service.py

Provides the reasoning boundary for Portfolio Intelligence.

Responsibilities
----------------
- Accept a portfolio user query and analytical context.
- Interpret the analytical context at a structural level.
- Prepare the information required for portfolio insight generation.
- Populate the interpretive sections of PortfolioAgentResponse.
- Preserve analytical evidence for explainability.

The service does NOT:
- Access the Portfolio Repository directly.
- Perform portfolio calculations.
- Select individual analytics services.
- Implement intent routing.
- Depend on a specific LLM provider.

LLM-based reasoning can be introduced behind this service later
without changing PortfolioAgent or PortfolioAnalyticsService.
"""

from typing import Any, Dict, List

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)


class PortfolioReasoningService:
    """
    Reasoning service for Portfolio Intelligence.

    Acts as the boundary between deterministic portfolio analytics
    and future LLM-based interpretation.
    """

    # --------------------------------------------------------------
    # Main Reasoning Entry Point
    # --------------------------------------------------------------

    def reason(
        self,
        query: str,
        analytical_context: Dict[str, Any],
    ) -> PortfolioAgentResponse:
        """
        Generate a structured portfolio response from the
        supplied analytical context.

        Parameters
        ----------
        query:
            Original portfolio-related user request.

        analytical_context:
            Complete analytical context produced by
            PortfolioAnalyticsService.

        Returns
        -------
        PortfolioAgentResponse
            Structured portfolio response.

        Notes
        -----
        The current implementation provides deterministic
        structural reasoning only. LLM-backed interpretation
        can be introduced without changing this interface.
        """

        if not query or not query.strip():

            return PortfolioAgentResponse.error_response(
                message="Portfolio query cannot be empty.",
                query=query,
            )

        if not analytical_context:

            return PortfolioAgentResponse.error_response(
                message=(
                    "Portfolio analytical context "
                    "cannot be empty."
                ),
                query=query,
            )

        facts = self._build_facts(
            analytical_context
        )

        observations = self._build_observations(
            analytical_context
        )

        risks = self._build_risk_context(
            analytical_context
        )

        trends = self._build_trend_context(
            analytical_context
        )

        opportunities = self._build_opportunity_context(
            analytical_context
        )

        evidence = self._build_evidence(
            analytical_context
        )

        return PortfolioAgentResponse(
            success=True,
            query=query,
            facts=facts,
            observations=observations,
            risks=risks,
            trends=trends,
            opportunities=opportunities,
            evidence=evidence,
            message=(
                "Portfolio analytical context "
                "processed successfully."
            ),
        )

    # --------------------------------------------------------------
    # Facts
    # --------------------------------------------------------------

    @staticmethod
    def _build_facts(
        analytical_context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Preserve analytical information as structured facts.

        No calculations or interpretation are performed here.
        """

        facts = []

        for domain, data in analytical_context.items():

            facts.append(
                {
                    "domain": domain,
                    "data": data,
                }
            )

        return facts

    # --------------------------------------------------------------
    # Observations
    # --------------------------------------------------------------

    @staticmethod
    def _build_observations(
        analytical_context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Build high-level structural observations.

        The current implementation intentionally avoids
        generating natural-language conclusions. This method
        establishes the contract for future LLM reasoning.
        """

        observations = []

        if "kpis" in analytical_context:

            observations.append(
                {
                    "type": "portfolio_kpi_context",
                    "source": "kpis",
                }
            )

        if "segmentation" in analytical_context:

            observations.append(
                {
                    "type": "portfolio_segmentation_context",
                    "source": "segmentation",
                }
            )

        return observations

    # --------------------------------------------------------------
    # Risk Context
    # --------------------------------------------------------------

    @staticmethod
    def _build_risk_context(
        analytical_context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract the portfolio risk context.

        Risk calculations remain owned by PortfolioRiskService.
        """

        if "risk" not in analytical_context:

            return []

        return [
            {
                "source": "risk",
                "data": analytical_context["risk"],
            }
        ]

    # --------------------------------------------------------------
    # Trend Context
    # --------------------------------------------------------------

    @staticmethod
    def _build_trend_context(
        analytical_context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract the portfolio trend context.

        Trend calculations remain owned by PortfolioTrendService.
        """

        if "trends" not in analytical_context:

            return []

        return [
            {
                "source": "trends",
                "data": analytical_context["trends"],
            }
        ]

    # --------------------------------------------------------------
    # Opportunity Context
    # --------------------------------------------------------------

    @staticmethod
    def _build_opportunity_context(
        analytical_context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Extract the portfolio opportunity context.

        Opportunity calculations remain owned by
        PortfolioOpportunityService.
        """

        if "opportunities" not in analytical_context:

            return []

        return [
            {
                "source": "opportunities",
                "data": analytical_context["opportunities"],
            }
        ]

    # --------------------------------------------------------------
    # Evidence
    # --------------------------------------------------------------

    @staticmethod
    def _build_evidence(
        analytical_context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Build traceable evidence references from the analytical
        context.

        Evidence identifies the analytical domain from which the
        information originated.
        """

        evidence = []

        for domain in analytical_context:

            evidence.append(
                {
                    "source": "PortfolioAnalyticsService",
                    "domain": domain,
                }
            )

        return evidence