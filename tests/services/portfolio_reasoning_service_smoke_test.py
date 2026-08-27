"""
portfolio_reasoning_service_smoke_test.py

Smoke tests for PortfolioReasoningService.

Purpose
-------
Validate the reasoning boundary between:

    PortfolioAgent
        ↓
    PortfolioAnalyticsService
        ↓
    PortfolioReasoningService
        ↓
    PortfolioAgentResponse

The current implementation is intentionally LLM-independent.

The tests validate:
- Service initialization.
- Analytical context consumption.
- Structured response generation.
- Facts preservation.
- Risk, trend and opportunity context.
- Evidence generation.
- Empty input handling.
- Integration with PortfolioAgent.
"""

from pathlib import Path
import sys


# ------------------------------------------------------------------
# Repository Root
# ------------------------------------------------------------------

REPO_ROOT = str(
    Path(__file__).resolve().parents[2]
)

if REPO_ROOT not in sys.path:

    sys.path.insert(
        0,
        REPO_ROOT
    )


# ------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------

from src.agents.portfolio_agent import (
    PortfolioAgent,
)

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)

from src.services.portfolio_reasoning_service import (
    PortfolioReasoningService,
)


# ==============================================================
# Test Utility
# ==============================================================

def run_test(
    test_name: str,
    test_function,
) -> None:
    """
    Execute an individual smoke test and display the result.
    """

    try:

        test_function()

        print(
            f"{test_name:<55} [PASS]"
        )

    except AssertionError as exc:

        print(
            f"{test_name:<55} [FAIL]"
        )

        print(
            f"    Assertion: {exc}"
        )

        raise

    except Exception as exc:

        print(
            f"{test_name:<55} [FAIL]"
        )

        print(
            f"    Error: {exc}"
        )

        raise


# ==============================================================
# Service Tests
# ==============================================================

def test_reasoning_service_initialization():
    """
    Verify that PortfolioReasoningService can be initialized.
    """

    service = PortfolioReasoningService()

    assert service is not None


# ------------------------------------------------------------------

def test_analytical_service_initialization():
    """
    Verify that the analytical service required by the reasoning
    flow can be initialized successfully.
    """

    service = PortfolioAnalyticsService()

    assert service is not None


# ------------------------------------------------------------------

def test_analytical_context_available():
    """
    Verify that the Portfolio Analytics Service provides the
    complete analytical context expected by the reasoning layer.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    assert isinstance(
        context,
        dict
    )

    expected_domains = {
        "kpis",
        "risk",
        "exposure",
        "segmentation",
        "trends",
        "opportunities",
    }

    assert expected_domains.issubset(
        context.keys()
    )


# ------------------------------------------------------------------

def test_reasoning_service_processes_context():
    """
    Verify that PortfolioReasoningService can consume the complete
    analytical context and produce a response.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query="Provide an overview of the portfolio.",
        analytical_context=context,
    )

    assert isinstance(
        response,
        PortfolioAgentResponse
    )

    assert response.success is True


# ------------------------------------------------------------------

def test_facts_are_preserved():
    """
    Verify that analytical domains are preserved as structured
    facts by the reasoning service.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query="Analyse the portfolio.",
        analytical_context=context,
    )

    assert len(
        response.facts
    ) > 0

    fact_domains = {
        fact.get("domain")
        for fact in response.facts
    }

    expected_domains = {
        "kpis",
        "risk",
        "exposure",
        "segmentation",
        "trends",
        "opportunities",
    }

    assert expected_domains.issubset(
        fact_domains
    )


# ------------------------------------------------------------------

def test_risk_context_is_available():
    """
    Verify that risk analytics are transferred into the response.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query="Identify portfolio risks.",
        analytical_context=context,
    )

    assert len(
        response.risks
    ) > 0

    assert response.risks[0]["source"] == "risk"


# ------------------------------------------------------------------

def test_trend_context_is_available():
    """
    Verify that trend analytics are transferred into the response.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query="Identify important portfolio trends.",
        analytical_context=context,
    )

    assert len(
        response.trends
    ) > 0

    assert response.trends[0]["source"] == "trends"


# ------------------------------------------------------------------

def test_opportunity_context_is_available():
    """
    Verify that opportunity analytics are transferred into
    the response.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query="Identify portfolio opportunities.",
        analytical_context=context,
    )

    assert len(
        response.opportunities
    ) > 0

    assert (
        response.opportunities[0]["source"]
        == "opportunities"
    )


# ------------------------------------------------------------------

def test_observations_are_generated():
    """
    Verify that the current structural reasoning implementation
    generates observation context from available analytics.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query="What should I know about the portfolio?",
        analytical_context=context,
    )

    assert isinstance(
        response.observations,
        list
    )

    assert len(
        response.observations
    ) > 0


# ------------------------------------------------------------------

def test_evidence_is_generated():
    """
    Verify that evidence references are created for the
    analytical domains.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query="Provide supporting portfolio evidence.",
        analytical_context=context,
    )

    assert isinstance(
        response.evidence,
        list
    )

    assert len(
        response.evidence
    ) > 0

    evidence_domains = {
        item.get("domain")
        for item in response.evidence
    }

    expected_domains = {
        "kpis",
        "risk",
        "exposure",
        "segmentation",
        "trends",
        "opportunities",
    }

    assert expected_domains.issubset(
        evidence_domains
    )


