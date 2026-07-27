"""
application_startup.py

Purpose
-------
Initializes the shared application infrastructure.

Responsibilities
----------------
- Build shared infrastructure services
- Initialize semantic routing
- Expose initialized components
- Ensure startup occurs only once

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

from src.services.similarity_service import (
    SimilarityService
)

from src.services.routing_policy_service import (
    RoutingPolicyService
)

from src.services.intent_routing_service import (
    IntentRoutingService
)

from src.startup.routing_bootstrap import (
    RoutingBootstrap
)


class ApplicationStartup:
    """
    Initializes the complete routing infrastructure.

    Startup is performed only once and the created
    service instances are shared throughout the
    application.
    """

    def __init__(self):

        self._initialized = False

        self.embedding_service = None

        self.intent_repository = None

        self.intent_embedding_service = None

        self.similarity_service = None

        self.routing_policy_service = None

        self.routing_service = None

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def initialize(self) -> None:
        """
        Initializes the application.

        Safe to call multiple times.
        """

        if self._initialized:

            return

        # -------------------------------------------------
        # Shared Services
        # -------------------------------------------------

        self.embedding_service = (
            EmbeddingService()
        )

        self.intent_repository = (
            IntentRepository()
        )

        self.intent_embedding_service = (
            IntentEmbeddingService(

                repository=
                self.intent_repository,

                embedding_service=
                self.embedding_service
            )
        )

        self.similarity_service = (
            SimilarityService()
        )

        self.routing_policy_service = (
            RoutingPolicyService()
        )

        # -------------------------------------------------
        # Initialize Intent Embeddings
        # -------------------------------------------------

        RoutingBootstrap(

            intent_embedding_service=
            self.intent_embedding_service

        ).initialize()

        # -------------------------------------------------
        # Routing Service
        # -------------------------------------------------

        self.routing_service = (
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

    # ---------------------------------------------------------

    @property
    def initialized(self) -> bool:

        return self._initialized
