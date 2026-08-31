"""
coordinator_agent_integration_smoke_test.py

Smoke test for CoordinatorAgent integration.

Purpose
-------
Validates the Coordinator integration with:

    IntentRoutingService
            ↓
    Specialist Agent Selection
            ↓
    PortfolioAgent
            ↓
    PortfolioAnalyticsService
            ↓
    PortfolioReasoningService
            ↓
    LLMService
            ↓
    OpenAI API

The test also performs basic regression checks for the existing
Policy and Customer Agent routing.

The smoke test validates orchestration and integration boundaries.
Detailed analytics and reasoning are tested independently by their
respective smoke-test components.

NOTE
----
Portfolio end-to-end tests require:

    OPENAI_API_KEY
    OPENAI_MODEL

to be configured in the runtime environment.
"""

from typing import Callable

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
            print(
                f"    Assertion: {exc}"
            )

        raise

    except Exception as exc:

        print(
            f"{test_name:<60} [FAIL]"
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
    Create CoordinatorAgent using the application startup
    configuration.

    This intentionally uses the production initialization path
    rather than manually constructing the routing service.
    """

    startup = ApplicationStartup()

    return startup.initialize()


# ------------------------------------------------------------------
# Test 1
# ------------------------------------------------------------------

def test_coordinator_initialization() -> None:
    """
    Verify that CoordinatorAgent initializes successfully and
    contains the expected specialist agents.
    """

    coordinator = create_coordinator()

    assert coordinator is not None

    assert isinstance(
        coordinator,
        CoordinatorAgent,
    )

    assert coordinator.routing_service is not None

    assert coordinator.response_formatter is not None

    assert coordinator.query_logger is not None

    assert coordinator.execution_logger is not None

    assert "policy" in coordinator._agents

    assert "customer" in coordinator._agents

    assert "portfolio" in coordinator._agents


# ------------------------------------------------------------------
# Test 2
# ------------------------------------------------------------------

def test_portfolio_agent_registration() -> None:
    """
    Verify the Portfolio Agent is registered using the generic
    Coordinator agent contract.
    """

    coordinator = create_coordinator()

    portfolio_registration = (
        coordinator._agents["portfolio"]
    )

    assert (
        portfolio_registration["instance"]
        is not None
    )

    assert (
        portfolio_registration["method"]
        == "process"
    )

    assert (
        portfolio_registration["input_type"]
        == coordinator.QUERY_INPUT
    )


# ------------------------------------------------------------------
# Test 3
# ------------------------------------------------------------------

def test_portfolio_intent_routing() -> None:
    """
    Verify that a portfolio-related query is routed to the
    Portfolio Agent.

    This test validates the Coordinator's integration with the
    semantic IntentRoutingService.

    No LLM call is required.
    """

    coordinator = create_coordinator()

    query = (
        "What are the main risks and opportunities "
        "in the current portfolio?"
    )

    routing_decision = (
        coordinator.routing_service
        .route_request(query)
    )

    assert routing_decision is not None

    assert (
        "portfolio"
        in routing_decision.selected_agents
    )


# ------------------------------------------------------------------
# Test 4
# ------------------------------------------------------------------

def test_portfolio_agent_invocation() -> None:
    """
    Verify that the Coordinator can invoke the Portfolio Agent
    through its generic agent registration mechanism.

    This test uses the real Portfolio Agent and therefore invokes
    the analytical and LLM reasoning layers.
    """

    coordinator = create_coordinator()

    query = (
        "Provide a concise overview of the portfolio "
        "including its key risks, trends and opportunities."
    )

    response = coordinator.process_query(
        query
    )

    assert response is not None

    assert isinstance(
        response,
        dict,
    )


# ------------------------------------------------------------------
# Test 5
# ------------------------------------------------------------------

def test_portfolio_end_to_end_response() -> None:
    """
    Validate the complete Coordinator → Portfolio Agent →
    Analytics → Reasoning → LLM flow.
    """

    coordinator = create_coordinator()

    query = (
        "Analyze the current portfolio and identify "
        "the most important risks, trends and "
        "business opportunities."
    )

    response = coordinator.process_query(
        query
    )

    assert response is not None

    assert isinstance(
        response,
        dict,
    )

    # --------------------------------------------------------------
    # Coordinator response contract
    # --------------------------------------------------------------

    assert (
        response.get("success") is True
    )

    assert (
        "agents_invoked"
        in response
    )

    assert (
        "responses"
        in response
    )

    # --------------------------------------------------------------
    # Portfolio Agent invocation
    # --------------------------------------------------------------

    agents_invoked = (
        response["agents_invoked"]
    )

    assert (
        "portfolio"
        in agents_invoked
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
# Test 6
# ------------------------------------------------------------------

def test_portfolio_routing_metadata() -> None:
    """
    Verify that Coordinator preserves routing metadata generated
    by IntentRoutingService.
    """

    coordinator = create_coordinator()

    query = (
        "What is the overall health of the portfolio "
        "and where are the major risk concentrations?"
    )

    response = coordinator.process_query(
        query
    )

    assert response.get(
        "routing"
    ) is not None

    routing = response["routing"]

    assert (
        "candidate_agents"
        in routing
    )

    assert (
        "routing_reasons"
        in routing
    )

    assert (
        "similarity_results"
        in routing
    )


# ------------------------------------------------------------------
# Test 7
# ------------------------------------------------------------------

def test_empty_query_handling() -> None:
    """
    Verify graceful handling of an empty query.

    This test must not invoke an agent or the LLM.
    """

    coordinator = create_coordinator()

    response = coordinator.process_query(
        ""
    )

    assert response is not None

    assert isinstance(
        response,
        dict,
    )

    assert (
        response.get("success")
        is False
    )

    assert (
        response.get("message")
        == "Please provide a valid query."
    )


# ------------------------------------------------------------------
# Test 8
# ------------------------------------------------------------------

def test_policy_routing_regression() -> None:
    """
    Verify that existing Policy Agent routing remains functional
    after Portfolio Agent registration.
    """

    coordinator = create_coordinator()

    query = (
        "What is the minimum credit score required "
        "for a premium credit card?"
    )

    routing_decision = (
        coordinator.routing_service
        .route_request(query)
    )

    assert routing_decision is not None

    assert (
        "policy"
        in routing_decision.selected_agents
    )


# ------------------------------------------------------------------
# Test 9
# ------------------------------------------------------------------

def test_customer_routing_regression() -> None:
    """
    Verify that existing Customer Agent routing remains functional
    after Portfolio Agent registration.

    The query should contain a valid customer identifier.
    """

    coordinator = create_coordinator()

    query = (
        "Show me the risk assessment for customer CUST001."
    )

    routing_decision = (
        coordinator.routing_service
        .route_request(query)
    )

    assert routing_decision is not None

    assert (
        "customer"
        in routing_decision.selected_agents
    )


# ------------------------------------------------------------------
# Main Test Runner
# ------------------------------------------------------------------

def main() -> None:
    """
    Execute the Coordinator Agent smoke-test suite.
    """

    print()
    print("=" * 75)
    print("Coordinator Agent : Smoke Test")
    print("=" * 75)

    print(
        "NOTE: Portfolio end-to-end tests require "
        "OPENAI_API_KEY and OPENAI_MODEL."
    )

    print()

    run_test(
        "CoordinatorAgent initialization",
        test_coordinator_initialization,
    )

    run_test(
        "Portfolio Agent registration",
        test_portfolio_agent_registration,
    )

    run_test(
        "Portfolio intent routing",
        test_portfolio_intent_routing,
    )

    run_test(
        "Portfolio Agent invocation",
        test_portfolio_agent_invocation,
    )

    run_test(
        "Portfolio end-to-end response",
        test_portfolio_end_to_end_response,
    )

    run_test(
        "Portfolio routing metadata",
        test_portfolio_routing_metadata,
    )

    run_test(
        "Empty query handling",
        test_empty_query_handling,
    )

    run_test(
        "Policy routing regression",
        test_policy_routing_regression,
    )

    run_test(
        "Customer routing regression",
        test_customer_routing_regression,
    )

    print()
    print("=" * 75)
    print("Coordinator Agent : Smoke Test PASSED")
    print("=" * 75)


if __name__ == "__main__":
    main()
