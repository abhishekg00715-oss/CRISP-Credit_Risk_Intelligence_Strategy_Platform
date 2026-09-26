"""
portfolio_agent.py

Portfolio Agent responsible for orchestrating Portfolio Intelligence.

Responsibilities
----------------
- Accept portfolio-related user requests.
- Obtain the consolidated portfolio analytical summary.
- Delegate interpretation to PortfolioReasoningService.
- Return a structured PortfolioAgentResponse.

The Portfolio Agent intentionally does NOT:
- perform portfolio calculations,
- access the Portfolio Repository,
- invoke individual analytics services,
- determine analytics selection,
- construct LLM prompts,
- invoke the LLM directly.

Portfolio analytics remain within PortfolioAnalyticsService.

Summary consolidation remains within PortfolioSummaryService.

LLM reasoning remains within PortfolioReasoningService.
"""

from typing import Optional

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)

from src.services.portfolio_summary_service import (
    PortfolioSummaryService,
)

from src.services.portfolio_reasoning_service import (
    PortfolioReasoningService,
)


class PortfolioAgent:
    """
    Agent responsible for Portfolio Intelligence requests.

    The agent obtains the consolidated analytical summary
    and delegates interpretation to PortfolioReasoningService.
    """

    def __init__(
        self,
        summary_service: PortfolioSummaryService,
        reasoning_service: PortfolioReasoningService,
    ) -> None:

        self.summary_service = summary_service

        self.reasoning_service = reasoning_service

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
        1. Obtain the consolidated analytical summary.
        2. Pass the summary and user query to the reasoning service.
        3. Return the structured PortfolioAgentResponse.
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
            # Step 1: Obtain consolidated analytical summary
            # ------------------------------------------------------

            analytical_context = (
                self.summary_service
                .get_summary()
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

