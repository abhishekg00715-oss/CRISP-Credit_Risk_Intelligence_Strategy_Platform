"""
coordinator_agent.py

Purpose
-------
Central orchestration layer responsible
for routing user requests to the
appropriate specialist agent.

Current Capabilities
--------------------
- Policy Agent
- Customer Agent

Future Capabilities
-------------------
- Portfolio Agent
- Recommendation Agent
- Explainability Agent

Responsibilities
----------------
- Determine required specialist agents
- Delegate requests to the appropriate agent(s)
- Aggregate responses
- Return a standardized orchestration response

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


class CoordinatorAgent:
    """
    Central orchestration agent.
    """

    QUERY_INPUT = "query"
    CUSTOMER_ID_INPUT = "customer_id"

    def __init__(self) -> None:
        """
        Initialize routing service
        and specialist agents.
        """

        embedding_service = EmbeddingService()

        intent_embedding_service = (
            IntentEmbeddingService(
                repository=IntentRepository(),
                embedding_service=embedding_service
            )
        )

        intent_embedding_service.initialize()

        similarity_service = SimilarityService()


        self.routing_service = (
            IntentRoutingService(
                embedding_service=embedding_service,
                intent_embedding_service=(
                    intent_embedding_service
                ),
                similarity_service=similarity_service
            )
        )

        self.routing_policy_service = (
            RoutingPolicyService()
        )

        self._register_agents()
        self.response_formatter = (
            ResponseFormattingService()
        )
        self.query_logger = QueryLogger()
        self.execution_logger = (
            AgentExecutionLogger()
        )

    # ---------------------------------------------------------
    # Agent Registration
    # ---------------------------------------------------------

    def _register_agents(self) -> None:
        """
        Register all available
        specialist agents.
        """

        self._agents = {

            "policy": {

                "instance": PolicyAgent(),

                "method": "answer_question",

                "input_type": self.QUERY_INPUT

            },

            "customer": {

                "instance": CustomerAgent(),

                "method": "retrieve_customer_profile",

                "input_type": self.CUSTOMER_ID_INPUT

            }

        }

    # ---------------------------------------------------------
    # Routing
    # ---------------------------------------------------------

    def route_query(
        self,
        query: str,
        correlation_id: str
    ) -> Dict[str, Any]:
        """
        Route the request to one or
        more specialist agents.
        """

# ---------------------------------------------------------
# Semantic Routing
# ---------------------------------------------------------

        routing_decision = (
            self.routing_service.route_request(
                query
            )
        )

# ---------------------------------------------------------
# Business Rule Enrichment
# ---------------------------------------------------------

        routing_decision = (
            self.routing_policy_service.apply_rules(
                routing_decision
            )
        )

        agent_names = (
            routing_decision.selected_agents
        )

        customer_id = (
            routing_decision.customer_id
        )
        
        self.query_logger.log_query(
            query=query,
            agents=agent_names,
            customer_id=customer_id
        )

        if not routing_decision.selected_agents:

            return self._build_error_response(

                "Unable to determine the "
                "appropriate agent."

            )

        responses = {}

        for agent_name in agent_names:

            responses[agent_name] = (

                self._invoke_agent(

                    agent_name,

                    query,
                    correlation_id

                )

            )

        return {

            "success": True,

            "agents_invoked": (
                routing_decision.selected_agents
            ),
            "routing_decision": (
                routing_decision
            ),

            "responses": responses

        }



# ---------------------------------------------------------
# Agent Invocation
# ---------------------------------------------------------

    def _invoke_agent(
        self,
        agent_name: str,
        query: str,
        correlation_id: str
    ) -> Any:
        """
        Invoke the configured specialist agent
        and record execution metrics.
        """

        agent = self._agents[agent_name]

        handler = getattr(
            agent["instance"],
            agent["method"]
        )

        input_type = agent["input_type"]

        start = time.perf_counter()

        success = True
        error = None
        response = None
        input_summary = query

        try:

            # -------------------------------------------------
            # Customer Identifier
            # -------------------------------------------------

            if input_type == self.CUSTOMER_ID_INPUT:

                customer_id = (
                    self.routing_service.extract_customer_id(
                        query
                    )
                )

                if customer_id is None:

                    response = {

                        "success": False,

                        "message": (
                            "No valid customer ID "
                            "was found in the request."
                        ),

                        "customer_profile": None,

                        "assessment": None,

                        "risk_summary": None

                    }

                else:

                    input_summary = customer_id

                    response = handler(
                        customer_id
                    )

            # -------------------------------------------------
            # Natural Language Query
            # -------------------------------------------------

            elif input_type == self.QUERY_INPUT:

                response = handler(
                    query
                )

            # -------------------------------------------------
            # Unsupported Input Type
            # -------------------------------------------------

            else:

                success = False

                response = {

                    "success": False,

                    "message": (
                        f"Unsupported input type: "
                        f"{input_type}"
                    )

                }

        except Exception as ex:

            success = False

            error = str(ex)

            raise

        finally:

            elapsed = (
                time.perf_counter()
                - start
            ) * 1000

            self.execution_logger.log_execution(

                correlation_id=correlation_id,

                agent_name=agent_name,

                input_summary=input_summary,

                response=response,

                execution_time_ms=elapsed,

                success=success,

                error_message=error

            )

        return response

    # ---------------------------------------------------------
    # Response Helpers
    # ---------------------------------------------------------

    def _build_error_response(
        self,
        message: str
    ) -> Dict[str, Any]:
        """
        Build standardized
        error response.
        """

        return {

            "success": False,

            "message": message,

            "agents_invoked": [],

            "responses": {}

        }

    # ---------------------------------------------------------
    # Public Entry Point
    # ---------------------------------------------------------

    def process_query(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Process a user request.
        """
        correlation_id = (
            self.execution_logger
            .create_correlation_id()
        )

        if not query.strip():

            return self._build_error_response(

                "Please provide a valid query."

            )

        start = time.perf_counter()

        success = True
        error = None
        response = self.route_query(
        query=query,
        correlation_id=correlation_id
            )

        return self.response_formatter.format_response(
                response
        )
        

# ---------------------------------------------------------
# Test Harness
# ---------------------------------------------------------

if __name__ == "__main__":

    coordinator = CoordinatorAgent()

    query = (
        "Assess customer "
        "CUST000001 against the "
        "premium credit card policy."
    )

    response = coordinator.process_query(
        query
    )

    from pprint import pprint

    print("\nResponse")
    print("=" * 80)

    pprint(response)
