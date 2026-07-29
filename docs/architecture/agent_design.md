# Agent Design

## Overview

The CRISP(Credit Risk Intelligence & Strategy Platform) follows a modular, multi-agent architecture where each specialist agent owns a single business capability. A lightweight Coordinator Agent orchestrates interactions between agents while keeping business logic isolated within individual components.

The current implementation follows these architectural principles:

- Single Responsibility Principle
- Separation of Concerns
- Repository Pattern
- Service-Oriented Design
- Explainability by Design
- Framework Independence
- Local-First Execution
- Extensibility

---

# Current Architecture (Phase 2)

```text
                                User
                                  │
                                  ▼
                        Coordinator Agent
                                  │
                 Intent Routing Service
                                  │
            ┌─────────────────────┴─────────────────────┐
            ▼                                           ▼

      Policy Agent                              Customer Agent
            │                                           │
            ▼                                           ▼
   Retrieval Service                         Customer Repository
            │                                           │
            ▼                                           ▼
       LLM Service                      Customer Assessment Service
                                                        │
                                                        ▼
                                            Customer Summary Service
                                  └─────────────────────┬─────────────────────┘
                                                        ▼
                                         Response Formatting Service
                                                        │
                                                        ▼
                                                Final Response
```

---

# Agent Responsibilities

## Coordinator Agent

### Purpose

Acts as the central orchestration layer for all user requests.

### Responsibilities

- Receive user requests
- Determine required business capabilities
- Route requests using the Intent Routing Service
- Invoke specialist agents
- Coordinate agent execution
- Aggregate responses
- Invoke Response Formatting Service
- Return standardized responses
- Log user queries
- Log agent execution metrics

### Internal Services

- IntentRoutingService
- ResponseFormattingService
- QueryLogger
- AgentExecutionLogger

### Does NOT

- Execute business rules
- Access databases
- Query policy documents
- Generate recommendations

---

# Policy Agent

## Purpose

Provide policy research capabilities using Retrieval-Augmented Generation (RAG).

### Responsibilities

- Retrieve relevant policy documents
- Build retrieval context
- Construct LLM prompts
- Generate policy answers
- Cite supporting policy sources

### Internal Components

- RetrievalService
- LLMService

### Inputs

- Natural language policy question

### Outputs

- Policy answer
- Supporting citations

### Data Sources

- Credit Policy PDFs
- Chroma Vector Database

---

# Customer Agent

## Purpose

Provide customer-level credit risk assessment.

### Responsibilities

- Validate customer identifiers
- Retrieve customer profile
- Assess customer credit risk
- Generate executive risk summary
- Return standardized customer response

### Internal Components

- CustomerRepository
- CustomerAssessmentService
- CustomerSummaryService

### Inputs

- Customer Identifier

### Outputs

- Customer Profile
- Credit Assessment
- Risk Summary

### Data Sources

- SQLite Customer Database

---

# Response Formatting Service

## Purpose

Convert raw orchestration responses into presentation-ready outputs.

### Responsibilities

- Format policy responses
- Format customer responses
- Format combined responses
- Preserve standardized response contracts
- Separate presentation from orchestration

---

# Intent Routing Service

## Purpose

Determine which specialist agents should process a user request.

### Current Implementation

Deterministic keyword and pattern matching.

### Responsibilities

- Normalize requests
- Detect policy intent
- Detect customer intent
- Extract customer identifiers
- Return target agents

### Future Evolution

Replace deterministic routing with an intelligent SLM-based intent classification engine capable of:

- Semantic intent detection
- Confidence scoring
- Multi-intent decomposition
- Dynamic routing

---

# Logging Components

## Query Logger

Responsible for recording user requests.

### Captures

- Timestamp
- User Query
- Invoked Agents
- Customer Identifier (if applicable)

---

## Agent Execution Logger

Responsible for execution observability.

### Captures

- Correlation ID
- Agent Name
- Execution Duration
- Success / Failure
- Response Summary
- Error Details

---

## Portfolio Agent

### Purpose

Generate portfolio-level credit risk insights.

### Planned Responsibilities

- Portfolio segmentation
- Default trend analysis
- Exposure analysis
- Risk concentration analysis
- Benchmarking

---

## Recommendation Agent

### Purpose

Generate consolidated lending recommendations using outputs from specialist agents.

### Planned Inputs

- Policy Findings
- Customer Assessment
- Portfolio Insights

### Planned Outputs

- Approve
- Decline
- Review

---

## Explainability Agent

### Purpose

Provide transparent justification for generated recommendations.

### Planned Responsibilities

- Aggregate evidence
- Produce decision rationale
- Generate confidence scores
- Present explainable outputs

---

# Agent Interaction Matrix

| Component | Consumes | Produces |
|------------|----------|-----------|
| Coordinator Agent | User Request | Orchestrated Response |
| Intent Routing Service | User Request | Target Agents |
| Policy Agent | Policy Question | Policy Findings |
| Customer Agent | Customer ID | Customer Assessment |
| Response Formatting Service | Agent Responses | Presentation Response |
| Query Logger | User Request | Query Audit Log |
| Agent Execution Logger | Agent Execution | Execution Audit Log |
| Portfolio Agent *(Future)* | Portfolio Data | Portfolio Insights |
| Recommendation Agent *(Future)* | Agent Findings | Lending Recommendation |
| Explainability Agent *(Future)* | Recommendation | Explainable Decision |

---

# Design Principles

1. Every agent owns a single business capability.
2. The Coordinator remains orchestration-focused and contains no business logic.
3. Agents communicate only through the Coordinator Agent.
4. Business logic is encapsulated within services.
5. Data access is isolated through repositories.
6. Presentation logic is isolated from orchestration.
7. All recommendations must be evidence-based and explainable.
8. The architecture remains framework-independent.
9. New agents can be added without modifying existing specialist agents.
10. The system is designed for local-first execution with future extensibility toward intelligent orchestration.
