"""
portfolio_agent.py

Portfolio Agent responsible for orchestrating Portfolio Intelligence.

Responsibilities
----------------
- Accept portfolio-related user requests.
- Retrieve the complete portfolio analytical context.
- Delegate reasoning to PortfolioReasoningService.
- Return a structured PortfolioAgentResponse.

The Portfolio Agent intentionally does NOT:
- perform portfolio calculations,
- directly access the Portfolio Repository,
- select individual analytical services,
- construct LLM prompts,
- invoke the LLM directly.

Analytical calculations remain within the specialised portfolio
analytics services.

LLM reasoning remains encapsulated within PortfolioReasoningService.

The Agent therefore acts as a thin orchestration layer between
the portfolio analytics and reasoning capabilities.
"""

from typing import Optional

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)

from src.services.portfolio_reasoning_service import (
    PortfolioReasoningService,
)


class PortfolioAgent:
    """
    Agent responsible for Portfolio Intelligence requests.

    The agent retrieves the complete analytical portfolio context
    and delegates interpretation and reasoning to the
    PortfolioReasoningService.
    """

    def __init__(
        self,
        analytics_service: Optional[
            PortfolioAnalyticsService
        ] = None,
        reasoning_service: Optional[
            PortfolioReasoningService
        ] = None,
    ) -> None:

        self.analytics_service = (
            analytics_service
            if analytics_service is not None
            else PortfolioAnalyticsService()
        )

        self.reasoning_service = (
            reasoning_service
            if reasoning_service is not None
            else PortfolioReasoningService()
        )

    # --------------------------------------------------------------
    # Portfolio Request Processing
    # --------------------------------------------------------------

    def process(
        self,
        query: str,
    ) -> PortfolioAgentResponse:
        """
        Process a portfolio intelligence request.

        Workflow
        --------
        1. Retrieve the complete analytical portfolio context.
        2. Pass the context and user query to the reasoning service.
        3. Return the structured PortfolioAgentResponse.

        The complete analytical context is intentionally provided
        to the reasoning service rather than selectively invoking
        individual portfolio analytics services.

        This allows the reasoning layer to determine which
        information is relevant to the user's request.
        """

        if not query or not query.strip():

            return PortfolioAgentResponse(
                success=False,
                query=query,
                message=(
                    "Portfolio query cannot be empty."
                ),
            )

        try:

            # ------------------------------------------------------
            # Step 1: Retrieve complete analytical context
            # ------------------------------------------------------

            analytical_context = (
                self.analytics_service
                .get_full_analytical_context()
            )

            # ------------------------------------------------------
            # Step 2: Delegate reasoning
            # ------------------------------------------------------

            return (
                self.reasoning_service
                .reason(
                    query=query,
                    analytical_context=analytical_context,
                )
            )

        except Exception as exc:

            return PortfolioAgentResponse(
                success=False,
                query=query,
                message=(
                    f"Portfolio agent processing failed: {exc}"
                ),
            )
