"""
portfolio_agent.py

Portfolio Intelligence Agent responsible for orchestrating
portfolio analytics and portfolio reasoning.

Responsibilities
----------------
- Accept portfolio-related user requests.
- Retrieve the complete portfolio analytical context.
- Delegate interpretation to PortfolioReasoningService.
- Return the standardized PortfolioAgentResponse.

The agent does NOT:
- Access the Portfolio Repository directly.
- Perform business calculations.
- Select individual portfolio analytics services.
- Implement portfolio business rules.
- Implement LLM-specific reasoning.

PortfolioAnalyticsService owns analytical orchestration.

PortfolioReasoningService owns the reasoning boundary and can
later be backed by an LLM without changing the PortfolioAgent
contract.
"""

from typing import Any, Dict, Optional

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)

from src.services.portfolio_reasoning_service import (
    PortfolioReasoningService,
)

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)


class PortfolioAgent:
    """
    Portfolio Intelligence Agent.

    Acts as the orchestration boundary between the request,
    portfolio analytics and portfolio reasoning layers.
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

    # ==============================================================
    # Main Agent Entry Point
    # ==============================================================

    def process(
        self,
        query: str,
    ) -> PortfolioAgentResponse:
        """
        Process a portfolio-related user request.

        The agent retrieves the complete analytical context and
        delegates reasoning to PortfolioReasoningService.

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

            return self.reasoning_service.reason(
                query=query,
                analytical_context=analytical_context,
            )

        except Exception as exc:

            return PortfolioAgentResponse.error_response(
                message=(
                    "Unable to process portfolio request: "
                    f"{str(exc)}"
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

        PortfolioAgent deliberately consumes the consolidated
        analytics interface rather than invoking individual
        portfolio analytics services.

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
# Local Testing
# ==============================================================

if __name__ == "__main__":

    agent = PortfolioAgent()

    response = agent.process(
        "Provide an overview of the portfolio."
    )

    print()

    print("=" * 70)

    print(
        "PORTFOLIO AGENT"
    )

    print("=" * 70)

    print(
        response.to_dict()
    )

    print("=" * 70)