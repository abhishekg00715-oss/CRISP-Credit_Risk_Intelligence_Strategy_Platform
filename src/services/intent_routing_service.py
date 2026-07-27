"""
intent_routing_service.py

Purpose
-------
Determine candidate specialist agents using
semantic similarity.

Responsibilities
----------------
- Normalize requests
- Extract customer identifiers
- Generate query embeddings
- Perform semantic similarity matching
- Select candidate agents
- Produce routing decision for policy enrichment

Author
------
Credit Risk Research Agent
"""

import re

from typing import List

from src.config.intent_rules import (
    CUSTOMER_ID_PATTERN
)

from src.models.routing_models import (
    RoutingDecision,
    AgentSimilarityResult
)

from src.services.embedding_service import (
    EmbeddingService
)

from src.services.intent_embedding_service import (
    IntentEmbeddingService
)

from src.services.similarity_service import (
    SimilarityService
)

from src.services.routing_policy_service import (
    RoutingPolicyService
)

# ------------------------------------------------------------------
# Intent Routing Service
# ------------------------------------------------------------------

class IntentRoutingService:
    """
    Performs semantic capability detection.

    This service identifies candidate agents
    using semantic similarity only.

    Business orchestration rules are applied
    later by RoutingPolicyService.
    """

    DEFAULT_SIMILARITY_THRESHOLD = 0.7

    MULTI_AGENT_MARGIN = 0.05

    # --------------------------------------------------------------

    def __init__(
        self,
        embedding_service: EmbeddingService,
        intent_embedding_service: IntentEmbeddingService,
        similarity_service: SimilarityService,
        routing_policy_service: RoutingPolicyService,
        similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
        multi_agent_margin: float = MULTI_AGENT_MARGIN
    ):

        self._embedding_service = (
            embedding_service
        )

        self._intent_embedding_service = (
            intent_embedding_service
        )

        self._similarity_service = (
            similarity_service
        )

        self._threshold = (
            similarity_threshold
        )

        self._multi_agent_margin = (
            multi_agent_margin
        )

        self._routing_policy_service = (
            routing_policy_service
        )

        self._multi_agent_margin = (
            multi_agent_margin
        )

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def identify_agents(
        self,
        request: str
    ) -> List[str]:
        """
        Backward compatible API.

        Returns the candidate agents.
        """

        return (
            self.route_request(
                request
            ).candidate_agents
        )

    # --------------------------------------------------------------

    def route_request(
        self,
        request: str
    ) -> RoutingDecision:
        """
        Performs semantic routing.

        Returns a routing decision
        containing candidate agents.
        """

        normalized_request = (
            self._normalize_request(
                request
            )
        )

        customer_id = (
            self.extract_customer_id(
                normalized_request
            )
        )

        query_embedding = (
            self._embedding_service
            .generate_embedding(
                normalized_request
            )
        )

        similarity_results = (
            self._similarity_service
            .find_best_matches(
                query_embedding,
                self._intent_embedding_service
                .get_all_embeddings()
            )
        )

        candidate_agents = (
            self._select_candidate_agents(
                similarity_results
            )
        )

        routing_result = (
            self._routing_policy_service
            .apply_rules(
                candidate_agents=candidate_agents,
                similarity_results=similarity_results,
                customer_id=customer_id,
                request=normalized_request
            )
        )

        return RoutingDecision(

            candidate_agents=candidate_agents,

            selected_agents=(
                routing_result.selected_agents
            ),

            similarity_results=(
                similarity_results
            ),

            customer_id=customer_id,

            routing_reasons=routing_result.routing_reasons

        )

    # --------------------------------------------------------------
    # Candidate Selection
    # --------------------------------------------------------------

    def _select_candidate_agents(
        self,
        similarity_results: List[
            AgentSimilarityResult
        ]
    ) -> List[str]:
        """
        Select semantic routing candidates.

        Rules
        -----
        1. Highest scoring agent must satisfy
           similarity threshold.

        2. Additional agents are included when
           they satisfy the threshold and are
           within the configured margin.
        """

        if not similarity_results:

            return []

        top_score = (
            similarity_results[0]
            .similarity_score
        )

        if top_score < self._threshold:

            return []

        candidate_agents = []

        for result in similarity_results:

            if (
                result.similarity_score
                < self._threshold
            ):

                continue

            if (
                top_score
                - result.similarity_score
                <= self._multi_agent_margin
            ):

                candidate_agents.append(
                    result.agent_name
                )

        return candidate_agents

    # --------------------------------------------------------------
    # Customer Identifier
    # --------------------------------------------------------------

    def extract_customer_id(
        self,
        request: str
    ) -> str | None:

        match = re.search(

            CUSTOMER_ID_PATTERN,

            request.upper()

        )

        if match:

            return match.group()

        return None

    # --------------------------------------------------------------

    @staticmethod
    def _normalize_request(
        request: str
    ) -> str:

        return request.lower().strip()