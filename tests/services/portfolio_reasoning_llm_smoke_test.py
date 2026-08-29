"""
portfolio_reasoning_llm_smoke_test.py

Smoke test for the OpenAI-backed Portfolio Reasoning flow.

Purpose
-------
Validate the live LLM integration:

    PortfolioAgent
          ↓
    PortfolioAnalyticsService
          ↓
    Complete Analytical Context
          ↓
    PortfolioReasoningService
          ↓
    PortfolioReasoningPromptBuilder
          ↓
    LLMService
          ↓
    OpenAI API
          ↓
    PortfolioAgentResponse

This test is intentionally separate from
portfolio_reasoning_service_smoke_test.py.

The standard reasoning smoke test validates service structure
and contracts without requiring an external LLM call.

This test validates the actual OpenAI integration and therefore
requires:

    OPENAI_API_KEY

and a valid:

    OPENAI_MODEL

in the repository .env file.
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

from src.services.llm_service import (
    LLMService,
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
            f"{test_name:<60} [PASS]"
        )

    except AssertionError as exc:

        print(
            f"{test_name:<60} [FAIL]"
        )

        print(
            f"    Assertion: {exc}"
        )

        raise

    except Exception as exc:

        print(
            f"{test_name:<60} [FAIL]"
        )

        print(
            f"    Error: {exc}"
        )

        raise


# ==============================================================
# LLM Service Tests
# ==============================================================

def test_llm_service_initialization():
    """
    Verify that the existing LLMService can be initialized.

    LLMService is the common OpenAI API wrapper already used
    elsewhere in CRISP.
    """

    service = LLMService()

    assert service is not None

    assert service.client is not None


# ------------------------------------------------------------------

def test_llm_service_direct_response():
    """
    Verify that the existing LLMService can successfully
    communicate with the configured OpenAI API.

    This is intentionally a minimal request so that the smoke
    test validates connectivity without testing portfolio
    reasoning itself.
    """

    service = LLMService()

    response = service.generate_response(
        prompt=(
            "Respond with exactly one short sentence "
            "confirming that the LLM integration is working."
        )
    )

    assert response is not None

    assert isinstance(
        response,
        str
    )

    assert response.strip() != ""


# ==============================================================
# Portfolio Reasoning Tests
# ==============================================================

def test_portfolio_analytics_context_available():
    """
    Verify that the Portfolio Analytics Service can provide
    the complete analytical context required by the reasoning
    service.
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

def test_portfolio_reasoning_llm_response():
    """
    Verify that PortfolioReasoningService can invoke the
    configured OpenAI API and produce a non-empty response.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService(
            llm_service=LLMService()
        )
    )

    analytical_context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query=(
            "Provide a concise overview of the "
            "current portfolio position, highlighting "
            "important observations, risks, trends "
            "and opportunities."
        ),
        analytical_context=analytical_context,
    )

    assert isinstance(
        response,
        PortfolioAgentResponse
    )

    assert response.success is True

    assert response.observations

    assert isinstance(
        response.observations,
        list
    )


# ------------------------------------------------------------------

def test_llm_generated_observation_is_non_empty():
    """
    Verify that the LLM-generated reasoning content is
    successfully captured in the response.

    No exact wording is asserted because LLM responses
    are inherently variable.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService(
            llm_service=LLMService()
        )
    )

    analytical_context = (
        analytics_service
        .get_full_analytical_context()
    )

    response = reasoning_service.reason(
        query=(
            "Identify the most important portfolio "
            "observations."
        ),
        analytical_context=analytical_context,
    )

    assert response.success is True

    assert len(
        response.observations
    ) > 0

    llm_observation = (
        response.observations[0]
    )

    assert isinstance(
        llm_observation,
        dict
    )

    assert (
        llm_observation.get("content")
    )

    assert (
        llm_observation["content"].strip()
        != ""
    )


# ==============================================================
# Portfolio Agent End-to-End Test
# ==============================================================

def test_portfolio_agent_llm_integration():
    """
    Verify the complete Portfolio Agent → Analytics →
    Reasoning → OpenAI API → Response flow.
    """

    reasoning_service = (
        PortfolioReasoningService(
            llm_service=LLMService()
        )
    )

    agent = PortfolioAgent(
        reasoning_service=reasoning_service
    )

    response = agent.process(
        (
            "Provide a concise portfolio intelligence "
            "summary covering key observations, risks, "
            "trends and opportunities."
        )
    )

    assert isinstance(
        response,
        PortfolioAgentResponse
    )

    assert response.success is True

    assert response.query is not None

    assert response.facts

    assert response.observations

    assert response.evidence


# ------------------------------------------------------------------

def test_portfolio_agent_llm_response_content():
    """
    Verify that the final PortfolioAgent response contains
    non-empty LLM-generated reasoning content.
    """

    reasoning_service = (
        PortfolioReasoningService(
            llm_service=LLMService()
        )
    )

    agent = PortfolioAgent(
        reasoning_service=reasoning_service
    )

    response = agent.process(
        "What are the most important things to know about the portfolio?"
    )

    assert response.success is True

    assert len(
        response.observations
    ) > 0

    observation = (
        response.observations[0]
    )

    assert observation.get(
        "content"
    )

    assert observation[
        "content"
    ].strip() != ""


# ==============================================================
# Smoke Test Runner
# ==============================================================

def main():
    """
    Execute the OpenAI-backed Portfolio Reasoning smoke tests.
    """

    print()

    print(
        "=" * 75
    )

    print(
        "Portfolio Reasoning LLM : Smoke Test"
    )

    print(
        "=" * 75
    )

    print(
        "NOTE: This test requires a valid OPENAI_API_KEY "
        "and OPENAI_MODEL configuration."
    )

    print()

    run_test(
        "LLMService initialization",
        test_llm_service_initialization,
    )

    run_test(
        "Direct OpenAI API response",
        test_llm_service_direct_response,
    )

    run_test(
        "Complete analytical context available",
        test_portfolio_analytics_context_available,
    )

    run_test(
        "Portfolio reasoning LLM response",
        test_portfolio_reasoning_llm_response,
    )

    run_test(
        "LLM-generated observation is non-empty",
        test_llm_generated_observation_is_non_empty,
    )

    run_test(
        "Portfolio Agent LLM integration",
        test_portfolio_agent_llm_integration,
    )

    run_test(
        "Portfolio Agent LLM response content",
        test_portfolio_agent_llm_response_content,
    )

    print()

    print(
        "=" * 75
    )

    print(
        "Portfolio Reasoning LLM : PASSED"
    )

    print(
        "=" * 75
    )


# ==============================================================
# Local Execution
# ==============================================================

if __name__ == "__main__":

    main()
