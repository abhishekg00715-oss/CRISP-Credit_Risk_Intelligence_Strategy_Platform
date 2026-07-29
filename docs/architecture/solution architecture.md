# Solution Architecture

## Overview

CRISP(Credit Risk Intelligence & Strategy Platform) is a modular, local-first Agentic AI platform designed to support credit analysts in researching lending policies, assessing customer creditworthiness, and producing explainable credit risk insights.

The solution follows a layered architecture that separates presentation, orchestration, business capabilities, data access, and infrastructure concerns.

Rather than relying on an external agent framework, the platform implements a lightweight, framework-independent orchestration model that emphasizes modularity, explainability, and extensibility.

The current implementation includes:

- Policy Research (RAG)
- Customer Credit Assessment
- Request Orchestration
- Intent-Based Routing
- Response Formatting
- Query Logging
- Agent Execution Logging

Future phases will introduce portfolio analytics, recommendation generation, and explainability workflows

---

# Architecture Goals

The solution aims to:

- Demonstrate Agentic AI design principles
- Implement Retrieval-Augmented Generation (RAG)
- Showcase Credit Risk domain modelling
- Provide explainable assessments
- Support incremental capability expansion
- Remain framework independent
- Execute entirely on local infrastructure

---

# Architecture Principles

1. Local-first execution
2. Separation of concerns
3. Single Responsibility Principle
4. Service-oriented design
5. Repository pattern
6. Explainability by design
7. Thin orchestration layer
8. Extensible multi-agent architecture
9. Framework independence
10. Evidence-based decision support

---

# Technology Stack

| Layer | Technology |
|---------|-----------|
| UI | Streamlit |
| LLM Access | OpenAI GPT |
| Orchestration | Coordinator Agent |
| RAG Framework | LlamaIndex |
| Embeddings | Sentence Transformers (Local) |
| Vector Store | ChromaDB |
| Structured Data | SQLite |
| Portfolio Data | CSV / SQLite |
| Configuration | YAML / ENV |
| Logging | JSON based |
| Programming Language | Python |

---

# High-Level Architecture

```
                                User
                                  │
                                  ▼
                           Streamlit UI
                                  │
                                  ▼
                         Coordinator Agent
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
            Intent Routing Service      Query Logger
                    │
        ┌───────────┴───────────────┐
        ▼                           ▼
   Policy Agent                Customer Agent
        │                           │
        ▼                           ▼
 Retrieval Service         Customer Repository
        │                           │
        ▼                           ▼
   LLM Service        Customer Assessment Service
                                    │
                                    ▼
                      Customer Summary Service
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
         Agent Execution Logger     Response Formatting Service
                                                │
                                                ▼
                                          Final Response

```

---
#  Layered Architecture  

## Presentation Layer

**Component:**

- Streamlit UI

**Responsibilities:**

- Accept user requests
- Display formatted responses
- Present expandable customer information
- Display supporting evidence
- Maintain session history

------

## Orchestration Layer

**Component:**

- Coordinator Agent

**Responsibilities:**

- Receive requests
- Invoke Intent Routing Service
- Coordinate specialist agents
- Aggregate responses
- Invoke Response Formatting Service
- Record logging events

The Coordinator intentionally contains no business logic.

-------

## Business Capability Layer

Current specialist agents:

## Policy Agent

**Responsibilities:**

- Policy retrieval
- Context generation
- Prompt construction
- Policy answer generation

**Internal Services:**

- RetrievalService
- LLMService

---------

## Customer Agent

**Responsibilities:**

- Customer validation
- Customer retrieval
- Credit assessment
- Executive summary generation

**Internal Components:**

- CustomerRepository
- CustomerAssessmentService
- CustomerSummaryService

--------

# Infrastructure Services

## Intent Routing Service

**Responsible for:**

- Request normalization
- Customer ID extraction
- Intent detection
- Agent selection

**Current implementation:**

- Deterministic keyword routing

