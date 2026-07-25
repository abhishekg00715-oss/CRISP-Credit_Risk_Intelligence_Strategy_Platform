"""
intent_embedding_service.py

Purpose
-------
Generate and cache semantic embeddings for
registered agent intent examples.

This service reuses the existing EmbeddingService
introduced in Phase 1.

Responsibilities
----------------
- Load registered intents
- Generate embeddings
- Cache embeddings
- Provide intent vectors for routing

Author:
Credit Risk Research Agent
"""

from dataclasses import dataclass
from typing import Dict, List

import numpy as np

from src.repository.intent_repository import IntentRepository
from src.services.embedding_service import EmbeddingService


# ------------------------------------------------------------------
# Data Model
# ------------------------------------------------------------------

@dataclass
class EmbeddedIntent:
    """
    Represents an embedded intent example.
    """

    agent_name: str
    intent_text: str
    embedding: np.ndarray


# ------------------------------------------------------------------
# Intent Embedding Service
# ------------------------------------------------------------------

class IntentEmbeddingService:
    """
    Generates semantic embeddings for
    registered intent examples.

    Embeddings are generated once during
    application startup and reused for
    semantic routing.
    """

    def __init__(
        self,
        repository: IntentRepository,
        embedding_service: EmbeddingService
    ):

        self._repository = repository

        self._embedding_service = embedding_service

        self._intent_embeddings: Dict[
            str,
            List[EmbeddedIntent]
        ] = {}

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def initialize(self) -> None:
        """
        Generates embeddings for all
        registered intent examples.
        """

        self._intent_embeddings.clear()

        for definition in (
            self._repository.get_all_intent_definitions()
        ):

            embedded_examples = []

            for example in definition.intent_examples:

                vector = (
                    self._embedding_service
                    .generate_embedding(example)
                )

                embedded_examples.append(

                    EmbeddedIntent(

                        agent_name=definition.agent_name,

                        intent_text=example,

                        embedding=vector

                    )

                )

            self._intent_embeddings[
                definition.agent_name
            ] = embedded_examples

    # --------------------------------------------------------------

    def get_agent_embeddings(
        self,
        agent_name: str
    ) -> List[EmbeddedIntent]:

        return self._intent_embeddings.get(
            agent_name,
            []
        )

    # --------------------------------------------------------------

    def get_all_embeddings(
        self
    ) -> Dict[
        str,
        List[EmbeddedIntent]
    ]:

        return self._intent_embeddings

    # --------------------------------------------------------------

    def is_initialized(self) -> bool:

        return len(
            self._intent_embeddings
        ) > 0

    # --------------------------------------------------------------

    def get_registered_agents(self):

        return list(
            self._intent_embeddings.keys()
        )
