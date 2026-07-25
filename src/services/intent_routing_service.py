"""
intent_routing_service.py

Purpose
-------
Determine which specialist agents should
process a user's request using semantic
similarity.

Responsibilities
----------------
- Normalize requests
- Extract customer identifiers
- Generate query embeddings
- Perform semantic intent routing
- Return routing decisions

Author
------
Credit Risk Research Agent
"""

import re

from dataclasses import dataclass
from typing import List

from src.config.intent_rules import CUSTOMER_ID_PATTERN

from src.services.embedding_service import EmbeddingService
from src.services.intent_embedding_service import IntentEmbeddingService
from src.services.similarity_service import (
    SimilarityService,
    AgentSimilarityResult
)


# ------------------------------------------------------------------
# Routing Models
# ------------------------------------------------------------------

@dataclass(frozen=True)
class RoutingDecision:
    """
    Represents the routing outcome
    for a user request.
    """

    selected_agents: List[str]

    similarity_results: List[AgentSimilarityResult]

    customer_id: str | None


# ------------------------------------------------------------------
# Intent Routing Service
# ------------------------------------------------------------------

class IntentRoutingService:

    DEFAULT_SIMILARITY_THRESHOLD = 0.70

    def __init__(
        self,
        embedding_service: EmbeddingService,
        intent_embedding_service: IntentEmbeddingService,
        similarity_service: SimilarityService,
        similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD
    ):

        self._embedding_service = embedding_service

        self._intent_embedding_service = (
            intent_embedding_service
        )

        self._similarity_service = (
            similarity_service
        )

        self._threshold = similarity_threshold

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def identify_agents(
        self,
        request: str
    ) -> List[str]:
        """
        Backward-compatible API.

        Returns only the selected agents.
        """

        return self.route_request(
            request
        ).selected_agents

    # --------------------------------------------------------------

    def route_request(
        self,
        request: str
    ) -> RoutingDecision:
        """
        Performs semantic routing and
        returns the complete routing decision.
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

            self._embedding_service.generate_embedding(

                normalized_request

            )

        )

        similarity_results = (

            self._similarity_service.find_best_matches(

                query_embedding,

                self._intent_embedding_service.get_all_embeddings()

            )

        )

        selected_agents = [

            result.agent_name

            for result

            in similarity_results

            if result.similarity_score >= self._threshold

        ]

        return RoutingDecision(

            selected_agents=selected_agents,

            similarity_results=similarity_results,

            customer_id=customer_id

        )

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