**Future evolution:**

- SLM-powered semantic intent classification (to be explored)
- Confidence scoring
- Dynamic routing

--------

## Response Formatting Service

**Responsible for:**

- Formatting Policy responses
- Formatting Customer responses
- Formatting composite responses
- Decoupling presentation from orchestration

---------

## Query Logger

**Responsible for recording:**

 Timestamp
- Query
- Customer ID
- Invoked agents

----------

## Agent Execution Logger

**Responsible for recording:**

- Correlation ID
- Agent name
- Execution duration
- Success/failure
- Response summary
- Error information

-------------

# Data Architecture

## Unstructured Data

**Policy Documents**

Format
- PDF

Storage
- docs/policies/

Purpose

- Knowledge source for Retrieval-Augmented Generation
------------

## Vector Store

**Technology**

- ChromaDB

**Purpose**

- Embedding storage
- Semantic similarity search
- Context retrieval
--------------

## Structured Data

**Technology**

- SQLite

**Database**

- src/database/customer_risk.db

**Contains**

- Customer Master
- Credit Bureau
- Credit Cards
- Loan Accounts
- Transactions
- Digital Behaviour

---------

## Analytical Data 

**Technology**

- CSV
- SQLite

**Purpose**

- Portfolio analytics
- Segment benchmarking
- Trend analysis

---------

## Current Capability Map

|Capability|	Status|
|--------|------|
|Policy Research	|✅ Complete|
|Customer Assessment	|✅ Complete|
|Request Orchestration	|✅ Complete|
|Intent Routing	|✅ Initial Implementation|
|Response Formatting	|✅ Complete|
|Query Logging	|✅ Complete|
|Agent Execution Logging|	✅ Complete|
|Portfolio Analytics|	Planned|
|Recommendation Engine|	Planned|
|Explainability Workflow|	Planned|

----------
# Deployment Model

**Current deployment target**

- Developer Workstation

**Minimum Requirements**

- Python 3.12+
- 8 GB RAM
- Internet Access (OpenAI API)

The architecture remains cloud-independent and is designed for local execution throughout development.

--------------

# Architectural Evolution
## Phase 1
**Policy Agent**
- Retrieval-Augmented Generation
- Streamlit UI
---------
## Phase 2
**Customer Agent**
- SQLite Repository
- Customer Assessment Service
- Customer Summary Service
- Coordinator Orchestration
- Intent Routing Service
- Response Formatting Service
- Query Logging
- Agent Execution Logging
- Planned Future Evolution
----------

## Phase 3
**Portfolio Agent**
- Portfolio Repository
- Portfolio Analytics Services
--------
## Phase 4
**Recommendation Agent**
- Credit Decision Engine

---------

## Phase 5
**Explainability Agent**

- Multi-Agent Workflow
- Evidence Aggregation
----------

## Future agents may include:

- Regulatory Agent : Monitors and interprets regulatory guidelines to identify impacts on credit risk policies and decision-making.
- Fraud Risk Agent : Detects suspicious customer behaviors and potential fraud indicators during credit assessment.
- Market Intelligence Agent : Analyzes macroeconomic, industry, and market trends that may influence portfolio risk and lending strategies.
- Collections Agent : Evaluates delinquent accounts and recommends collection, recovery, or customer engagement actions.


--------------
## Future Enhancements
  
- Intelligent SLM-based Intent Classification
- Agent Registry Configuration
- Dynamic Agent Discovery
- Agent Memory
- Workflow Engine
- Execution Dashboard
- Performance Monitoring
- Policy Evaluation Service

-------------------
# Architectural Characteristics

The solution is intentionally designed to demonstrate production-quality software engineering practices alongside Agentic AI concepts.

Key characteristics include:

- Thin orchestration layer
- Independent specialist agents
- Service-based business logic
- Repository-based data access
- Framework-independent architecture
- Explainability-first design
- Observable execution through structured logging
- Extensible capability-driven architecture
