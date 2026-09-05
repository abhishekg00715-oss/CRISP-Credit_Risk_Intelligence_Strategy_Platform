"""
portfolio_intelligence_integration_test.py

Functional Integration Test for Portfolio Intelligence.

Purpose
-------
Validate the end-to-end Portfolio Intelligence capability through
the production orchestration path:

    User Query
        ↓
    CoordinatorAgent
        ↓
    IntentRoutingService
        ↓
    PortfolioAgent
        ↓
    PortfolioAnalyticsService
        ↓
    PortfolioReasoningService
        ↓
    LLMService
        ↓
    PortfolioAgentResponse

The test focuses on functional behaviour rather than individual
component implementation details.

Detailed component behaviour is covered by the existing smoke tests.

This test intentionally does not assert exact LLM wording because
LLM responses are non-deterministic.

Required environment
--------------------
OPENAI_API_KEY
OPENAI_MODEL
"""

from typing import Any, Callable, Dict

from src.agents.coordinator_agent import (
    CoordinatorAgent,
)

from src.initialization.application_startup import (
    ApplicationStartup,
)


# ------------------------------------------------------------------
# Test Utilities
# ------------------------------------------------------------------

def run_test(
    test_name: str,
    test_function: Callable[[], None],
) -> None:
    """
    Execute an individual functional integration test.
    """

    try:

        test_function()

        print(
            f"{test_name:<65} [PASS]"
        )

    except AssertionError as exc:

        print(
            f"{test_name:<65} [FAIL]"
        )

        if str(exc):
            print(
                f"    Assertion: {exc}"
            )

        raise

    except Exception as exc:

        print(
            f"{test_name:<65} [FAIL]"
        )

        print(
            f"    Error: "
            f"{type(exc).__name__}: {exc}"
        )

        raise


# ------------------------------------------------------------------
# Coordinator Factory
# ------------------------------------------------------------------

def create_coordinator() -> CoordinatorAgent:
    """
    Create the Coordinator through the existing application
    startup lifecycle.

    ApplicationStartup.initialize() returns the startup instance.
    The CoordinatorAgent is exposed through startup.coordinator.
    """

    startup = (
        ApplicationStartup()
        .initialize()
    )

    return startup.coordinator


# ------------------------------------------------------------------
# Response Validation
# ------------------------------------------------------------------

