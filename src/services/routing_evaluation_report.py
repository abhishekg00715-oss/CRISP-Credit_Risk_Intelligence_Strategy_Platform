"""
routing_evaluation_report.py
"""

from dataclasses import dataclass
from typing import List

from tests.routing.routing_test_cases import RoutingTestCase

from src.services.routing_evaluation_service import (
    RoutingEvaluationResult
)


@dataclass
class FailedRoutingCase:

    query: str

    expected_agents: List[str]

    actual_agents: List[str]


class RoutingEvaluationReport:

    def __init__(self):

        self.total = 0

        self.passed = 0

        self.failed_cases: List[
            FailedRoutingCase
        ] = []

    # ---------------------------------------------------------

    def record_result(
        self,
        test_case: RoutingTestCase,
        evaluation: RoutingEvaluationResult
    ) -> None:

        self.total += 1

        if evaluation.passed:

            self.passed += 1

            return

        self.failed_cases.append(

            FailedRoutingCase(

                query=test_case.query,

                expected_agents=(
                    evaluation.expected_agents
                ),

                actual_agents=(
                    evaluation.actual_agents
                )

            )

        )

    # ---------------------------------------------------------

    @property
    def accuracy(self) -> float:

        if self.total == 0:

            return 0.0

        return round(

            (
                self.passed
                / self.total
            ) * 100,

            2

        )

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