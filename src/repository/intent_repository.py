"""
Intent Repository

Provides access to the semantic intent definitions registered
within the platform.

Responsibilities
----------------
- Load registered agent intents.
- Retrieve intent definitions.
- Retrieve intent examples.
- Support future dynamic registration if required.

Author: Abhishek Gupta
Project: Credit Decision Intelligence Platform
"""

from typing import Dict, List, Optional

from src.config.intent_definitions import (
    AgentIntentDefinition,
    REGISTERED_INTENTS
)


class IntentRepository:
    """
    Repository responsible for managing semantic intent definitions.

    This repository acts as the single access layer for retrieving
    registered agent intent metadata.
    """

    def __init__(self) -> None:

        self._intent_registry: Dict[str, AgentIntentDefinition] = {
            intent.agent_name: intent
            for intent in REGISTERED_INTENTS
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_registered_agents(self) -> List[str]:
        """
        Returns all registered agent identifiers.
        """

        return list(self._intent_registry.keys())

    def get_intent_definition(
        self,
        agent_name: str
    ) -> Optional[AgentIntentDefinition]:
        """
        Returns the intent definition for a specific agent.
        """

        return self._intent_registry.get(agent_name)


    def get_all_intent_definitions(
        self
    ) -> List[AgentIntentDefinition]:
        """
        Returns all registered intent definitions.
        """

        return list(self._intent_registry.values())

    

    def agent_exists(
        self,
        agent_name: str
    ) -> bool:
        """
        Returns True if the agent is registered.
        """

        return agent_name in self._intent_registry
