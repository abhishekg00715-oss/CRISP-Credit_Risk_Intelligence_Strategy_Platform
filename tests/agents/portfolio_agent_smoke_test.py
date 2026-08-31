"""
portfolio_agent_smoke_test.py

Smoke test for PortfolioAgent integration.

Purpose
-------
Validates the integration between:

    PortfolioAgent
        ↓
    PortfolioAnalyticsService
        ↓
    PortfolioReasoningService
        ↓
    LLMService
        ↓
    OpenAI API
        ↓
    PortfolioAgentResponse

The test intentionally validates orchestration and integration
rather than detailed analytical calculations. Those calculations
are already covered by the Portfolio Analytics Service tests.

NOTE
----
This test requires:

    OPENAI_API_KEY
    OPENAI_MODEL

to be configured in the runtime environment.
"""

from typing import Callable

from src.models.portfolio_agent_response import (
    PortfolioAgentResponse,
)

from src.services.llm_service import (
    LLMService,
)

from src.services.portfolio_agent import (
    PortfolioAgent,
)

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)

from src.services.portfolio_reasoning_service import (
    PortfolioReasoningService,
)


# ------------------------------------------------------------------
# Test Utilities
# ------------------------------------------------------------------

def run_test(
    test_name: str,
    test_function: Callable[[], None],
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

        if str(exc):
            print(f"    Assertion: {exc}")

        raise

    except Exception as exc:

        print(
            f"{test_name:<60} [FAIL]"
        )

        print(
            f"    Error: {type(exc).__name__}: {exc}"
        )

        raise


# ------------------------------------------------------------------
# Shared Test Objects
# ------------------------------------------------------------------

def create_portfolio_agent() -> PortfolioAgent:
    """
    Create a PortfolioAgent using the production dependency chain.

    Dependency injection is used explicitly so that the smoke test
    validates the same service composition used by the application.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    reasoning_service = (
        PortfolioReasoningService(
            llm_service=LLMService()
        )
    )

    return PortfolioAgent(
        analytics_service=analytics_service,
        reasoning_service=reasoning_service,
    )


# ------------------------------------------------------------------
# Test 1
# ------------------------------------------------------------------

def test_portfolio_agent_initialization() -> None:
    """
    Verify that PortfolioAgent and its primary dependencies
    initialize successfully.
    """

    agent = create_portfolio_agent()

    assert agent is not None

    assert isinstance(
        agent.analytics_service,
        PortfolioAnalyticsService,
    )

    assert isinstance(
        agent.reasoning_service,
        PortfolioReasoningService,
    )


# ------------------------------------------------------------------
# Test 2
# ------------------------------------------------------------------

def test_portfolio_analytical_context_available() -> None:
    """
    Verify that the Portfolio Analytics Service can provide the
    complete analytical context required by the reasoning layer.
    """

    analytics_service = (
        PortfolioAnalyticsService()
    )

    context = (
        analytics_service
        .get_full_analytical_context()
    )

    assert context is not None

    assert isinstance(
        context,
        dict,
    )

    assert len(context) > 0


# ------------------------------------------------------------------
# Test 3
# ------------------------------------------------------------------

def test_portfolio_agent_empty_query_handling() -> None:
    """
    Verify graceful handling of an empty portfolio query.

    This test does not require an LLM call.
    """

    agent = create_portfolio_agent()

    response = agent.process("")

    assert isinstance(
        response,
        PortfolioAgentResponse,
    )

    assert response.success is False

    assert response.query == ""

    assert response.message is not None


# ------------------------------------------------------------------
# Test 4
# ------------------------------------------------------------------

def test_portfolio_agent_llm_integration() -> None:
    """
    Validate the complete Portfolio Agent reasoning flow.

    This test invokes the real LLM through the existing LLMService.
    """

    agent = create_portfolio_agent()

    query = (
        "Provide a concise overview of the current "
        "portfolio position, highlighting important "
        "observations, risks, trends and opportunities."
    )

    response = agent.process(query)

    # --------------------------------------------------------------
    # Response contract
    # --------------------------------------------------------------

    assert isinstance(
        response,
        PortfolioAgentResponse,
    )

    assert response.success is True

    assert response.query == query

    # --------------------------------------------------------------
    # Structured reasoning output
    # --------------------------------------------------------------

    assert isinstance(
        response.facts,
        list,
    )

    assert isinstance(
        response.observations,
        list,
    )

    assert isinstance(
        response.risks,
        list,
    )

    assert isinstance(
        response.trends,
        list,
    )

    assert isinstance(
        response.opportunities,
        list,
    )

    assert isinstance(
        response.evidence,
        list,
    )


# ------------------------------------------------------------------
# Test 5
# ------------------------------------------------------------------

def test_portfolio_agent_generates_reasoning_content() -> None:
    """
    Verify that the LLM-backed Portfolio Agent produces at least
    some meaningful structured reasoning content.

    The test deliberately does not assert exact wording because
    LLM output is non-deterministic.
    """

    agent = create_portfolio_agent()

    query = (
        "Identify the most important portfolio risks and "
        "opportunities from the available analytical data."
    )

    response = agent.process(query)

    assert response.success is True

    content_sections = [
        response.facts,
        response.observations,
        response.risks,
        response.trends,
        response.opportunities,
        response.evidence,
    ]

    total_items = sum(
        len(section)
        for section in content_sections
    )

    assert total_items > 0


# ------------------------------------------------------------------
# Test 6
# ------------------------------------------------------------------

def test_portfolio_agent_complete_flow() -> None:
    """
    Validate the complete production-style Portfolio Intelligence
    flow through a single Agent invocation.

    This is the primary integration smoke test.
    """

    agent = create_portfolio_agent()

    query = (
        "Analyze the portfolio and summarize its overall health, "
        "key risks, important trends and potential opportunities."
    )

    response = agent.process(query)

    assert isinstance(
        response,
        PortfolioAgentResponse,
    )

    assert response.success is True

    assert response.query == query

    assert (
        len(response.facts)
        + len(response.observations)
        + len(response.risks)
        + len(response.trends)
        + len(response.opportunities)
    ) > 0


# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

def main() -> None:
    """
    Execute the Portfolio Agent smoke-test suite.
    """

    print()
    print("=" * 75)
    print("Portfolio Agent : Smoke Test")
    print("=" * 75)

    print(
        "NOTE: LLM integration tests require a valid "
        "OPENAI_API_KEY and OPENAI_MODEL configuration."
    )

    print()

    run_test(
        "PortfolioAgent initialization",
        test_portfolio_agent_initialization,
    )

    run_test(
        "Complete analytical context available",
        test_portfolio_analytical_context_available,
    )

    run_test(
        "Empty portfolio query handling",
        test_portfolio_agent_empty_query_handling,
    )

    run_test(
        "Portfolio Agent LLM integration",
        test_portfolio_agent_llm_integration,
    )

    run_test(
        "Portfolio Agent reasoning content",
        test_portfolio_agent_generates_reasoning_content,
    )

    run_test(
        "Portfolio Agent complete integration flow",
        test_portfolio_agent_complete_flow,
    )

    print()
    print("=" * 75)
    print("Portfolio Agent : Smoke Test Completed")
    print("=" * 75)


if __name__ == "__main__":
    main()
```
