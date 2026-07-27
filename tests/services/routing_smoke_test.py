"""
routing_smoke_test.py

Purpose
-------
Validates the complete semantic intent
routing pipeline.

Workflow
--------
1. Load registered intent definitions
2. Generate intent embeddings
3. Execute representative routing queries
4. Apply routing business policies
5. Display routing decisions

Author
------
Credit Risk Research Agent
"""

from typing import List

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
from src.services.intent_routing_service import (
    IntentRoutingService
)


def print_separator():

    print("\n" + "=" * 80)


def execute_query(
    router: IntentRoutingService,
    query: str,
    expected_agents: List[str]
):

    print_separator()

    print(f"Query : {query}")

    decision = router.route_request(
        query
    )

    assert decision.selected_agents, (
        "No agents selected for query."
    )

    print("\nSelected Agents")

    for agent in decision.selected_agents:

        print(f"  ✓ {agent}")

    if decision.customer_id:

        print(
            f"\nCustomer ID : "
            f"{decision.customer_id}"
        )

    print("\nSimilarity Scores")

    for result in decision.similarity_results:

        print(
            f"  {result.agent_name:<18}"
            f"{result.similarity_score:.3f}"
        )

        print(
            f"      ↳ {result.matched_intent}"
        )

    if decision.routing_reasons:

        print("\nRouting Policies Applied")

        for reason in decision.routing_reasons:

            print(f"  • {reason}")

    actual = set(
        decision.selected_agents
    )

    expected = set(
        expected_agents
    )

    if actual != expected:

        raise AssertionError(

            f"\nQuery : {query}\n"

            f"Expected : {expected}\n"

            f"Received : {actual}"

        )

    print("\n✓ Routing validated")


def main():

    print_separator()

    print(
        "SEMANTIC INTENT ROUTING\n"
        "SMOKE TEST"
    )

    print_separator()

    # ---------------------------------------------------------
    # Initialise Components
    # ---------------------------------------------------------

    repository = IntentRepository()

    embedding_service = EmbeddingService()

    intent_embedding_service = (
        IntentEmbeddingService(
            repository=repository,
            embedding_service=embedding_service
        )
    )

    print(
        "\nGenerating intent embeddings..."
    )

    intent_embedding_service.initialize()

    if not intent_embedding_service.is_initialized():

        raise RuntimeError(
            "Intent embeddings failed "
            "to initialize."
        )

    similarity_service = (
        SimilarityService()
    )

    routing_policy_service = (
        RoutingPolicyService()
    )

    router = IntentRoutingService(

        embedding_service=embedding_service,

        intent_embedding_service=
        intent_embedding_service,

        similarity_service=
        similarity_service,

        routing_policy_service=
        routing_policy_service
    )

    # ---------------------------------------------------------
    # Display Registered Intents
    # ---------------------------------------------------------

    print_separator()

    print(
        "Registered Intent Definitions"
    )

    all_embeddings = (
        intent_embedding_service
        .get_all_embeddings()
    )

    if not all_embeddings:

        raise RuntimeError(
            "No intent embeddings "
            "were generated."
        )

    for (

        agent,

        intents

    ) in all_embeddings.items():

        print(
            f"{agent:<18}"
            f"{len(intents)} examples"
        )

    # ---------------------------------------------------------
    # Representative Queries
    # ---------------------------------------------------------

    execute_query(

        router,

        "What is the minimum credit score "
        "required for a premium credit card?",

        ["policy"]

    )

    execute_query(

        router,

        "Assess customer CUST000001",

        ["customer"]

    )

    execute_query(

        router,

        "Can customer CUST000001 "
        "receive a premium credit card?",

        ["policy", "customer"]

    )

    execute_query(

        router,

        "Show portfolio default trends",

        ["portfolio"]

    )

    execute_query(

        router,

        "Recommend whether customer "
        "CUST000001 should be approved.",

        ["customer", "recommendation","policy"]

    )

    print_separator()

    print(
        "Semantic routing smoke test "
        "completed successfully."
    )


if __name__ == "__main__":

    main()