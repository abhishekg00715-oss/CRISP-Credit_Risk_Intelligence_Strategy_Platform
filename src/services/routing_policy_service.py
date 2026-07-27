"""
routing_policy_service.py

Purpose
-------
Applies business routing policies to enrich the
semantic routing decision.

Responsibilities
----------------
- Evaluate routing business rules
- Promote mandatory agent execution
- Preserve semantic routing decisions
- Record applied routing rules
- Produce the final routing decision

Author
------
Credit Risk Research Agent
"""

from dataclasses import replace
from typing import List

from src.models.routing_models import (
    RoutingDecision
)


class RoutingPolicyService:
    """
    Applies deterministic routing policies
    after semantic intent detection.

    This service enriches the routing decision
    using business context rather than semantic
    similarity.
    """

    POLICY_AGENT = "policy"

    CUSTOMER_AGENT = "customer"

    RECOMMENDATION_AGENT = "recommendation"

    PORTFOLIO_AGENT = "portfolio"

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def apply_rules(
        self,
        candidate_agents: List[str],
        similarity_results: List,
        customer_id: str | None,
        request: str
    ) -> RoutingDecision:
        """
        Applies all routing policies and
        returns an updated RoutingDecision.
        """

        selected_agents = set(candidate_agents)

        routing_reasons = []

      

        # -------------------------------------------------
        # Rule 1
        # Customer identifier always requires
        # Customer Agent
        # -------------------------------------------------

        if (
            customer_id
            and self.CUSTOMER_AGENT
            not in selected_agents
        ):

            selected_agents.add(
                self.CUSTOMER_AGENT
            )

            applied_rules.append(
                "Customer ID detected -> Customer Agent added."
            )

        # -------------------------------------------------
        # Rule 2
        # Customer eligibility assessments require
        # both Customer and Policy Agents when both
        # intents are strongly represented.
        # -------------------------------------------------

        policy_score = self._get_similarity_score(
            similarity_results,
            self.POLICY_AGENT
        )

        customer_score = self._get_similarity_score(
            similarity_results,
            self.CUSTOMER_AGENT
        )

        if (
            customer_id
            and customer_score >= 0.75
            and policy_score >= 0.75
        ):

            selected_agents.add(
                self.CUSTOMER_AGENT
            )

            selected_agents.add(
                self.POLICY_AGENT
            )

            routing_reasons.append(
                "Customer eligibility assessment requires both "
                "Customer and Policy Agents."
            )

        # -------------------------------------------------
        # Rule 3
        # Recommendation depends upon
        # Customer assessment.
        # (Future-proof)
        # -------------------------------------------------

        if self.RECOMMENDATION_AGENT in selected_agents:

            if self.CUSTOMER_AGENT not in selected_agents:
                selected_agents.add(self.CUSTOMER_AGENT)

            if self.POLICY_AGENT not in selected_agents:
                selected_agents.add(self.POLICY_AGENT)

            routing_reasons.append(
                "Recommendation requires both "
                "Customer and Policy evaluation."
            )
        # -------------------------------------------------
        # Rule 4
        # Portfolio currently independent.
        # Reserved for future evolution.
        # -------------------------------------------------

        # -------------------------------------------------
        # Return updated immutable object
        # -------------------------------------------------

        return RoutingDecision(

            candidate_agents=candidate_agents,

            selected_agents=sorted(selected_agents),

            similarity_results=similarity_results,

            customer_id=customer_id,

            routing_reasons=routing_reasons

        )

    def _get_similarity_score(
        self,
        similarity_results,
        agent_name: str
    ) -> float:
        """
        Returns the similarity score for an agent.
        """

        for result in similarity_results:

            if result.agent_name == agent_name:

                return result.similarity_score

        return 0.0