# ------------------------------------------------------------------

def test_empty_query_handling():
    """
    Verify standardized handling of an empty query.
    """

    reasoning_service = (
        PortfolioReasoningService()
    )

    response = reasoning_service.reason(
        query="",
        analytical_context={
            "kpis": {}
        },
    )

    assert isinstance(
        response,
        PortfolioAgentResponse
    )

    assert response.success is False

    assert response.query == ""

    assert response.facts == []

    assert response.observations == []

    assert response.risks == []

    assert response.trends == []

    assert response.opportunities == []

    assert response.evidence == []


# ------------------------------------------------------------------

def test_empty_context_handling():
    """
    Verify standardized handling when no analytical context
    is available.
    """

    reasoning_service = (
        PortfolioReasoningService()
    )

    response = reasoning_service.reason(
        query="Analyse the portfolio.",
        analytical_context={},
    )

    assert isinstance(
        response,
        PortfolioAgentResponse
    )

    assert response.success is False

    assert response.query == (
        "Analyse the portfolio."
    )


# ==============================================================
# Portfolio Agent Integration
# ==============================================================

def test_portfolio_agent_uses_reasoning_service():
    """
    Verify that PortfolioAgent is correctly wired to
    PortfolioReasoningService.
    """

    agent = PortfolioAgent()

    assert agent.reasoning_service is not None

    assert isinstance(
        agent.reasoning_service,
        PortfolioReasoningService
    )


# ------------------------------------------------------------------

def test_portfolio_agent_returns_reasoned_response():
    """
    Verify the end-to-end integration:

        PortfolioAgent
            ↓
        PortfolioAnalyticsService
            ↓
        PortfolioReasoningService
            ↓
        PortfolioAgentResponse
    """

    agent = PortfolioAgent()

    response = agent.process(
        "Provide an overview of the portfolio."
    )

    assert isinstance(
        response,
        PortfolioAgentResponse
    )

    assert response.success is True

    assert len(
        response.facts
    ) > 0

    assert len(
        response.evidence
    ) > 0


# ------------------------------------------------------------------

def test_portfolio_agent_preserves_all_domains():
    """
    Verify that the complete analytical context remains available
    after passing through the Portfolio Agent and reasoning layer.
    """

    agent = PortfolioAgent()

    response = agent.process(
        "Analyse the complete portfolio."
    )

    fact_domains = {
        fact.get("domain")
        for fact in response.facts
    }

    expected_domains = {
        "kpis",
        "risk",
        "exposure",
        "segmentation",
        "trends",
        "opportunities",
    }

    assert expected_domains.issubset(
        fact_domains
    )


# ==============================================================
# Smoke Test Runner
# ==============================================================

def main():
    """
    Execute PortfolioReasoningService smoke tests.
    """

    print()

    print(
        "=" * 75
    )

    print(
        "Portfolio Reasoning Service : Smoke Test"
    )

    print(
        "=" * 75
    )

    run_test(
        "PortfolioReasoningService initialization",
        test_reasoning_service_initialization,
    )

    run_test(
        "PortfolioAnalyticsService initialization",
        test_analytical_service_initialization,
    )

    run_test(
        "Complete analytical context available",
        test_analytical_context_available,
    )

    run_test(
        "Reasoning service processes analytical context",
        test_reasoning_service_processes_context,
    )

    run_test(
        "Analytical facts are preserved",
        test_facts_are_preserved,
    )

    run_test(
        "Risk context available",
        test_risk_context_is_available,
    )

    run_test(
        "Trend context available",
        test_trend_context_is_available,
    )

    run_test(
        "Opportunity context available",
        test_opportunity_context_is_available,
    )

    run_test(
        "Observation context generated",
        test_observations_are_generated,
    )

    run_test(
        "Evidence references generated",
        test_evidence_is_generated,
    )

    run_test(
        "Empty query handling",
        test_empty_query_handling,
    )

    run_test(
        "Empty analytical context handling",
        test_empty_context_handling,
    )

    run_test(
        "PortfolioAgent uses reasoning service",
        test_portfolio_agent_uses_reasoning_service,
    )

    run_test(
        "PortfolioAgent returns reasoned response",
        test_portfolio_agent_returns_reasoned_response,
    )

    run_test(
        "PortfolioAgent preserves all analytical domains",
        test_portfolio_agent_preserves_all_domains,
    )

    print()

    print(
        "=" * 75
    )

    print(
        "Portfolio Reasoning Service : PASSED"
    )

    print(
        "=" * 75
    )


# ==============================================================
# Local Execution
# ==============================================================

if __name__ == "__main__":

    main()