def validate_portfolio_response(
    response: Dict[str, Any],
) -> None:
    """
    Validate the standard Coordinator response contract and
    confirm that Portfolio Agent was invoked successfully.
    """

    assert isinstance(
        response,
        dict,
    )

    assert (
        response.get("success") is True
    ), (
        "Coordinator returned an unsuccessful response."
    )

    assert (
        "agents_invoked"
        in response
    )

    assert (
        "responses"
        in response
    )

    assert (
        "portfolio"
        in response["agents_invoked"]
    )

    assert (
        "portfolio"
        in response["responses"]
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert portfolio_response is not None


# ------------------------------------------------------------------
# Test 1
# ------------------------------------------------------------------

def test_portfolio_overview() -> None:
    """
    Validate a general portfolio overview request.

    Expected behaviour:
    - Portfolio intent is selected.
    - Portfolio Agent is invoked.
    - A successful structured response is returned.
    """

    coordinator = create_coordinator()

    query = (
        "Provide an overview of the current portfolio "
        "position, including its key risks, trends and "
        "opportunities."
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert (
        len(
            portfolio_response.facts
        )
        + len(
            portfolio_response.observations
        )
        + len(
            portfolio_response.risks
        )
        + len(
            portfolio_response.trends
        )
        + len(
            portfolio_response.opportunities
        )
        > 0
    )


# ------------------------------------------------------------------
# Test 2
# ------------------------------------------------------------------

def test_portfolio_kpi_request() -> None:
    """
    Validate a portfolio KPI-oriented request.
    """

    coordinator = create_coordinator()

    query = (
        "What is the overall health and current position "
        "of the portfolio?"
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert (
        len(portfolio_response.facts)
        + len(portfolio_response.observations)
        > 0
    )


# ------------------------------------------------------------------
# Test 3
# ------------------------------------------------------------------

def test_portfolio_risk_request() -> None:
    """
    Validate a risk-focused portfolio request.
    """

    coordinator = create_coordinator()

    query = (
        "What are the most significant credit risks "
        "in the portfolio?"
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert (
        len(portfolio_response.risks)
        > 0
    )


# ------------------------------------------------------------------
# Test 4
# ------------------------------------------------------------------

def test_portfolio_exposure_request() -> None:
    """
    Validate an exposure-focused portfolio request.
    """

    coordinator = create_coordinator()

    query = (
        "Where is the portfolio exposure concentrated "
        "across products and geography?"
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert (
        len(portfolio_response.observations)
        + len(portfolio_response.risks)
        > 0
    )


# ------------------------------------------------------------------
# Test 5
# ------------------------------------------------------------------

def test_portfolio_segmentation_request() -> None:
    """
    Validate a customer-segmentation portfolio request.
    """

    coordinator = create_coordinator()

    query = (
        "How is the portfolio distributed across "
        "customer segments?"
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert (
        len(portfolio_response.observations)
        + len(portfolio_response.facts)
        > 0
    )


# ------------------------------------------------------------------
# Test 6
# ------------------------------------------------------------------

def test_portfolio_trend_request() -> None:
    """
    Validate a portfolio trend request.
    """

    coordinator = create_coordinator()

    query = (
        "What are the most important trends "
        "in the portfolio?"
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert (
        len(portfolio_response.trends)
        > 0
    )


# ------------------------------------------------------------------
# Test 7
# ------------------------------------------------------------------

def test_portfolio_opportunity_request() -> None:
    """
    Validate a portfolio opportunity request.
    """

    coordinator = create_coordinator()

    query = (
        "What are the most significant opportunities "
        "identified in the portfolio?"
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert (
        len(portfolio_response.opportunities)
        > 0
    )


# ------------------------------------------------------------------
# Test 8
# ------------------------------------------------------------------

def test_portfolio_cross_domain_request() -> None:
    """
    Validate a request requiring multiple analytical domains.

    This is an important test for the agreed design in which the
    complete analytical context is supplied to the reasoning layer
    rather than selectively invoking individual services.
    """

    coordinator = create_coordinator()

    query = (
        "Assess the overall portfolio health and explain "
        "how risk, exposure, recent trends and business "
        "opportunities relate to each other."
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    total_content = (
        len(portfolio_response.facts)
        + len(portfolio_response.observations)
        + len(portfolio_response.risks)
        + len(portfolio_response.trends)
        + len(portfolio_response.opportunities)
    )

    assert (
        total_content > 0
    )


# ------------------------------------------------------------------
# Test 9
# ------------------------------------------------------------------

def test_portfolio_response_evidence() -> None:
    """
    Validate that the Portfolio Agent returns evidence information
    when available.

    Evidence is checked as a collection rather than against exact
    wording or exact source values.
    """

    coordinator = create_coordinator()

    query = (
        "Summarize the portfolio position and provide "
        "supporting evidence for the key findings."
    )

    response = coordinator.process_query(
        query
    )

    validate_portfolio_response(
        response
    )

    portfolio_response = (
        response["responses"]["portfolio"]
    )

    assert (
        portfolio_response.success is True
    )

    assert isinstance(
        portfolio_response.evidence,
        list,
    )


# ------------------------------------------------------------------
# Test 10
# ------------------------------------------------------------------

def test_invalid_portfolio_query() -> None:
    """
    Validate graceful handling of an empty query.

    This test does not invoke the LLM.
    """

    coordinator = create_coordinator()

    response = coordinator.process_query(
        ""
    )

    assert isinstance(
        response,
        dict,
    )

    assert (
        response.get("success") is False
    )

    assert (
        response.get("message")
        == "Please provide a valid query."
    )


# ------------------------------------------------------------------
# Test 11
# ------------------------------------------------------------------

def test_existing_policy_routing_regression() -> None:
    """
    Verify that Portfolio integration has not disrupted
    existing Policy routing.
    """

    coordinator = create_coordinator()

    query = (
        "What is the minimum credit score required "
        "for a premium credit card?"
    )

    response = coordinator.process_query(
        query
    )

    assert isinstance(
        response,
        dict,
    )

    assert (
        response.get("success") is True
    )

    assert (
        "policy"
        in response.get(
            "agents_invoked",
            [],
        )
    )


# ------------------------------------------------------------------
# Test 12
# ------------------------------------------------------------------

def test_existing_customer_routing_regression() -> None:
    """
    Verify that Portfolio integration has not disrupted
    existing Customer routing.
    """

    coordinator = create_coordinator()

    query = (
        "Show me the risk assessment for "
        "customer CUST001."
    )

    response = coordinator.process_query(
        query
    )

    assert isinstance(
        response,
        dict,
    )

    assert (
        response.get("success") is True
    )

    assert (
        "customer"
        in response.get(
            "agents_invoked",
            [],
        )
    )


# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

def main() -> None:
    """
    Execute the Portfolio Intelligence functional integration
    test suite.
    """

    print()
    print("=" * 80)
    print("Portfolio Intelligence : Functional Integration Test")
    print("=" * 80)

    print(
        "NOTE: Portfolio functional tests require "
        "OPENAI_API_KEY and OPENAI_MODEL."
    )

    print()

    run_test(
        "Portfolio overview request",
        test_portfolio_overview,
    )

    run_test(
        "Portfolio KPI request",
        test_portfolio_kpi_request,
    )

    run_test(
        "Portfolio risk request",
        test_portfolio_risk_request,
    )

    run_test(
        "Portfolio exposure request",
        test_portfolio_exposure_request,
    )

    run_test(
        "Portfolio segmentation request",
        test_portfolio_segmentation_request,
    )

    run_test(
        "Portfolio trend request",
        test_portfolio_trend_request,
    )

    run_test(
        "Portfolio opportunity request",
        test_portfolio_opportunity_request,
    )

    run_test(
        "Portfolio cross-domain request",
        test_portfolio_cross_domain_request,
    )

    run_test(
        "Portfolio response evidence",
        test_portfolio_response_evidence,
    )

    run_test(
        "Invalid portfolio query handling",
        test_invalid_portfolio_query,
    )

    run_test(
        "Policy routing regression",
        test_existing_policy_routing_regression,
    )

    run_test(
        "Customer routing regression",
        test_existing_customer_routing_regression,
    )

    print()
    print("=" * 80)
    print("Portfolio Intelligence : Functional Integration Test PASSED")
    print("=" * 80)


if __name__ == "__main__":
    main()
