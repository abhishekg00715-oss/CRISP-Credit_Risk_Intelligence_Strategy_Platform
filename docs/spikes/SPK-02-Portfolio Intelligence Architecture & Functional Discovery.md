# Portfolio Intelligence Design
### CRISP – Credit Risk Intelligence & Strategy Platform

| Attribute | Value |
|-----------|-------|
| Phase | Phase 3 – Portfolio Intelligence |
| Spike | SPK-02 – Portfolio Intelligence Architecture & Functional Discovery |
| Status | Draft |
| Purpose | Define the functional and architectural foundation for implementing the Portfolio Intelligence capability. |

---

# 1. Introduction

## 1.1 Purpose

Portfolio Intelligence is a core capability of CRISP that enables portfolio-level credit risk analysis through reusable analytical services and executive-friendly business insights.

Unlike the Customer Agent, which assesses an individual customer, the Portfolio Agent evaluates the overall portfolio by analysing pre-computed analytical datasets representing the portfolio's composition, quality, exposure and performance.

Rather than executing every available analysis, the Portfolio Agent determines the underlying business objective of a portfolio-related query and orchestrates the appropriate analytical capabilities to generate explainable, evidence-based portfolio insights.

The outcome of this spike is to establish the functional scope and architectural direction required to implement the Portfolio Intelligence capability represented by the following product backlog items.

| Backlog ID | Feature |
|------------|---------|
| CRA-12 | Portfolio Repository & Portfolio Data Foundation |
| CRA-13 | Portfolio Analytics Service |
| CRA-14 | Portfolio Summary Service |
| CRA-15 | Portfolio Agent |

This document intentionally focuses on architecture and functional design rather than implementation details and will be progressively elaborated throughout Phase 3.

---

# 2. Portfolio Intelligence Vision

Portfolio Intelligence transforms portfolio-level analytical data into actionable business intelligence for portfolio managers, credit risk analysts and executive stakeholders.

Rather than retrieving operational data or performing transactional calculations, the Portfolio Agent interprets portfolio-related business questions, determines the underlying analytical objective and orchestrates reusable analytical services to answer strategic questions such as:

- How healthy is the current portfolio?
- Where are the major areas of credit risk?
- Which customer segments require attention?
- Where is portfolio exposure concentrated?
- What trends are emerging over time?
- What opportunities exist to improve portfolio performance?

The outcome is an explainable portfolio assessment consisting of business insights, supporting analytical evidence and recommendation candidates that can be further tailored by downstream capabilities.

---

# 3. Design Philosophy

Portfolio Intelligence follows a deterministic analytical execution model.

Natural language portfolio queries are interpreted into **Analytical Business Objectives** using semantic similarity. Each business objective invokes a predefined analytical workflow consisting of one or more analytical capabilities.

This approach ensures that:

- Analytical execution remains deterministic, explainable and testable.
- Business logic is separated from AI-generated narratives.
- Analytical capabilities are reusable across multiple business objectives.
- Large Language Models are used exclusively for explanation and narrative generation, not for determining analytical execution.

The high-level analytical execution flow is illustrated below.

```text
Natural Language Query
        │
        ▼
Analytical Business Objective
        │
        ▼
Analytical Workflow
        │
        ▼
Analytical Capabilities
        │
        ▼
Portfolio Insights
        │
        ▼
Recommendation Candidates
```

---

# 4. Portfolio Analytical Capabilities

Portfolio Intelligence enables portfolio-level analytical decision support by evaluating the overall health, performance and risk profile of the credit portfolio. Rather than focusing on individual customers, it provides strategic insights that support portfolio monitoring, risk management and business decision-making.

The capability is organised into five core analytical domains.

| Capability | Description |
|------------|-------------|
| **Portfolio Health & Performance** | Provides an overall assessment of portfolio quality, performance and operational health. |
| **Portfolio Risk Analysis** | Evaluates portfolio-wide credit risk, exposure and concentration to identify areas requiring attention. |
| **Portfolio Segmentation** | Compares portfolio behaviour across customer, product and geographic dimensions to identify performance variations. |
| **Portfolio Trend Analysis** | Monitors changes in portfolio performance and risk over time to identify emerging patterns and early warning signals. |
| **Portfolio Opportunity Analysis** | Identifies opportunities to optimise portfolio growth while maintaining an acceptable risk profile. |

These capabilities define the functional scope of Portfolio Intelligence. Depending on the analytical business objective identified from a user's query, one or more analytical capabilities may be orchestrated to produce contextual portfolio insights and recommendation candidates.

---

# 5. Illustrative Portfolio Intelligence Outcome

The following example demonstrates the expected analytical lifecycle of a typical portfolio intelligence request.

### Example User Query

> **"How healthy is our current portfolio?"**

### Identified Analytical Business Objective

**Assess Portfolio Health**

### Analytical Capabilities Invoked

- Portfolio Health & Performance
- Portfolio Risk Analysis
- Portfolio Trend Analysis
- Portfolio Exposure Analysis

### Example Portfolio Intelligence Response

> **Portfolio Executive Summary**

```text
──────────────────────────────────────────────────────────────
            PORTFOLIO HEALTH DASHBOARD
──────────────────────────────────────────────────────────────

Portfolio Health            : Healthy

Active Customers            : 100

Total Exposure              : $12.8M

Average Credit Score        : 724

High Risk Customers         : 8%

Average Utilisation         : 41%

Default Rate                : 1.9%

Highest Risk Segment        : Young Professionals

Largest Exposure            : Home Loans

Emerging Trend              : Credit card utilisation
                              increasing over last 3 months

Top Opportunity             : 18 customers eligible for
                              credit limit enhancement

──────────────────────────────────────────────────────────────

Key Insights

✓ Portfolio quality remains stable.

✓ Overall default rate remains within acceptable limits.

✓ Home Loan portfolio contributes the largest exposure.

⚠ Credit card utilisation has increased among younger customers.

⚠ Western Region shows increasing delinquency trend.

★ Opportunity exists to increase credit limits for
  low-risk customers with consistently high repayment behaviour.
```

The Portfolio Agent complements this narrative with appropriate visualisations such as KPI cards, trend charts, risk distributions, concentration charts and segment comparisons to improve business interpretation.

> **Architectural Note**
>
> The Portfolio Agent does not execute every analytical capability for every request. Instead, it identifies the analytical business objective and orchestrates only the analytical capabilities required to satisfy that objective, ensuring focused, explainable and efficient portfolio analysis.

---

# Document Evolution

This document will be progressively elaborated during SPK-02 through the addition of the following sections:

1. Analytical Business Objectives
2. Analytical Workflows
3. Portfolio Analytics Catalogue
4. Portfolio KPI Catalogue
5. Portfolio Analytical Data Foundation
6. Portfolio Response Model
7. Logical Architecture

Each section builds upon the previous one to establish the complete functional and architectural foundation required to implement the Portfolio Intelligence capability within CRISP.
