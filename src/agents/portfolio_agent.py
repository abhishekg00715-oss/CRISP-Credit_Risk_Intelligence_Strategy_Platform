"""
portfolio_agent.py

Portfolio Intelligence Agent responsible for orchestrating
portfolio analytics and constructing the standardized
Portfolio Agent response.

Responsibilities
----------------
- Accept portfolio-related user requests.
- Retrieve the complete analytical portfolio context.
- Construct a standardized PortfolioAgentResponse.
- Provide a clean integration boundary for future LLM-based
  reasoning and narrative generation.

The agent does NOT:
- Access the Portfolio Repository directly.
- Perform business calculations.
- Select individual portfolio analytics services.
- Implement portfolio business rules.
- Perform natural-language interpretation itself.

Portfolio analytics are provided by PortfolioAnalyticsService.
Future LLM reasoning will consume the analytical context and
populate the interpretive sections of PortfolioAgentResponse.
"""

from typing import Any, Dict, Optional

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)


class PortfolioAgent:
    """
    Portfolio Intelligence Agent.

    Acts as the orchestration boundary between the Coordinator,
    PortfolioAnalyticsService and the future reasoning /
    narrative generation layer.
    """

    def __init__(
        self,
        analytics_service: Optional[
            PortfolioAnalyticsService
        ] = None,
    ) -> None:

        self.analytics_service = (
            analytics_service
            if analytics_service is not None
            else PortfolioAnalyticsService()
        )

    # ==============================================================
    # Main Agent Entry Point
    # ==============================================================

    def process(
        self,
        query: str,
    ) -> PortfolioAgentResponse:
        """
        Process a portfolio-related user request.

        The complete portfolio analytical context is retrieved
        through PortfolioAnalyticsService.

        The agent deliberately does not select individual
        analytical capabilities based on the user query.

        Parameters
        ----------
        query:
            Portfolio-related user request.

        Returns
        -------
        PortfolioAgentResponse
            Standardized portfolio agent response.
        """

        if not query or not query.strip():

            return PortfolioAgentResponse.error_response(
                message="Portfolio query cannot be empty.",
                query=query,
            )

        try:

            analytical_context = (
                self.get_analytical_context()
            )

            return self._build_response(
                query=query,
                analytical_context=analytical_context,
            )

        except Exception as exc:

            return PortfolioAgentResponse.error_response(
                message=(
                    "Unable to retrieve portfolio "
                    f"analytics: {str(exc)}"
                ),
                query=query,
            )

    # ==============================================================
    # Analytical Context
    # ==============================================================

    def get_analytical_context(
        self,
    ) -> Dict[str, Any]:
        """
        Retrieve the complete portfolio analytical context.

        PortfolioAgent uses the consolidated analytics interface
        rather than directly invoking individual analytical
        services.

        Returns
        -------
        Dict[str, Any]
            Complete structured portfolio analytical context.
        """

        return (
            self.analytics_service
            .get_full_analytical_context()
        )

    # ==============================================================
    # Response Construction
    # ==============================================================

    def _build_response(
        self,
        query: str,
        analytical_context: Dict[str, Any],
    ) -> PortfolioAgentResponse:
        """
        Construct the PortfolioAgentResponse.

        At the current implementation stage, the complete
        analytical context is exposed as facts.

        Future LLM integration will interpret these facts and
        populate observations, risks, trends, opportunities
        and evidence without changing the agent contract.
        """

        facts = self._extract_facts(
            analytical_context
        )

        return PortfolioAgentResponse.success_response(
            query=query,
            facts=facts,
            message=(
                "Portfolio analytics retrieved "
                "successfully."
            ),
        )

    # ==============================================================
    # Fact Preparation
    # ==============================================================

    @staticmethod
    def _extract_facts(
        analytical_context: Dict[str, Any],
    ) -> list[dict]:
        """
        Convert the consolidated analytical context into the
        fact collection expected by PortfolioAgentResponse.

        The method does not perform business calculations or
        interpretation. It only preserves the analytical
        information returned by PortfolioAnalyticsService.

        Each analytical domain is represented as a separate
        fact entry to maintain domain traceability.
        """

        facts = []

        for domain, analytical_data in (
            analytical_context.items()
        ):

            facts.append(
                {
                    "domain": domain,
                    "data": analytical_data,
                }
            )

        return facts
