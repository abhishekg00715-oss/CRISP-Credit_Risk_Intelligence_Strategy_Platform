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
- Receive routing decisions
- Invoke specialist agents
- Aggregate responses
- Return standardized orchestration response

Author
------
Credit Risk Research Agent
"""

import time
from typing import Any, Dict

from src.agents.customer_agent import CustomerAgent
from src.agents.policy_agent import PolicyAgent

from src.services.intent_routing_service import (
    IntentRoutingService
)

from src.services.response_formatting_service import (
    ResponseFormattingService
)

from src.logging.query_logger import (
    QueryLogger
)

from src.logging.agent_execution_logger import (
    AgentExecutionLogger
)


class CoordinatorAgent:
    """
    Central orchestration agent.
    """

    QUERY_INPUT = "query"

    CUSTOMER_ID_INPUT = "customer_id"

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------

    def __init__(
        self,
        routing_service: IntentRoutingService
    ) -> None:
        """
        Parameters
        ----------
        routing_service
            Fully initialized routing service
            supplied by ApplicationStartup.
        """

        self.routing_service = routing_service

        self._register_agents()

        self.response_formatter = (
            ResponseFormattingService()
        )

        self.query_logger = (
            QueryLogger()
        )

        self.execution_logger = (
            AgentExecutionLogger()
        )

    # ---------------------------------------------------------
    # Agent Registration
    # ---------------------------------------------------------

    def _register_agents(self) -> None:

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

        routing_decision = (

            self.routing_service.route_request(
                query
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

        if not agent_names:

            return self._build_error_response(

                "Unable to determine the "
                "appropriate agent."

            )

        responses = {}

        for agent_name in agent_names:

            responses[agent_name] = (

                self._invoke_agent(

                    agent_name=agent_name,

                    query=query,

                    correlation_id=correlation_id

                )

            )

        return {

            "success": True,

            "agents_invoked": agent_names,

            "responses": responses,

            "routing": {

                "candidate_agents": (
                    routing_decision.candidate_agents
                ),

                "routing_reasons": (
                    routing_decision.routing_reasons
                ),

                "similarity_results": (
                    routing_decision.similarity_results
                )

            }

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

        agent = self._agents[agent_name]

        handler = getattr(

            agent["instance"],

            agent["method"]

        )

        input_type = (
            agent["input_type"]
        )

        start = time.perf_counter()

        success = True

        error = None

        response = None

        input_summary = query

        try:

            if input_type == self.CUSTOMER_ID_INPUT:

                customer_id = (

                    self.routing_service
                    .extract_customer_id(
                        query
                    )

                )

                if customer_id is None:

                    response = {

                        "success": False,

                        "message": (
                            "No valid customer ID "
                            "was found."
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

            elif input_type == self.QUERY_INPUT:

                response = handler(
                    query
                )

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
    # Helpers
    # ---------------------------------------------------------

    def _build_error_response(
        self,
        message: str
    ) -> Dict[str, Any]:

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

        if not query.strip():

            return self._build_error_response(

                "Please provide a valid query."

            )

        correlation_id = (

            self.execution_logger
            .create_correlation_id()

        )

        orchestration_response = (

            self.route_query(

                query=query,

                correlation_id=correlation_id

            )

        )

        return (

            self.response_formatter
            .format_response(
                orchestration_response
            )

        )


# ---------------------------------------------------------
# Test Harness
# ---------------------------------------------------------

if __name__ == "__main__":

    from src.initialization.application_startup import (
        ApplicationStartup
    )

    startup = ApplicationStartup()

    startup.initialize()

    coordinator = (
        startup.create_coordinator()
    )

    response = coordinator.process_query(

        "Assess customer CUST000001 "
        "against the premium credit "
        "card policy."

    )

    from pprint import pprint

    pprint(response)
