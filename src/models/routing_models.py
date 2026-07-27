"""
routing_models.py

Purpose
-------
Shared routing models used throughout the
semantic routing and orchestration pipeline.

Responsibilities
----------------
- Represent semantic similarity results
- Represent routing decisions
- Provide a common contract between:
    * IntentRoutingService
    * RoutingPolicyService
    * CoordinatorAgent

Author
------
Credit Risk Research Agent
"""

from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------------------
# Similarity Result
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class AgentSimilarityResult:
    """
    Represents the highest semantic similarity
    achieved by an agent.
    """

    agent_name: str

    similarity_score: float

    matched_intent: str


# ---------------------------------------------------------------------
# Routing Decision
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RoutingDecision:
    """
    Represents the complete routing decision.

    Routing occurs in two stages:

    1. Semantic routing identifies candidate agents.
    2. Routing policies refine the final selection.
    """

    # ---------------------------------------------------------
    # Stage 1
    # ---------------------------------------------------------

    candidate_agents: List[str]

    # ---------------------------------------------------------
    # Stage 2
    # ---------------------------------------------------------

    selected_agents: List[str]

    # ---------------------------------------------------------
    # Explainability
    # ---------------------------------------------------------

    similarity_results: List[AgentSimilarityResult]

    customer_id: str | None

    routing_reasons: List[str] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Extracted Context
    # ---------------------------------------------------------

    customer_id: str | None = None