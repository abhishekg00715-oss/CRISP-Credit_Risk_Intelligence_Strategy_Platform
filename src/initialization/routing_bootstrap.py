"""
routing_bootstrap.py

Purpose
-------
Bootstraps the complete semantic routing subsystem.

Responsibilities
----------------
- Construct routing infrastructure
- Initialize semantic intent embeddings
- Build routing services
- Expose initialized services

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
    Builds and initializes the semantic
    routing infrastructure.

    Startup is safe to invoke multiple
    times.
    """

    def __init__(self):

        self._initialized = False

        self.embedding_service = None

        self.intent_repository = None

        self.intent_embedding_service = None

        self.similarity_service = None

        self.routing_policy_service = None

        self.intent_routing_service = None

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def initialize(self):
        """
        Initializes the routing subsystem.
        """

        if self._initialized:

            return self

        # -------------------------------------------------
        # Core Services
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Initialize Intent Embeddings
        # -------------------------------------------------

        IntentEmbeddingInitializer(
            self.intent_embedding_service
        ).initialize()

        # -------------------------------------------------
        # Supporting Services
        # -------------------------------------------------

        self.similarity_service = (
            SimilarityService()
        )

        self.routing_policy_service = (
            RoutingPolicyService()
        )

        # -------------------------------------------------
        # Intent Routing
        # -------------------------------------------------

        self.intent_routing_service = (
            IntentRoutingService(

                embedding_service=
                self.embedding_service,

                intent_embedding_service=
                self.intent_embedding_service,

                similarity_service=
                self.similarity_service,

                routing_policy_service=
                self.routing_policy_service
            )
        )

        self._initialized = True

        return self