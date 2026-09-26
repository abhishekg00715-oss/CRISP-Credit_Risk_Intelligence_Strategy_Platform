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


"""

from src.initialization.routing_bootstrap import (
    RoutingBootstrap
)

from src.agents.coordinator_agent import (
    CoordinatorAgent
)

from src.agents.portfolio_agent import (
    PortfolioAgent
)

from src.services.portfolio_analytics_service import (
    PortfolioAnalyticsService,
)

from src.services.portfolio_summary_service import (
    PortfolioSummaryService,
)

from src.services.portfolio_reasoning_service import (
    PortfolioReasoningService,
)

from src.services.llm_service import (
    LLMService,
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

        self.portfolio_analytics_service = None
        self.portfolio_summary_service = None
        self.portfolio_reasoning_service = None
        self.portfolio_agent = None
        self.coordinator = None

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

        # -----------------------------------------------------
        # Routing infrastructure
        # -----------------------------------------------------

        self.routing_bootstrap = (
            RoutingBootstrap()
            .initialize()
        )

        # -----------------------------------------------------
        # Portfolio dependencies
        # -----------------------------------------------------

        self.portfolio_analytics_service = (
            PortfolioAnalyticsService()
        )

        self.portfolio_summary_service = (
            PortfolioSummaryService(
                analytics_service=(
                    self.portfolio_analytics_service
                )
            )
        )

        self.portfolio_reasoning_service = (
            PortfolioReasoningService(
                llm_service=LLMService()
            )
        )

        self.portfolio_agent = (
            PortfolioAgent(
                summary_service=(
                    self.portfolio_summary_service
                ),
                reasoning_service=(
                    self.portfolio_reasoning_service
                ),
            )
        )

        # -----------------------------------------------------
        # Coordinator
        # -----------------------------------------------------

        self.coordinator = CoordinatorAgent(
            routing_service=(
                self.routing_bootstrap
                .intent_routing_service
            ),
            portfolio_agent=self.portfolio_agent,
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