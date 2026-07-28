"""
routing_regression_test.py

Purpose
-------
Executes the semantic routing regression suite using
the predefined routing benchmark scenarios.

Responsibilities
----------------
- Bootstrap routing components
- Execute benchmark routing scenarios
- Evaluate routing accuracy
- Produce a standardized evaluation report

Author
------
Credit Risk Research Agent
"""

from src.initialization.application_startup import (
    ApplicationStartup
)
from src.services.routing_evaluation_service import (
    RoutingEvaluationService
)
from tests.services.routing_test_cases import (
    ROUTING_TEST_CASES
)
from tests.services.routing_evaluation_report import (
    RoutingEvaluationReport
)


# ---------------------------------------------------------
# Regression Runner
# ---------------------------------------------------------

def main() -> None:
    """
    Execute the complete routing regression suite.
    """

    print("\n" + "=" * 80)
    print("SEMANTIC ROUTING REGRESSION TEST")
    print("=" * 80)

    # -----------------------------------------------------
    # Bootstrap application
    # -----------------------------------------------------

    startup = ApplicationStartup()

    services = startup.initialize()

    router = services.intent_routing_service

    # -----------------------------------------------------
    # Evaluation Service
    # -----------------------------------------------------

    evaluator = RoutingEvaluationService(
        router=router
    )

    report = RoutingEvaluationReport()

    # -----------------------------------------------------
    # Execute benchmark scenarios
    # -----------------------------------------------------

    for test_case in ROUTING_TEST_CASES:

        decision = evaluator.evaluate(
            test_case.query
        )

        report.record_result(
            test_case=test_case,
            decision=decision
        )

    # -----------------------------------------------------
    # Display Report
    # -----------------------------------------------------

    report.print_summary()

    # -----------------------------------------------------
    # Regression Result
    # -----------------------------------------------------

    if report.failed_cases:

        raise AssertionError(
            "\nRouting regression suite failed."
        )

    print("\n✓ Routing regression suite passed.")


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":

    main()
