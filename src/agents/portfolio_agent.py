"""
portfolio_agent.py

Portfolio Intelligence Agent responsible for orchestrating
portfolio analytics and constructing portfolio insights.

Responsibilities
----------------
- Accept portfolio-related user requests.
- Retrieve the complete analytical portfolio context.
- Provide the analytical context to the reasoning/narrative layer.
- Construct a standardized portfolio response.

The agent does NOT:
- Access the Portfolio Repository directly.
- Perform business calculations.
- Select individual analytics services.
- Implement portfolio business rules.

Portfolio analytics are provided by PortfolioAnalyticsService.
The LLM, when enabled, is responsible for interpreting the
analytical evidence and generating narrative insights.
"""

from typing import Any, Dict, Optional

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


class PortfolioAgent:
    """
    Portfolio Intelligence Agent.

    Acts as the orchestration boundary between the Coordinator,
    PortfolioAnalyticsService and the downstream reasoning /
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
    ) -> Dict[str, Any]:
        """
        Process a portfolio-related user request.

        The complete portfolio analytical context is retrieved
        before reasoning. The agent does not selectively invoke
        individual analytical services based on the query.

        Parameters
        ----------
        query:
            User's portfolio-related question.

        Returns
        -------
        Dict[str, Any]
            Structured portfolio response.
        """

        if not query or not query.strip():

            return self._build_error_response(
                "Portfolio query cannot be empty."
            )

        analytical_context = (
            self.analytics_service
            .get_full_analytical_context()
        )

        return self._build_response(
            query=query,
            analytical_context=analytical_context,
        )

    # ==============================================================
    # Analytical Context
    # ==============================================================

    def get_analytical_context(
        self,
    ) -> Dict[str, Any]:
        """
        Retrieve the complete portfolio analytical context.

        This method provides a clean boundary between the agent
        and PortfolioAnalyticsService.

        No interpretation or narrative generation is performed.
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
    ) -> Dict[str, Any]:
        """
        Construct the standardized Portfolio Agent response.

        At this stage the response contains structured analytical
        evidence. LLM-based narrative generation can be introduced
        without changing the analytics or repository layers.
        """

        return {
            "success": True,

            "message": (
                "Portfolio analytics retrieved successfully."
            ),

            "query": query,

            "analytical_context": analytical_context,
        }

    # ==============================================================
    # Error Response
    # ==============================================================

    @staticmethod
    def _build_error_response(
        message: str,
    ) -> Dict[str, Any]:
        """
        Construct a standardized error response.
        """

        return {
            "success": False,

            "message": message,

            "query": None,

            "analytical_context": {},
        }
