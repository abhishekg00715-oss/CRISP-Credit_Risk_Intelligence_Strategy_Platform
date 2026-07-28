"""
routing_regression_test.py
"""

from src.initialization.application_startup import (
    ApplicationStartup
)

from src.services.routing_evaluation_service import (
    RoutingEvaluationService
)

from src.services.routing_evaluation_report import (
    RoutingEvaluationReport
)

from tests.routing.routing_test_cases import (
    ROUTING_TEST_CASES
)


def main() -> None:

    print("\n" + "=" * 80)
    print("SEMANTIC ROUTING REGRESSION TEST")
    print("=" * 80)

    startup = (
        ApplicationStartup()
        .initialize()
    )

    router = startup.routing_service

    evaluator = (
        RoutingEvaluationService()
    )

    report = (
        RoutingEvaluationReport()
    )

    for test_case in ROUTING_TEST_CASES:

        decision = (
            router.route_request(
                test_case.query
            )
        )

        evaluation = (
            evaluator.evaluate(

                decision=decision,

                expected_agents=(
                    test_case.expected_agents
                )

            )
        )

        report.record_result(

            test_case=test_case,

            evaluation=evaluation

        )

    report.print_summary()

    if report.failed_cases:

        raise AssertionError(
            "\nRouting regression suite failed."
        )

    print(
        "\n✓ Routing regression suite passed."
    )


if __name__ == "__main__":

    main()