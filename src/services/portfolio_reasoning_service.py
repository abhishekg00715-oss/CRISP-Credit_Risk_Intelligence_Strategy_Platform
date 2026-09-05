
"""
portfolio_reasoning_service.py

LLM-enabled reasoning service for Portfolio Intelligence.

Responsibilities
----------------
- Accept the user query and complete analytical context.
- Build the reasoning prompt.
- Invoke the configured LLM service.
- Parse and validate structured LLM reasoning.
- Return structured portfolio reasoning.

The service does NOT:
- Access databases.
- Perform portfolio calculations.
- Select individual analytics services.
- Depend on a specific LLM vendor or framework.
"""

import json
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

    REQUIRED_REASONING_FIELDS = (
        "observations",
        "risks",
        "trends",
        "opportunities",
    )

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
        Generate structured portfolio reasoning from
        deterministic analytical context.
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
        Parse and map the structured LLM response into
        PortfolioAgentResponse.

        The LLM is expected to return a JSON object containing:

        - observations
        - risks
        - trends
        - opportunities

        Evidence remains deterministic and is supplied by the
        PortfolioReasoningService rather than being generated
        by the LLM.
        """

        try:

            reasoning = self._parse_llm_response(
                llm_response
            )

            return PortfolioAgentResponse(
                success=True,
                query=query,
                facts=facts,
                observations=reasoning["observations"],
                risks=reasoning["risks"],
                trends=reasoning["trends"],
                opportunities=reasoning["opportunities"],
                evidence=evidence,
                message=(
                    "Portfolio reasoning completed successfully."
                ),
            )

        except ValueError as exc:

            return PortfolioAgentResponse.error_response(
                message=(
                    "Portfolio reasoning failed: "
                    f"{str(exc)}"
                ),
                query=query,
            )

    # --------------------------------------------------------------
    # LLM Response Parsing
    # --------------------------------------------------------------

    @classmethod
    def _parse_llm_response(
        cls,
        llm_response: str,
    ) -> Dict[str, list]:
        """
        Parse and validate the structured LLM response.

        Supports:
        - Plain JSON responses.
        - JSON responses wrapped in markdown code fences.

        Raises
        ------
        ValueError
            If the response is empty, invalid JSON, does not
            contain an object, or is missing required sections.
        """

        if not llm_response or not llm_response.strip():

            raise ValueError(
                "LLM returned an empty response."
            )

        cleaned_response = (
            cls._clean_llm_response(
                llm_response
            )
        )

        try:

            parsed_response = json.loads(
                cleaned_response
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "LLM returned invalid structured JSON."
            ) from exc

        if not isinstance(
            parsed_response,
            dict,
        ):

            raise ValueError(
                "LLM structured response must be a JSON object."
            )

        missing_fields = [
            field
            for field in cls.REQUIRED_REASONING_FIELDS
            if field not in parsed_response
        ]

        if missing_fields:

            raise ValueError(
                "LLM structured response is missing "
                "required fields: "
                + ", ".join(missing_fields)
            )

        for field in cls.REQUIRED_REASONING_FIELDS:

            value = parsed_response[field]

            if not isinstance(value, list):

                raise ValueError(
                    f"LLM reasoning field '{field}' "
                    "must be a JSON array."
                )

        return {
            field: parsed_response[field]
            for field in cls.REQUIRED_REASONING_FIELDS
        }

    # --------------------------------------------------------------
    # LLM Response Cleanup
    # --------------------------------------------------------------

    @staticmethod
    def _clean_llm_response(
        llm_response: str,
    ) -> str:
        """
        Remove common markdown wrappers around JSON.

        Example supported response:

        ```json
        {
            "observations": [],
            "risks": [],
            "trends": [],
            "opportunities": []
        }
        ```
        """

        response = llm_response.strip()

        if response.startswith("```"):

            lines = response.splitlines()

            if lines:

                lines = lines[1:]

            if lines and lines[-1].strip() == "```":

                lines = lines[:-1]

            response = "\n".join(lines).strip()

        return response

    # --------------------------------------------------------------
    # Facts
    # --------------------------------------------------------------

    @staticmethod
    def _build_facts(
        analytical_context: Dict[str, Any],
    ) -> list[dict]:
        """
        Preserve analytical domains as structured facts.

        Facts originate from deterministic analytics and are not
        generated by the LLM.
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

        Evidence identifies the deterministic analytical service
        and domain that supplied the reasoning context.
        """

        return [
            {
                "source": "PortfolioAnalyticsService",
                "domain": domain,
            }
            for domain in analytical_context
        ]
