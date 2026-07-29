# CRISP (Credit Risk Intelligence & Strategy Platform)

An AI-powered, local-first, multi-agent decision support platform that demonstrates how Agentic AI, Retrieval-Augmented Generation (RAG), semantic search, and explainable AI can be applied to enterprise Credit Risk decision support.

The solution enables credit analysts and underwriters to interpret lending policies, assess customer creditworthiness, and generate evidence-based decisions through collaboration between specialized AI agents.

The project has been intentionally designed as a portfolio solution to demonstrate modern AI solution architecture, software engineering principles, and credit risk domain expertise.

---

# Business Problem

Credit Risk teams rely on multiple sources of information before making lending decisions, including:

- Credit policies
- Underwriting guidelines
- Customer credit bureau information
- Income and repayment behaviour
- Portfolio performance
- Regulatory requirements

Analysts often spend considerable time navigating these sources, resulting in:

- Slow decision making
- Inconsistent policy interpretation
- Manual evidence gathering
- Limited explainability
- High onboarding effort for new analysts

CRISP (Credit Risk Intelligence & Strategy Platform) addresses these challenges by combining Retrieval-Augmented Generation (RAG) with specialized AI agents that retrieve, analyze and explain credit risk information.

---

# Current Solution Capabilities

## Phase 1 – Policy Intelligence (Completed)

- PDF Policy Ingestion Pipeline
- Intelligent Document Chunking
- Local Embedding Generation
- ChromaDB Vector Database
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Policy Agent
- Coordinator Agent
- Streamlit User Interface
- Policy Source Attribution
- Explainable Policy Responses

---

## Phase 2 – Customer Risk Assessment (Completed)

Phase 2 extends the platform beyond document intelligence by introducing structured customer assessment capabilities.

Implemented features include:

- SQLite Customer Repository
- Synthetic Customer Data Generation
- Customer Repository Pattern
- Customer Agent
- Customer Assessment Service
- Customer Risk Summary Service
- Business Rule Engine
- Customer Lookup
- Credit Score Assessment
- Credit Utilization Analysis
- Debt-to-Income Analysis
- Executive Risk Summary Generation
- Policy + Customer Multi-Agent Orchestration
- Response Formatting Service
- Query Logging
- Agent Execution Logging
- Explainable Customer Assessments

---

# High-Level Architecture



<img width="1536" height="1024" alt="Architecture Jul 19, 2026, 03_35_46 PM" src="https://github.com/user-attachments/assets/5e9d9711-2318-4b66-864f-c82d3937e0db" />


**Current AI Orchestration Layer**

- Coordinator Agent
- Policy Agent
- Customer Agent

The architecture has been intentionally designed to support additional specialist agents without modifying existing business logic.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python |
| User Interface | Streamlit |
| Agent Orchestration | Custom Coordinator Agent |
| LLM | OpenAI GPT |
| Embeddings | Sentence Transformers (Local) |
| Vector Database | ChromaDB |
| RAG Framework | LlamaIndex |
| Structured Data | SQLite |
| Configuration | Python Configuration Modules |
| Logging | JSON-based Custom Logging |
| Development Environment | GitHub Codespaces |

---

# Current Architecture

```text
                    User
                      │
                      ▼
               Streamlit UI
                      │
                      ▼
             Coordinator Agent
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼

   Policy Agent              Customer Agent
        │                           │
        ▼                           ▼

 Retrieval Service        Customer Repository
        │                           │
        ▼                           ▼

     ChromaDB                  SQLite Database
        │
        ▼

     OpenAI GPT

                      │
                      ▼

      Response Formatting Service
                      │
                      ▼

              Explainable Response
```

---

# Key Architectural Principles

The solution follows a number of core architectural principles:

- Local-first execution
- Modular multi-agent architecture
- Single Responsibility Principle
- Separation of concerns
- Repository Pattern
- Explainability by design
- Evidence-based decision support
- Extensible agent ecosystem
- Framework independence (no LangChain/CrewAI dependency)
- Configuration-driven behaviour

---

# Current End-to-End Workflow

The current solution supports multiple user journeys.

## Policy Research Workflow

1. User submits a policy question.
2. Coordinator Agent identifies policy intent.
3. Policy Agent performs semantic retrieval.
4. Relevant policy sections are retrieved from ChromaDB.
5. OpenAI GPT generates a grounded response.
6. Source citations are included.
7. Response is presented through the Streamlit UI.

---

## Customer Assessment Workflow

1. User requests assessment of a customer.
2. Coordinator Agent extracts the customer identifier.
3. Customer Agent retrieves customer information.
4. Customer Assessment Service evaluates customer risk.
5. Customer Summary Service generates an executive summary.
6. Response Formatting Service prepares a presentation-friendly output.
7. Final explainable assessment is presented to the user.

---

## Multi-Agent Workflow

For requests requiring both policy interpretation and customer assessment:

1. Coordinator Agent identifies multiple required capabilities.
2. Policy Agent retrieves relevant lending policy.
3. Customer Agent evaluates customer profile.
4. Responses are consolidated.
5. Evidence-based assessment is presented through a unified response.

---

# Explainability

A key objective of the solution is transparency.

Every customer assessment includes:

- Executive summary
- Risk classification
- Key strengths
- Risk factors
- Supporting evidence
- Business observations
- Policy citations (where applicable)

