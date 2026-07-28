"""
routing_evaluation_report.py

Purpose
-------
Produces a standardized routing evaluation report.

Responsibilities
----------------
- Display benchmark statistics
- Display routing accuracy
- Display failed scenarios
- Provide reusable reporting utilities

Author
------
Credit Risk Research Agent
"""

from dataclasses import dataclass
from typing import List

from src.models.routing_models import RoutingDecision
from tests.services.routing_test_cases import RoutingTestCase


@dataclass
class FailedRoutingCase:

    query: str

    expected_agents: List[str]

    actual_agents: List[str]


class RoutingEvaluationReport:
    """
    Produces evaluation summaries
    for routing benchmark execution.
    """

    def __init__(self):

        self.total = 0

        self.passed = 0

        self.failed_cases: List[
            FailedRoutingCase
        ] = []

    # ---------------------------------------------------------
    # Recording
    # ---------------------------------------------------------

    def record_result(
        self,
        test_case: RoutingTestCase,
        decision: RoutingDecision
    ) -> None:

        self.total += 1

        actual = set(
            decision.selected_agents
        )

        expected = set(
            test_case.expected_agents
        )

        if actual == expected:

            self.passed += 1

            return

        self.failed_cases.append(

            FailedRoutingCase(

                query=test_case.query,

                expected_agents=
                sorted(expected),

                actual_agents=
                sorted(actual)

            )

        )

    # ---------------------------------------------------------
    # Metrics
    # ---------------------------------------------------------

    @property
    def accuracy(self) -> float:

        if self.total == 0:

            return 0.0

        return (

            self.passed
            / self.total

        ) * 100

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    def print_summary(self) -> None:

        print("\n" + "=" * 80)

        print("ROUTING EVALUATION REPORT")

        print("=" * 80)

        print(f"Total Tests : {self.total}")

        print(f"Passed      : {self.passed}")

        print(
            f"Failed      : "
            f"{len(self.failed_cases)}"
        )

        print(
            f"Accuracy    : "
            f"{self.accuracy:.2f}%"
        )

        if not self.failed_cases:

            print(
                "\n✓ All routing scenarios passed."
            )

            return

        print("\nFailed Scenarios")

        print("-" * 80)

        for failure in self.failed_cases:

            print(
                f"\nQuery\n"
                f"  {failure.query}"
            )

            print(
                f"Expected\n"
                f"  {failure.expected_agents}"
            )

            print(
                f"Received\n"
                f"  {failure.actual_agents}"
            )
