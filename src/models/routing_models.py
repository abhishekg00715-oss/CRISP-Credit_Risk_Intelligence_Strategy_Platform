from dataclasses import dataclass
from typing import List

# ---------------------------------------------------------
# Routing Models
# ---------------------------------------------------------

@dataclass(frozen=True)
class AgentSimilarityResult:
    """
    Represents the best semantic match
    identified for a registered agent.
    """
    agent_name: str

    similarity_score: float

    matched_intent: str

@dataclass(frozen=True)
class RoutingDecision:
     """
    Represents the complete routing
    decision for a user request.
    """

    selected_agents: List[str]

    similarity_results: List[AgentSimilarityResult]

    customer_id: str | None