This ensures AI-generated responses remain interpretable and suitable for analyst review.

---

# Non-Functional Capabilities

The platform currently includes:

- Modular service architecture
- Explainable AI responses
- Query execution logging
- Agent execution logging
- Structured response formatting
- Local embedding generation
- Framework-independent design
- Extensible configuration model

---

# Repository Structure

```text
src/
│
├── agents/
├── services/
├── repository/
├── database/
├── ingestion/
├── logging/
├── config/
├── UI/
└── tests/
```

---
# Intelligence Domain Overview 

|Intelligence Domain |	Agents |
|--------------|-------------|
|Knowledge Intelligence |	Policy, Regulatory |
|Customer Intelligence |	Customer Assessment, Opportunity Intelligence, Fraud |
|Portfolio Intelligence |	Portfolio Analytics, Collections |
|Decision Intelligence |	Recommendation, Policy Decision Engine, Business Rules Engine|
|Strategic Intelligence	|Market Intelligence, Executive Dashboard, Predictive Analytics |



----
# Project Roadmap

The project is being developed incrementally through capability-driven phases.

## ✅ Phase 1 — Policy Intelligence

Completed

- Policy Agent
- RAG Pipeline
- Semantic Search
- Coordinator Agent
- Streamlit UI

---

## ✅ Phase 2 — Customer Risk Assessment

Completed

- Customer Agent
- Customer Assessment
- Business Rule Engine
- Response Formatting
- Logging
- Multi-Agent Coordination

---

## 🚧 Phase 3 — Intelligent Portfolio Assessment (In Progress)

Phase 3 focuses on two major architectural enhancements.

### Intelligent Agent Routing

Replace keyword-based routing with semantic intent classification using local embedding models.

Planned capabilities include:

- Embedding-based Intent Classification
- Hybrid Routing Strategy
- Routing Confidence Scoring
- Intelligent Coordinator Routing

---

### Portfolio Intelligence

Introduce portfolio-level risk analytics.

Planned capabilities include:

- Portfolio Repository
- Portfolio Agent
- Portfolio Assessment Service
- Portfolio Summary Service
- Portfolio Risk Insights
- Portfolio Benchmarking

---

## Future Enhancements

Additional enhancements currently under evaluation include:

- Agent Memory
- Multi-session Conversation Context
- Human-in-the-loop Review
- Decision Trace Visualization
- Regulatory Agent
- Fraud Risk Agent
- Market Intelligence Agent
- Collections Agent
- Recommendation Agent
- Explainability Agent
- Cloud Deployment Architecture
- CI/CD Pipeline

---

# Design Decisions

Some key architectural decisions made during development include:

- Local embedding generation to minimize operational cost.
- OpenAI GPT is used only for reasoning and answer generation.
- ChromaDB provides lightweight embedded vector storage.
- SQLite provides structured customer data storage.
- Specialized agents own individual business capabilities.
- Coordinator Agent contains orchestration only.
- Business logic remains isolated within domain services.
- Explainability is treated as a first-class architectural concern.
- Response formatting is separated from business processing.
- Logging is designed for traceability and future observability.

---

# How to Run

## Prerequisites

- Python 3.11+
- OpenAI API Key
- Git

---

## One-Time Setup

1. Clone the repository.

```bash
git clone <repository-url>
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Configure environment variables.

Create a `.env` file in the project root and configure your OpenAI API key.

```text
OPENAI_API_KEY=<your-api-key>
```

---


4. Build the Policy Knowledge Base

Run the ingestion pipeline to prepare the policy document repository.

1. Extract text from policy PDFs
2. Generate semantic chunks
3. Create local embeddings
4. Build the ChromaDB vector database

> This step only needs to be repeated when policy documents are added or modified.

---

5. Create the Customer Repository

Generate the synthetic customer repository and initialize the SQLite database.

The pipeline performs the following activities:

- Generate synthetic customer master data
- Generate bureau records
- Generate credit card accounts
- Generate loan accounts
- Generate transaction history
- Generate digital behaviour history
- Export intermediate CSV datasets
- Validate generated datasets
- Create the SQLite database
- Load all generated data into SQLite

> This step only needs to be repeated when regenerating the synthetic customer dataset.

----



## Launch the Application

Once the one-time setup is complete-

```bash
streamlit run src/UI/app.py
```

The Streamlit interface allows you to:

- Ask policy-related questions
- Assess customer credit risk
- Evaluate customers against lending policies
- View explainable policy evidence
- Review customer risk summaries

---

# Project Status

| Phase | Status |
|---------|--------|
| Phase 1 – Policy Intelligence | ✅ Completed |
| Phase 2 – Customer Risk Assessment | ✅ Completed |
| Phase 3 – Intelligent Portfolio Assessment | 🚧 In Progress |

---

# Documentation

Additional project documentation is available under the `docs/` directory, including:

- Vision
- Product Roadmap
- Capability Map
- Solution Architecture
- Agent Design
- Data Model
- Sequence Flows
- Future Enhancements
- Product Backlogs

---

**CRISP (Credit Risk Intelligence & Strategy Platform)** demonstrates how modern Agentic AI architectures can combine Retrieval-Augmented Generation, semantic search, structured analytics, and explainable AI into a modular decision support platform for enterprise credit risk management.


