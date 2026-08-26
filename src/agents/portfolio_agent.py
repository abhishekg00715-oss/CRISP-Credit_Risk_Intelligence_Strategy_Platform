"""
portfolio_agent.py

Portfolio Agent responsible for orchestrating Portfolio Intelligence
requests.

Responsibilities
----------------
- Accept portfolio-related analytical questions.
- Select the appropriate portfolio analytical capability.
- Invoke PortfolioAnalyticsService.
- Construct a structured analytical response.
- Preserve analytical facts as evidence for downstream narrative
  generation.

Design Principles
-----------------
- No direct database access.
- No direct repository access.
- No portfolio business calculations.
- Business calculations remain within specialised analytics services.
- PortfolioAnalyticsService remains the single analytical entry point.
- Response construction remains deterministic and structured.

The agent can later be extended with an LLM-based interpretation and
narrative layer without changing the underlying analytical services.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)


# ------------------------------------------------------------------
# Request / Response Models
# ------------------------------------------------------------------

@dataclass
class PortfolioAgentRequest:
    """
    Represents a request received by the Portfolio Agent.
    """

    query: str


@dataclass
class PortfolioAgentResponse:
    """
    Represents the structured response returned by the Portfolio Agent.
    """

    query: str
    analysis_type: str
    analytical_data: Any
    key_findings: list[str]
    insights: list[str]
    status: str = "success"
    error: Optional[str] = None


# ------------------------------------------------------------------
# Portfolio Agent
# ------------------------------------------------------------------

class PortfolioAgent:
    """
    Agent responsible for Portfolio Intelligence orchestration.

    The agent determines which analytical capability is relevant
    to the user's request and delegates the actual analysis to
    PortfolioAnalyticsService.
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

        self.capability_map = self._build_capability_map()

    # --------------------------------------------------------------
    # Capability Catalogue
    # --------------------------------------------------------------

    def _build_capability_map(self) -> Dict[str, str]:
        """
        Define the portfolio analytical capabilities supported
        by the agent.

        The mapping provides a controlled vocabulary between the
        user's business question and PortfolioAnalyticsService.
        """

        return {

            "overview": "get_portfolio_overview",

            "kpi": "get_kpis",

            "risk": "get_risk_analysis",

            "risk_distribution": (
                "get_risk_distribution"
            ),

            "risk_exposure": (
                "get_risk_exposure_distribution"
            ),

            "exposure": (
                "get_exposure_analysis"
            ),

            "product_exposure": (
                "get_product_exposure"
            ),

            "geographic_exposure": (
                "get_geographic_exposure"
            ),

            "exposure_concentration": (
                "get_exposure_concentration"
            ),

            "segmentation": (
                "get_segmentation_analysis"
            ),

            "segment_distribution": (
                "get_segment_distribution"
            ),

            "trend": (
                "get_trend_analysis"
            ),

            "opportunity": (
                "get_opportunity_analysis"
            ),
        }

    # --------------------------------------------------------------
    # Public Agent Interface
    # --------------------------------------------------------------

    def analyze(
        self,
        request: PortfolioAgentRequest,
    ) -> PortfolioAgentResponse:
        """
        Execute a portfolio intelligence request.
        """

        try:

            capability = self._select_capability(
                request.query
            )

            analytical_data = (
                self._execute_capability(
                    capability
                )
            )

            return self._build_response(
                query=request.query,
                analysis_type=capability,
                analytical_data=analytical_data,
            )

        except Exception as exc:

            return PortfolioAgentResponse(
                query=request.query,
                analysis_type="unknown",
                analytical_data={},
                key_findings=[],
                insights=[],
                status="error",
                error=str(exc),
            )

    # --------------------------------------------------------------
    # Capability Selection
    # --------------------------------------------------------------

    def _select_capability(
        self,
        query: str,
    ) -> str:
        """
        Select the analytical capability required for the query.

        This is intentionally a lightweight initial implementation.

        The Coordinator has already established that the request
        belongs to the Portfolio domain. This method therefore
        determines the required analytical operation within that
        domain.

        A more sophisticated semantic capability classifier can
        replace this implementation later without changing the
        agent contract.
        """

        normalized_query = query.lower()

        # ----------------------------------------------------------
        # Opportunity
        # ----------------------------------------------------------

        if any(
            keyword in normalized_query
            for keyword in (
                "opportunity",
                "opportunities",
                "growth",
                "cross sell",
                "cross-sell",
                "upsell",
                "eligible",
            )
        ):

            return "opportunity"

        # ----------------------------------------------------------
        # Trend
        # ----------------------------------------------------------

        if any(
            keyword in normalized_query
            for keyword in (
                "trend",
                "trends",
                "improving",
                "deteriorating",
                "movement",
                "change over time",
                "direction",
            )
        ):

            return "trend"

        # ----------------------------------------------------------
        # Risk
        # ----------------------------------------------------------

        if any(
            keyword in normalized_query
            for keyword in (
                "risk",
                "risky",
                "risk profile",
                "risk distribution",
                "risk band",
                "default",
                "delinquency",
            )
        ):

            return "risk"

        # ----------------------------------------------------------
        # Exposure
        # ----------------------------------------------------------

        if any(
            keyword in normalized_query
            for keyword in (
                "exposure",
                "concentration",
                "concentrated",
            )
        ):

            if any(
                keyword in normalized_query
                for keyword in (
                    "product",
                    "card",
                    "loan",
                )
            ):

                return "product_exposure"

            if any(
                keyword in normalized_query
                for keyword in (
                    "state",
                    "geographic",
                    "geography",
                    "location",
                )
            ):

                return "geographic_exposure"

            if any(
                keyword in normalized_query
                for keyword in (
                    "concentration",
                    "concentrated",
                )
            ):

                return "exposure_concentration"

            return "exposure"

        # ----------------------------------------------------------
        # Segmentation
        # ----------------------------------------------------------

        if any(
            keyword in normalized_query
            for keyword in (
                "segment",
                "segmentation",
                "customer segment",
                "customer profile",
            )
        ):

            return "segmentation"

        # ----------------------------------------------------------
        # KPI / Metrics
        # ----------------------------------------------------------

        if any(
            keyword in normalized_query
            for keyword in (
                "kpi",
                "kpis",
                "metric",
                "metrics",
                "health",
                "portfolio health",
                "credit score",
                "utilisation",
                "utilization",
            )
        ):

            return "kpi"

        # ----------------------------------------------------------
        # Default
        # ----------------------------------------------------------

        return "overview"

    # --------------------------------------------------------------
    # Execute Capability
    # --------------------------------------------------------------

    def _execute_capability(
        self,
        capability: str,
    ) -> Any:
        """
        Invoke the selected PortfolioAnalyticsService capability.
        """

        method_name = self.capability_map.get(
            capability
        )

        if method_name is None:

            raise ValueError(
                f"Unsupported portfolio capability: "
                f"{capability}"
            )

        method = getattr(
            self.analytics_service,
            method_name,
        )

        return method()

    # --------------------------------------------------------------
    # Response Construction
    # --------------------------------------------------------------

    def _build_response(
        self,
        query: str,
        analysis_type: str,
        analytical_data: Any,
    ) -> PortfolioAgentResponse:
        """
        Construct a structured response from analytical results.

        The response deliberately preserves the underlying
        analytical data rather than converting it immediately
        into natural language.
        """

        key_findings = (
            self._extract_key_findings(
                analysis_type,
                analytical_data,
            )
        )

        insights = (
            self._derive_basic_insights(
                analysis_type,
                analytical_data,
            )
        )

        return PortfolioAgentResponse(
            query=query,
            analysis_type=analysis_type,
            analytical_data=analytical_data,
            key_findings=key_findings,
            insights=insights,
        )

    # --------------------------------------------------------------
    # Key Findings
    # --------------------------------------------------------------

    @staticmethod
    def _extract_key_findings(
        analysis_type: str,
        analytical_data: Any,
    ) -> list[str]:
        """
        Extract lightweight factual findings from the analytical
        response.

        This method intentionally avoids complex business
        calculations.
        """

        findings = []

        if isinstance(analytical_data, dict):

            findings.append(
                f"{analysis_type} analysis successfully "
                f"retrieved."
            )

        elif isinstance(analytical_data, list):

            findings.append(
                f"{analysis_type} analysis returned "
                f"{len(analytical_data)} analytical records."
            )

        return findings

    # --------------------------------------------------------------
    # Basic Insights
    # --------------------------------------------------------------

    @staticmethod
    def _derive_basic_insights(
        analysis_type: str,
        analytical_data: Any,
    ) -> list[str]:
        """
        Provide basic deterministic observations.

        This is intentionally lightweight. Rich business
        interpretation and narrative generation can later be
        delegated to the LLM layer.
        """

        insights = []

        if analysis_type == "overview":

            insights.append(
                "Portfolio overview combines KPI, risk, "
                "exposure, segmentation, trend and "
                "opportunity information."
            )

        elif analysis_type == "risk":

            insights.append(
                "Risk analytics provide the portfolio "
                "risk distribution and related exposure."
            )

        elif analysis_type == "exposure":

            insights.append(
                "Exposure analytics provide a view of "
                "portfolio exposure and concentration."
            )

        elif analysis_type == "segmentation":

            insights.append(
                "Segmentation analytics provide customer "
                "distribution across portfolio segments."
            )

        elif analysis_type == "trend":

            insights.append(
                "Trend analytics provide indicators of "
                "portfolio movement over time."
            )

        elif analysis_type == "opportunity":

            insights.append(
                "Opportunity analytics identify portfolio "
                "opportunities and associated eligibility "
                "and value indicators."
            )

        return insights
