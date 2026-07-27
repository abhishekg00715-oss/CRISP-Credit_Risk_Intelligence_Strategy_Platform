"""
intent_embedding_initializer.py

Purpose
-------
Initializes semantic intent embeddings during
application startup.

Responsibilities
----------------
- Perform one-time initialization
- Prevent duplicate initialization
- Centralize startup logic
- Validate successful initialization

Notes
-----
This component should be executed once during
application startup before any routing requests
are processed.

Author
------
Credit Risk Research Agent
"""

from src.services.intent_embedding_service import (
    IntentEmbeddingService
)


class IntentEmbeddingInitializer:
    """
    Performs one-time initialization of
    semantic intent embeddings.
    """

    def __init__(
        self,
        intent_embedding_service: IntentEmbeddingService
    ) -> None:

        self._intent_embedding_service = (
            intent_embedding_service
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def initialize(self) -> None:
        """
        Initializes semantic intent embeddings
        only if they have not already been created.
        """

        if (
            self._intent_embedding_service
            .is_initialized()
        ):
            return

        self._intent_embedding_service.initialize()

        if (
            not self._intent_embedding_service
            .is_initialized()
        ):

            raise RuntimeError(
                "Intent embedding initialization failed."
            )
