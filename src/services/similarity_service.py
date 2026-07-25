"""
similarity_service.py

Purpose
-------
Provides semantic similarity computation between a user query
embedding and registered intent embeddings.

Responsibilities
----------------
- Compute cosine similarity
- Identify the best matching intent example for each agent
- Rank agents by similarity score
- Return explainable similarity results

Author:
Credit Risk Research Agent
"""

from dataclasses import dataclass
from typing import Dict, List

import numpy as np

from src.services.intent_embedding_service import EmbeddedIntent


# ---------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class AgentSimilarityResult:
    """
    Represents the highest semantic similarity score
    achieved by an agent.
    """

    agent_name: str
    similarity_score: float
    matched_intent: str


# ---------------------------------------------------------------------
# Similarity Service
# ---------------------------------------------------------------------

class SimilarityService:
    """
    Computes semantic similarity between a query embedding
    and cached agent intent embeddings.
    """

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def find_best_matches(
        self,
        query_embedding: np.ndarray,
        intent_embeddings: Dict[str, List[EmbeddedIntent]]
    ) -> List[AgentSimilarityResult]:
        """
        Computes the best semantic match for each registered agent.

        Parameters
        ----------
        query_embedding : np.ndarray
            User query embedding.

        intent_embeddings : Dict[str, List[EmbeddedIntent]]
            Cached intent embeddings grouped by agent.

        Returns
        -------
        List[AgentSimilarityResult]
            Ranked list ordered by descending similarity.
        """

        similarity_results = []

        for (
            agent_name,
            embedded_intents
        ) in intent_embeddings.items():

            best_match = self._find_best_agent_match(
                query_embedding=query_embedding,
                embedded_intents=embedded_intents
            )

            similarity_results.append(

                AgentSimilarityResult(

                    agent_name=agent_name,

                    similarity_score=best_match["score"],

                    matched_intent=best_match["intent"]

                )

            )

        similarity_results.sort(

            key=lambda result: result.similarity_score,

            reverse=True

        )

        return similarity_results

    # --------------------------------------------------------------
    # Private Methods
    # --------------------------------------------------------------

    def _find_best_agent_match(
        self,
        query_embedding: np.ndarray,
        embedded_intents: List[EmbeddedIntent]
    ) -> Dict:
        """
        Returns the highest scoring intent example
        for an individual agent.
        """

        best_score = -1.0
        best_intent = ""

        for intent in embedded_intents:

            score = self._cosine_similarity(

                query_embedding,

                intent.embedding

            )

            if score > best_score:

                best_score = score

                best_intent = intent.intent_text

        return {

            "score": float(best_score),

            "intent": best_intent

        }

    # --------------------------------------------------------------

    @staticmethod
    def _cosine_similarity(
        vector_a: np.ndarray,
        vector_b: np.ndarray
    ) -> float:
        """
        Computes cosine similarity between two vectors.

        Since embeddings are normalized during generation,
        cosine similarity reduces to the dot product.
        """

        return float(

            np.dot(vector_a, vector_b)

        )
