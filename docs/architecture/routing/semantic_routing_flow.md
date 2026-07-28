# Semantic Routing Flow

## Purpose

This document provides a lightweight view of the semantic routing pipeline.

It explains how a user query flows through the routing components before the
Coordinator Agent invokes one or more specialist agents.

This document is intended as a low-level design reference for developers.

---

## Routing Pipeline

```text
                 User Query
                      │
                      ▼
             CoordinatorAgent
                      │
                      ▼
          IntentRoutingService
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
Normalize Query   Extract Customer ID
                      │
                      ▼
              EmbeddingService
                      │
                      ▼
        IntentEmbeddingService
        (Intent Repository Embeddings)
                      │
                      ▼
            SimilarityService
                      │
                      ▼
        Candidate Agent Selection
                      │
                      ▼
          RoutingPolicyService
        (Business Routing Rules)
                      │
                      ▼
            RoutingDecision
                      │
                      ▼
          CoordinatorAgent
                      │
        ┌─────────────┴──────────────┐──────────────────────────┐
        ▼                            ▼                          ▼
 Policy Agent                 Customer Agent                Portfolio Agent
        │                            │                          │
        └─────────────┬──────────────┘──────────────────────────┘
                      ▼
          Response Formatter
                      │
                      ▼
                User Response
```

---

# Component Responsibilities

| Component | Responsibility |
|----------|----------------|
| CoordinatorAgent | Entry point for all user requests and orchestration of specialist agents |
| IntentRoutingService | Coordinates semantic routing workflow |
| EmbeddingService | Generates embeddings for incoming user queries |
| IntentEmbeddingService | Maintains embeddings for registered agent intent definitions |
| IntentRepository | Stores semantic intent examples for every registered agent |
| SimilarityService | Computes semantic similarity between query embedding and intent embeddings |
| RoutingPolicyService | Applies deterministic business routing policies after semantic routing |
| RoutingDecision | Immutable routing result returned by the routing engine |
| Specialist Agents | Execute domain-specific business logic |

---

# Startup Initialization

Semantic intent embeddings are generated once during application startup.

```text
ApplicationStartup
        │
        ▼
RoutingBootstrap
        │
        ▼
IntentEmbeddingInitializer
        │
        ▼
IntentEmbeddingService.initialize()
```

The generated embeddings are reused throughout the application lifecycle.

---

# Routing Decision Lifecycle

```text
User Query
      │
      ▼
Semantic Similarity
      │
      ▼
Candidate Agents
      │
      ▼
Business Routing Policies
      │
      ▼
Selected Agents
      │
      ▼
Coordinator Invocation
```

---

# Design Principles

- Semantic similarity determines candidate agents.
- Business policies enrich routing decisions without replacing semantic routing.
- Routing components are independent of specialist agents.
- Intent definitions are centrally managed by the Intent Repository.
- Semantic embeddings are initialized once during application startup.
- Routing decisions are immutable and explainable.

---

# Related Components

```
src/
├── initialization/
│   ├── application_startup.py
│   ├── routing_bootstrap.py
│   └── intent_embedding_initializer.py
│
├── repository/
│   └── intent_repository.py
│
├── services/
│   ├── embedding_service.py
│   ├── intent_embedding_service.py
│   ├── similarity_service.py
│   ├── intent_routing_service.py
│   └── routing_policy_service.py
│
├── models/
│   └── routing_models.py
│
└── agents/
    └── coordinator_agent.py
```

---

# Future Evolution

This routing pipeline has been intentionally designed to support additional specialist agents without modifying the semantic routing architecture.

Future agents include:

- Portfolio Agent
- Recommendation Agent
- Explainability Agent

Only the Intent Repository requires additional intent definitions for new routing capabilities.
