"""
routing_evaluation_service.py

Purpose
-------
Evaluates semantic routing decisions against
expected routing outcomes.

Responsibilities
----------------
- Compare expected and actual agent selection
- Calculate routing accuracy
- Identify missing agents
- Identify unexpected agents
- Produce explainable evaluation results

Notes
-----
This service performs evaluation only.

It contains no routing logic, semantic search,
or business policy implementation.

Author
------
Credit Risk Research Agent
"""

from dataclasses import dataclass
from typing import List, Set

from src.models.routing_models import (
    RoutingDecision
)


# ---------------------------------------------------------------------
# Evaluation Result
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RoutingEvaluationResult:
    """
    Represents the outcome of evaluating a
    routing decision.
    """

    passed: bool

    expected_agents: List[str]

    actual_agents: List[str]

    missing_agents: List[str]

    unexpected_agents: List[str]

    accuracy: float

    confidence: float


# ---------------------------------------------------------------------
# Routing Evaluation Service
# ---------------------------------------------------------------------

class RoutingEvaluationService:
    """
    Evaluates routing decisions produced by
    the semantic routing engine.
    """

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------

    def evaluate(
        self,
        decision: RoutingDecision,
        expected_agents: List[str]
    ) -> RoutingEvaluationResult:
        """
        Compare the routing decision with the
        expected routing outcome.
        """

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

        accuracy = self._calculate_accuracy(

            expected,

            actual

        )

        confidence = self._calculate_confidence(
            decision
        )

        return RoutingEvaluationResult(

            passed=passed,

            expected_agents=sorted(expected),

            actual_agents=sorted(actual),

            missing_agents=missing,

            unexpected_agents=unexpected,

            accuracy=accuracy,

            confidence=confidence

        )

    # -------------------------------------------------------------
    # Private Helpers
    # -------------------------------------------------------------

    @staticmethod
    def _calculate_accuracy(
        expected: Set[str],
        actual: Set[str]
    ) -> float:
        """
        Calculates routing accuracy using
        Jaccard similarity.

        Perfect match = 1.0
        """

        union = expected | actual

        if not union:

            return 1.0

        intersection = expected & actual

        return round(

            len(intersection)
            / len(union),

            3

        )

    # -------------------------------------------------------------

    @staticmethod
    def _calculate_confidence(
        decision: RoutingDecision
    ) -> float:
        """
        Returns the average similarity score
        of all selected agents.

        Intended for reporting only.
        """

        selected = [

            result.similarity_score

            for result

            in decision.similarity_results

            if result.agent_name
            in decision.selected_agents

        ]

        if not selected:

            return 0.0

        return round(

            sum(selected)
            / len(selected),

            3

        )
