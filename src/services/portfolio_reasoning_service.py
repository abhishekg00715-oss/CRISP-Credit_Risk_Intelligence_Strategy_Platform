"""
portfolio_reasoning_service.py

LLM-enabled reasoning service for Portfolio Intelligence.

Responsibilities
----------------
- Accept the user query and complete analytical context.
- Build the reasoning prompt.
- Invoke the configured LLM service.
- Return structured portfolio reasoning.

The service does NOT:
- Access databases.
- Perform portfolio calculations.
- Select individual analytics services.
- Depend on a specific LLM vendor or framework.
"""

from typing import Any, Dict, Optional

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)

from src.services.llm_service import (
    LLMService,
)

from src.services.portfolio_reasoning_prompt import (
    PortfolioReasoningPromptBuilder,
)


class PortfolioReasoningService:
    """
    LLM-enabled Portfolio Intelligence reasoning service.
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        prompt_builder: Optional[
            PortfolioReasoningPromptBuilder
        ] = None,
    ) -> None:
    
        self.llm_service = (
            llm_service
            if llm_service is not None
            else LLMService()
        )

        self.prompt_builder = (
            prompt_builder
            if prompt_builder is not None
            else PortfolioReasoningPromptBuilder()
        )

    # --------------------------------------------------------------
    # Main Reasoning Entry Point
    # --------------------------------------------------------------

    def reason(
        self,
        query: str,
        analytical_context: Dict[str, Any],
    ) -> PortfolioAgentResponse:
        """
        Generate portfolio reasoning from analytical context.
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

        try:

            facts = self._build_facts(
                analytical_context
            )

            evidence = self._build_evidence(
                analytical_context
            )

            # ------------------------------------------------------
            # LLM Reasoning
            # ------------------------------------------------------

            if self.llm_service is None:

                return PortfolioAgentResponse(
                    success=True,
                    query=query,
                    facts=facts,
                    evidence=evidence,
                    message=(
                        "Analytical context prepared. "
                        "LLM service is not configured."
                    ),
                )

            prompt = (
                self.prompt_builder.build(
                    query=query,
                    analytical_context=analytical_context,
                )
            )

            llm_response = (
                self.llm_service.generate_response(
                    prompt
                )
            )

            return self._build_llm_response(
                query=query,
                facts=facts,
                evidence=evidence,
                llm_response=llm_response,
            )

        except Exception as exc:

            return PortfolioAgentResponse.error_response(
                message=(
                    "Portfolio reasoning failed: "
                    f"{str(exc)}"
                ),
                query=query,
            )

    # --------------------------------------------------------------
    # LLM Response Mapping
    # --------------------------------------------------------------

    def _build_llm_response(
        self,
        query: str,
        facts: list[dict],
        evidence: list[dict],
        llm_response: str,
    ) -> PortfolioAgentResponse:
        """
        Map the LLM response into PortfolioAgentResponse.

        Initial implementation keeps the raw LLM output inside
        observations until structured-output parsing is introduced.
        """

        return PortfolioAgentResponse(
            success=True,
            query=query,
            facts=facts,
            observations=[
                {
                    "type": "llm_analysis",
                    "content": llm_response,
                }
            ],
            risks=[],
            trends=[],
            opportunities=[],
            evidence=evidence,
            message=(
                "Portfolio reasoning completed successfully."
            ),
        )

    # --------------------------------------------------------------
    # Facts
    # --------------------------------------------------------------

    @staticmethod
    def _build_facts(
        analytical_context: Dict[str, Any],
    ) -> list[dict]:
        """
        Preserve analytical domains as structured facts.
        """

        return [
            {
                "domain": domain,
                "data": data,
            }
            for domain, data
            in analytical_context.items()
        ]

    # --------------------------------------------------------------
    # Evidence
    # --------------------------------------------------------------

    @staticmethod
    def _build_evidence(
        analytical_context: Dict[str, Any],
    ) -> list[dict]:
        """
        Preserve analytical-domain traceability.
        """

        return [
            {
                "source": "PortfolioAnalyticsService",
                "domain": domain,
            }
            for domain in analytical_context
        ]
