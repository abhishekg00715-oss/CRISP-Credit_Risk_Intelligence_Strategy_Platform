"""
portfolio_agent_smoke_test.py

Smoke tests for PortfolioAgent.

Purpose
-------
Validate the integration between:

    PortfolioAgent
        ↓
    PortfolioAnalyticsService
        ↓
    Portfolio Analytical Services

The tests focus on the Portfolio Agent contract and the
complete analytical-context retrieval pattern.

These are smoke tests rather than exhaustive unit tests.
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


# ------------------------------------------------------------------
# Test Utility
# ------------------------------------------------------------------

def run_test(
    test_name: str,
    test_function,
) -> None:
    """
    Execute an individual smoke test and print its result.
    """

    try:

        test_function()

        print(
            f"{test_name:<50} [PASS]"
        )

    except AssertionError as exc:

        print(
            f"{test_name:<50} [FAIL]"
        )

        print(
            f"    Assertion: {exc}"
        )

        raise

    except Exception as exc:

        print(
            f"{test_name:<50} [FAIL]"
        )

        print(
            f"    Error: {exc}"
        )

        raise


# ==============================================================
# Tests
# ==============================================================

def test_agent_initialization():
    """
    Verify that PortfolioAgent can be initialized successfully.
    """

    agent = PortfolioAgent()

    assert agent is not None

    assert agent.analytics_service is not None


# ------------------------------------------------------------------

def test_analytical_context_retrieval():
    """
    Verify that PortfolioAgent can retrieve the complete
    analytical context through PortfolioAnalyticsService.
    """

    agent = PortfolioAgent()

    context = (
        agent.get_analytical_context()
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

def test_all_analytical_domains_available():
    """
    Verify that all six portfolio analytical domains are
    available to PortfolioAgent.
    """

    agent = PortfolioAgent()

    context = (
        agent.get_analytical_context()
    )

    expected_domains = [
        "kpis",
        "risk",
        "exposure",
        "segmentation",
        "trends",
        "opportunities",
    ]

    for domain in expected_domains:

        assert domain in context

        assert context[domain] is not None


# ------------------------------------------------------------------

def test_agent_response_contract():
    """
    Verify that PortfolioAgent returns the agreed response model.
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

    assert response.query == (
        "Provide an overview of the portfolio."
    )


# ------------------------------------------------------------------

def test_response_contains_facts():
    """
    Verify that the response contains analytical facts derived
    from the complete analytical context.
    """

    agent = PortfolioAgent()

    response = agent.process(
        "What is the current portfolio position?"
    )

    assert response.success is True

    assert isinstance(
        response.facts,
        list
    )

    assert len(
        response.facts
    ) > 0


# ------------------------------------------------------------------

def test_fact_domain_traceability():
    """
    Verify that analytical facts retain their originating
    analytical domain.
    """

    agent = PortfolioAgent()

    response = agent.process(
        "Analyse the portfolio."
    )

    domains = {
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
        domains
    )


# ------------------------------------------------------------------

def test_future_response_sections_exist():
    """
    Verify that the PortfolioAgentResponse exposes the agreed
    sections for future reasoning and narrative generation.

    The current implementation is not expected to populate all
    sections yet.
    """

    agent = PortfolioAgent()

    response = agent.process(
        "Identify important portfolio findings."
    )

    assert hasattr(
        response,
        "facts"
    )

    assert hasattr(
        response,
        "observations"
    )

    assert hasattr(
        response,
        "risks"
    )

    assert hasattr(
        response,
        "trends"
    )

    assert hasattr(
        response,
        "opportunities"
    )

    assert hasattr(
        response,
        "evidence"
    )


# ------------------------------------------------------------------

def test_future_response_sections_initially_empty():
    """
    Verify that interpretation-oriented sections are not
    artificially populated before the reasoning layer exists.
    """

    agent = PortfolioAgent()

    response = agent.process(
        "What are the key portfolio risks?"
    )

    assert response.observations == []

    assert response.risks == []

    assert response.trends == []

    assert response.opportunities == []

    assert response.evidence == []


# ------------------------------------------------------------------

def test_empty_query_handling():
    """
    Verify standardized handling of an empty query.
    """

    agent = PortfolioAgent()

    response = agent.process(
        ""
    )

    assert isinstance(
        response,
        PortfolioAgentResponse
    )

    assert response.success is False

    assert response.query == ""

    assert response.analytical_context if hasattr(
        response,
        "analytical_context"
    ) else True


# ------------------------------------------------------------------

def test_response_serialization():
    """
    Verify that PortfolioAgentResponse can be converted into
    a serializable dictionary.
    """

    agent = PortfolioAgent()

    response = agent.process(
        "Provide portfolio analytics."
    )

    response_dict = (
        response.to_dict()
    )

    assert isinstance(
        response_dict,
        dict
    )

    expected_fields = {
        "success",
        "query",
        "facts",
        "observations",
        "risks",
        "trends",
        "opportunities",
        "evidence",
        "message",
    }

    assert expected_fields.issubset(
        response_dict.keys()
    )


# ==============================================================
# Smoke Test Runner
# ==============================================================

def main():
    """
    Execute PortfolioAgent smoke tests.
    """

    print()

    print(
        "=" * 70
    )

    print(
        "Portfolio Agent : Smoke Test"
    )

    print(
        "=" * 70
    )

    run_test(
        "PortfolioAgent initialization",
        test_agent_initialization,
    )

    run_test(
        "Analytical context retrieval",
        test_analytical_context_retrieval,
    )

    run_test(
        "All analytical domains available",
        test_all_analytical_domains_available,
    )

    run_test(
        "PortfolioAgent response contract",
        test_agent_response_contract,
    )

    run_test(
        "Response contains analytical facts",
        test_response_contains_facts,
    )

    run_test(
        "Fact domain traceability",
        test_fact_domain_traceability,
    )

    run_test(
        "Future response sections available",
        test_future_response_sections_exist,
    )

    run_test(
        "Future response sections initially empty",
        test_future_response_sections_initially_empty,
    )

    run_test(
        "Empty query handling",
        test_empty_query_handling,
    )

    run_test(
        "Response serialization",
        test_response_serialization,
    )

    print()

    print(
        "=" * 70
    )

    print(
        "Portfolio Agent : PASSED"
    )

    print(
        "=" * 70
    )


# ------------------------------------------------------------------
# Local Execution
# ------------------------------------------------------------------

if __name__ == "__main__":

    main()
