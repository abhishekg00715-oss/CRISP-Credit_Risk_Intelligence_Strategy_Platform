"""
routing_evaluation_service.py

Purpose
-------
Evaluates semantic routing decisions against
expected routing outcomes.
"""

from dataclasses import dataclass

from src.models.routing_models import RoutingDecision


# ---------------------------------------------------------------------
# Evaluation Result
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RoutingEvaluationResult:

    passed: bool

    expected_agents: list[str]

    actual_agents: list[str]

    missing_agents: list[str]

    unexpected_agents: list[str]

    accuracy: float

    confidence: float


# ---------------------------------------------------------------------
# Routing Evaluation Service
# ---------------------------------------------------------------------

class RoutingEvaluationService:
    """
    Stateless evaluation component.

    This service evaluates an already
    generated RoutingDecision.

    It never invokes the router.
    """

    def __init__(self) -> None:
        pass

    # ---------------------------------------------------------

    def evaluate(
        self,
        decision: RoutingDecision,
        expected_agents: list[str]
    ) -> RoutingEvaluationResult:

        expected = set(expected_agents)

        actual = set(
            decision.selected_agents
        )

        missing = sorted(
            expected - actual
        )

        unexpected = sorted(
            actual - expected
        )

        passed = (
            not missing
            and
            not unexpected
        )

        return RoutingEvaluationResult(

            passed=passed,

            expected_agents=sorted(expected),

            actual_agents=sorted(actual),

            missing_agents=missing,

            unexpected_agents=unexpected,

            accuracy=self._calculate_accuracy(
                expected,
                actual
            ),

            confidence=self._calculate_confidence(
                decision
            )

        )

    # ---------------------------------------------------------

    @staticmethod
    def _calculate_accuracy(
        expected: set[str],
        actual: set[str]
    ) -> float:

        union = expected | actual

        if not union:

            return 1.0

        return round(

            len(expected & actual)
            / len(union),

            3

        )

    # ---------------------------------------------------------

    @staticmethod
    def _calculate_confidence(
        decision: RoutingDecision
    ) -> float:

        scores = [

            result.similarity_score

            for result

            in decision.similarity_results

            if result.agent_name
            in decision.selected_agents

        ]

        if not scores:

            return 0.0

        return round(

            sum(scores)
            / len(scores),

            3

        )