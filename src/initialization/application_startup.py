"""
application_startup.py

Purpose
-------
Initializes the shared application
infrastructure.

Responsibilities
----------------
- Perform application startup
- Initialize routing subsystem
- Expose shared services
- Execute startup once

Author
------
Credit Risk Research Agent
"""

from src.initialization.routing_bootstrap import (
    RoutingBootstrap
)
from src.agents.coordinator_agent import (
    CoordinatorAgent
)



class ApplicationStartup:
    """
    Coordinates application startup.

    This component owns the application
    lifecycle while RoutingBootstrap owns
    the routing infrastructure.
    """

    def __init__(self):

        self._initialized = False

        self.routing_bootstrap = None

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def initialize(self):
        """
        Performs application startup.

        Safe to invoke multiple times.
        """

        if self._initialized:

            return self

        self.routing_bootstrap = (
            RoutingBootstrap()
            .initialize()
        )

        self.coordinator = CoordinatorAgent(

            routing_service=(
                self.routing_bootstrap
                .intent_routing_service
            )

        )

        self._initialized = True

        return self

    # ---------------------------------------------------------
    # Exposed Services
    # ---------------------------------------------------------

    @property
    def routing_service(self):

        return (
            self.routing_bootstrap
            .intent_routing_service
        )

    @property
    def embedding_service(self):

        return (
            self.routing_bootstrap
            .embedding_service
        )

    @property
    def intent_repository(self):

        return (
            self.routing_bootstrap
            .intent_repository
        )

    @property
    def intent_embedding_service(self):

        return (
            self.routing_bootstrap
            .intent_embedding_service
        )

    @property
    def similarity_service(self):

        return (
            self.routing_bootstrap
            .similarity_service
        )

    @property
    def routing_policy_service(self):

        return (
            self.routing_bootstrap
            .routing_policy_service
        )

    @property
    def initialized(self):

        return self._initialized