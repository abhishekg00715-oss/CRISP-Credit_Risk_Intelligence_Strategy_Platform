# P3-S1 Spike – Intelligent Intent Routing Assessment

## Objective

Evaluate alternative approaches for intelligent intent classification and recommend the most suitable routing mechanism for the Credit Decision Intelligence Platform.

The selected solution should:

- Improve routing accuracy over deterministic keyword matching.
- Remain fully local and framework-independent.
- Reuse existing project components wherever possible.
- Scale seamlessly as additional agents are introduced.
- Preserve the modular architecture established in Phases 1 and 2.

---

# Current State

The current Coordinator Agent relies on **deterministic keyword-based routing** to identify which specialized agent(s) should process a user request.

This approach has served the initial MVP well, enabling integration of the Policy Agent and Customer Agent with minimal complexity.

### Current Routing Flow

```text
User Query
      │
      ▼
Coordinator Agent
      │
      ▼
Keyword Matching
      │
      ▼
Policy Agent / Customer Agent
```

### Strengths

- Simple implementation
- Easy to understand and debug
- No model inference required
- Low runtime overhead

### Limitations

- Requires continual maintenance as new intents are introduced.
- Difficult to support natural language variations.
- Cannot understand semantic similarity between different expressions.
- Scalability decreases as additional agents are added.
- Multiple keyword rules can overlap, increasing routing complexity.

---

# Existing AI Infrastructure

During **Phase 1**, the project introduced an **Embedding Service** for semantic document retrieval.

The implementation uses the **SentenceTransformer** framework to generate vector embeddings for policy document chunks, enabling semantic search within the RAG pipeline.

The current embedding infrastructure already provides:

- Local embedding generation
- Reusable Embedding Service
- Cosine similarity-based semantic search
- Framework-independent implementation

This existing capability presents an opportunity to reuse the same architectural pattern for intent classification, minimizing additional implementation effort.

---

# Solution Options Considered

| Option | Advantages | Limitations |
|---------|------------|-------------|
| **Keyword Rules** | Simple, fast and explainable | Poor scalability and limited semantic understanding |
| **Embedding-based Semantic Routing** | Understands intent semantically, reusable infrastructure, local execution | Requires similarity threshold tuning |
| **SLM-based Classification** | Better contextual understanding | Higher implementation complexity and model management |
| **LLM-based Classification** | Excellent reasoning capability | Higher latency, resource intensive and less deterministic |
| **Hybrid (Embeddings + Rules)** | Balances semantic understanding with deterministic overrides | Slightly increased implementation complexity |

---

# Evaluation Summary

The candidate approaches were evaluated against the architectural principles established for this project.

| Evaluation Criteria | Keyword | Embeddings | SLM | LLM | Hybrid |
|---------------------|:-------:|:----------:|:---:|:---:|:------:|
| Routing Accuracy | Medium | High | High | Very High | Very High |
| Local-first Execution | Excellent | Excellent | Excellent | Medium | Excellent |
| Explainability | High | High | Medium | Low | High |
| Scalability | Low | High | High | High | High |
| Reuse Existing Infrastructure | Low | Excellent | Medium | Low | High |
| Framework Independence | Excellent | Excellent | Excellent | Medium | Excellent |
| Implementation Complexity | Low | Medium | High | High | Medium |

---

# Recommendation

The spike recommends adopting **Embedding-based Semantic Intent Routing** as the preferred implementation approach.

This approach best aligns with the project's architectural principles by:

- Reusing the existing embedding infrastructure introduced in Phase 1.
- Improving routing accuracy through semantic understanding rather than keyword matching.
- Supporting local-first execution without reliance on external AI services.
- Maintaining framework independence.
- Scaling naturally as new specialized agents are introduced.

The existing keyword router may be retained as a lightweight fallback mechanism during the migration period.

---

# Proposed Architecture

```text
                User Query
                     │
                     ▼
            Embedding Service
       (SentenceTransformer)
                     │
                     ▼
           Query Embedding Vector
                     │
                     ▼
            Cosine Similarity Search
                     │
                     ▼
             Intent Repository
                     │
                     ▼
          Selected Agent(s)
                     │
                     ▼
            Coordinator Agent
```

---

# Implementation Approach

The implementation will introduce a semantic routing layer while preserving the existing Coordinator architecture.

Key implementation activities include:

- Select and standardize the embedding model for intent routing.
- Create an Intent Repository containing representative intent examples for each specialized agent.
- Generate embeddings for all registered intents.
- Compare user query embeddings against stored intent embeddings using cosine similarity.
- Route requests to the most relevant agent(s) based on configurable confidence thresholds.
- Retain keyword-based routing as a fallback where appropriate.

The implementation will remain modular, allowing future agents to register new intents without changes to the routing algorithm.

---

# Outcome

## Decision

**Selected Approach:** Embedding-based Semantic Intent Routing

## Expected Benefits

- Improved intent recognition accuracy.
- Reduced dependence on manually maintained keyword lists.
- Better support for natural language queries.
- Reuse of the existing Embedding Service from Phase 1.
- Improved scalability for future multi-agent expansion.

## Follow-on Backlog

The completion of this spike enables the following implementation stories:

- **CRA-37** – Implement Semantic Intent Routing.
- **CRA-38** – Implement Intent Repository.
- **CRA-39** – Implement Routing Evaluation Framework.

---

## Spike Exit Criteria

- ✅ Alternative routing approaches evaluated.
- ✅ Preferred routing architecture identified.
- ✅ Existing embedding infrastructure assessed for reuse.
- ✅ High-level implementation approach defined.
- ✅ Phase 3 implementation backlog validated.
