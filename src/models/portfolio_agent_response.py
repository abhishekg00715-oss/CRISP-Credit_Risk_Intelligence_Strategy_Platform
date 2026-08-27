"""
portfolio_agent_response.py

Response contract for the Portfolio Intelligence Agent.

Responsibilities
----------------
- Define the standardized response structure exposed by PortfolioAgent.
- Separate analytical facts from interpreted insights.
- Provide a consistent structure for risks, trends and opportunities.
- Support evidence and explainability.
- Remain independent of the LLM implementation.

Design Principles
-----------------
- The response model contains structured information only.
- Business calculations remain outside the response model.
- Evidence should originate from the analytical context.
- LLM-generated observations are represented separately from
  deterministic analytical facts.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PortfolioAgentResponse:
    """
    Standard response contract for PortfolioAgent.

    Attributes
    ----------
    success:
        Indicates whether the portfolio request was processed
        successfully.

    query:
        Original user query.

    facts:
        Deterministic analytical facts retrieved from the
        Portfolio Analytics Service.

    observations:
        Analytical observations derived from the available facts.

    risks:
        Identified portfolio risk findings.

    trends:
        Relevant portfolio trend findings.

    opportunities:
        Relevant portfolio opportunity findings.

    evidence:
        Supporting analytical evidence used to substantiate
        the response.

    message:
        Optional response or status message.
    """

    success: bool

    query: Optional[str]

    facts: List[Dict[str, Any]] = field(
        default_factory=list
    )

    observations: List[Dict[str, Any]] = field(
        default_factory=list
    )

    risks: List[Dict[str, Any]] = field(
        default_factory=list
    )

    trends: List[Dict[str, Any]] = field(
        default_factory=list
    )

    opportunities: List[Dict[str, Any]] = field(
        default_factory=list
    )

    evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    message: Optional[str] = None

    # --------------------------------------------------------------
    # Serialization
    # --------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response model into a serializable dictionary.

        This method provides a stable boundary between the domain
        response model and presentation/API layers.
        """

        return {
            "success": self.success,

            "query": self.query,

            "facts": self.facts,

            "observations": self.observations,

            "risks": self.risks,

            "trends": self.trends,

            "opportunities": self.opportunities,

            "evidence": self.evidence,

            "message": self.message,
        }

    # --------------------------------------------------------------
    # Factory Methods
    # --------------------------------------------------------------

    @classmethod
    def success_response(
        cls,
        query: str,
        facts: Optional[List[Dict[str, Any]]] = None,
        message: Optional[str] = None,
    ) -> "PortfolioAgentResponse":
        """
        Create a successful Portfolio Agent response.

        This factory is useful during the current implementation
        stage where deterministic analytical facts are available
        but LLM-based interpretation has not yet been introduced.
        """

        return cls(
            success=True,

            query=query,

            facts=facts or [],

            message=message
            or "Portfolio analytics retrieved successfully.",
        )

    @classmethod
    def error_response(
        cls,
        message: str,
        query: Optional[str] = None,
    ) -> "PortfolioAgentResponse":
        """
        Create a standardized error response.
        """

        return cls(
            success=False,

            query=query,

            message=message,
        )
