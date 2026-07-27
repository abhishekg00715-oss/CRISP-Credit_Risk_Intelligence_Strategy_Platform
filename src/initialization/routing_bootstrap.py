"""
routing_bootstrap.py

Purpose
-------
Bootstraps the semantic intent routing subsystem.

Responsibilities
----------------
- Create routing dependencies
- Initialize semantic intent embeddings
- Construct the routing pipeline
- Expose initialized routing components

Author
------
Credit Risk Research Agent
"""

from src.repository.intent_repository import (
    IntentRepository
)

from src.services.embedding_service import (
    EmbeddingService
)

from src.services.intent_embedding_service import (
    IntentEmbeddingService
)

from src.initialization.intent_embedding_initializer import (
    IntentEmbeddingInitializer
)

from src.services.similarity_service import (
    SimilarityService
)

from src.services.routing_policy_service import (
    RoutingPolicyService
)

from src.services.intent_routing_service import (
    IntentRoutingService
)


class RoutingBootstrap:
    """
    Bootstraps the semantic routing subsystem.

    This component is responsible for wiring
    together all routing dependencies during
    application startup.
    """

    def __init__(self):

        # -----------------------------------------
        # Core Services
        # -----------------------------------------

        self.embedding_service = (
            EmbeddingService()
        )

        self.intent_repository = (
            IntentRepository()
        )

        self.intent_embedding_service = (
            IntentEmbeddingService(
                repository=self.intent_repository,
                embedding_service=self.embedding_service
            )
        )

        # -----------------------------------------
        # Initialize embeddings
        # -----------------------------------------

        initializer = (
            IntentEmbeddingInitializer(
                self.intent_embedding_service
            )
        )

        initializer.initialize()

        # -----------------------------------------
        # Supporting services
        # -----------------------------------------

        self.similarity_service = (
            SimilarityService()
        )

        self.routing_policy_service = (
            RoutingPolicyService()
        )

        # -----------------------------------------
        # Routing service
        # -----------------------------------------

        self.intent_routing_service = (
            IntentRoutingService(
                embedding_service=self.embedding_service,
                intent_embedding_service=(
                    self.intent_embedding_service
                ),
                similarity_service=(
                    self.similarity_service
                ),
                routing_policy_service=(
                    self.routing_policy_service
                )
            )
        )
