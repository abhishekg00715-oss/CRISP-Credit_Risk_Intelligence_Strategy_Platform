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

# 6. Portfolio Analytical Business Objectives

Portfolio Intelligence supports multiple business objectives, each representing a distinct portfolio analysis scenario. After the Coordinator routes a request to the Portfolio Agent, the agent identifies the most appropriate business objective using semantic similarity.

Each business objective defines **what business question is being answered**. The analytical workflow, required analytical capabilities and supporting KPIs are derived deterministically from the selected business objective.

This approach ensures that portfolio analysis remains consistent, explainable and reusable while allowing users to interact using natural language.

| Business Objective | Business Purpose | Example User Queries |
|--------------------|------------------|----------------------|
| **Assess Portfolio Health** | Evaluate the overall health and quality of the portfolio. | "How healthy is our portfolio?", "Give me a portfolio health summary." |
| **Assess Portfolio Risk** | Analyse the overall credit risk profile and identify areas of concern. | "Where are the biggest portfolio risks?", "Show the highest risk areas." |
| **Assess Portfolio Exposure** | Understand credit exposure and concentration across the portfolio. | "Where is our exposure concentrated?", "Which products carry the highest exposure?" |
| **Assess Segment Performance** | Compare portfolio performance across customer, product or geographic segments. | "How are premium customers performing?", "Compare portfolio performance by region." |
| **Assess Portfolio Trends** | Evaluate changes in portfolio performance and risk over time. | "How has the portfolio changed this quarter?", "Show utilisation trends." |
| **Identify Portfolio Opportunities** | Identify opportunities for portfolio optimisation and business growth while maintaining acceptable risk. | "Which customers qualify for higher limits?", "Where are the portfolio growth opportunities?" |

> **Design Principle**
>
> Portfolio Business Objectives are the orchestration layer of Portfolio Intelligence. They bridge natural language business questions and deterministic analytical execution, ensuring that similar business questions consistently produce the same analytical workflow regardless of how the question is phrased.


# 7. Portfolio Analytical Workflows

## Purpose

Each Portfolio Analytical Business Objective is realised through a predefined analytical workflow.

An analytical workflow defines the sequence of analytical capabilities required to satisfy a particular business objective. Rather than dynamically determining which analytics to execute, the Portfolio Agent invokes the workflow associated with the identified business objective.

This approach ensures that portfolio analysis remains deterministic, reusable and explainable while providing consistent outcomes for semantically similar business questions.

---

## Workflow Design Principles

Each analytical workflow:

- Is associated with a single Portfolio Analytical Business Objective.
- Invokes one or more analytical capabilities in a predefined sequence.
- Produces consistent analytical outputs for similar business questions.
- Can be reused across multiple user queries.
- Forms the basis for portfolio summaries and recommendation candidates.

---

## Portfolio Analytical Workflow Catalogue

| Business Objective | Analytical Workflow |
|--------------------|---------------------|
| Assess Portfolio Health | Portfolio Health Workflow |
| Assess Portfolio Risk | Portfolio Risk Workflow |
| Assess Portfolio Exposure | Portfolio Exposure Workflow |
| Assess Segment Performance | Portfolio Segmentation Workflow |
| Assess Portfolio Trends | Portfolio Trend Analysis Workflow |
| Identify Portfolio Opportunities | Portfolio Opportunity Workflow |

---

## Conceptual Execution Flow

```text
User Query
      │
      ▼
Portfolio Agent
      │
      ▼
Identify Business Objective
      │
      ▼
Select Analytical Workflow
      │
      ▼
Execute Analytical Capabilities
      │
      ▼
Generate Portfolio Insights
      │
      ▼
Recommendation Candidates
```

The analytical workflows described in this section establish the orchestration layer of Portfolio Intelligence. The following section defines the analytical capabilities that comprise each workflow.

-----

# 8. Portfolio Analytics Catalogue

The Portfolio Analytics Catalogue defines the reusable analytical capabilities available within the Portfolio Analytics Service.

Each analytical capability performs a specific portfolio analysis and can be reused across multiple analytical workflows. This modular approach promotes consistency, reusability and independent evolution of analytical services while maintaining deterministic analytical execution.

---

## Portfolio Analytics Catalogue

| Analytical Capability | Business Purpose | Typical Outputs | Consumed By |
|------------------------|------------------|-----------------|-------------|
| **Portfolio Health Analytics** | Assess the overall health and quality of the portfolio. | Portfolio health indicators, quality assessment | Portfolio Health Workflow |
| **Portfolio Performance Analytics** | Evaluate overall portfolio performance across key business measures. | Performance indicators, portfolio summary metrics | Portfolio Health Workflow |
| **Portfolio Risk Analytics** | Analyse portfolio-wide credit risk characteristics. | Risk profile, risk distribution, high-risk segments | Portfolio Health Workflow, Portfolio Risk Workflow |
| **Portfolio Exposure Analytics** | Assess portfolio exposure and concentration. | Exposure distribution, concentration analysis | Portfolio Health Workflow, Portfolio Exposure Workflow |
| **Portfolio Segmentation Analytics** | Compare portfolio performance across customer, product and geographic dimensions. | Segment comparisons, segment rankings | Portfolio Segmentation Workflow, Portfolio Opportunity Workflow |
| **Portfolio Trend Analytics** | Analyse changes in portfolio behaviour over time. | Trend indicators, performance movement, risk trends | Portfolio Health Workflow, Portfolio Trend Workflow |
| **Portfolio Opportunity Analytics** | Identify opportunities to optimise portfolio growth while maintaining acceptable risk. | Opportunity candidates, growth segments | Portfolio Opportunity Workflow |

---

## Design Principles

The Portfolio Analytics Catalogue follows the following principles:

- Each analytical capability has a single analytical responsibility.
- Analytical capabilities are reusable across multiple business objectives and workflows.
- Analytical capabilities remain independent of presentation, visualisation and narrative generation.
- Analytical capabilities produce structured analytical outputs that can be consumed by the Portfolio Summary Service and Recommendation Agent.
- New analytical capabilities can be introduced without impacting existing workflows, provided they conform to the established analytical execution model.

The subsequent section defines the Key Performance Indicators (KPIs) and business measures produced by these analytical capabilities.
---------

# 9. Portfolio KPI Catalogue

The Portfolio KPI Catalogue defines the key business measures produced by each analytical capability. These KPIs provide the quantitative foundation for portfolio assessments, executive summaries and recommendation generation.

The KPI catalogue is organised by analytical capability to maintain clear traceability between analytical execution and business outcomes.

---

## Portfolio KPI Catalogue

| Analytical Capability | Key Performance Indicators (KPIs) |
|------------------------|-----------------------------------|
| **Portfolio Health Analytics** | Portfolio Health Score, Active Customers, Portfolio Quality Index, Average Credit Score |
| **Portfolio Performance Analytics** | Total Portfolio Value, Total Credit Exposure, Average Credit Utilisation, Portfolio Growth Rate |
| **Portfolio Risk Analytics** | High-Risk Customer %, Delinquency Rate, Default Rate, Average Risk Score |
| **Portfolio Exposure Analytics** | Total Exposure, Exposure by Product, Exposure by Region, Concentration Ratio |
| **Portfolio Segmentation Analytics** | Customers by Segment, Segment Performance Score, Segment Risk Distribution, Segment Exposure |
| **Portfolio Trend Analytics** | Credit Score Trend, Utilisation Trend, Delinquency Trend, Portfolio Growth Trend |
| **Portfolio Opportunity Analytics** | Eligible Upgrade Customers, Cross-Sell Opportunities, Credit Limit Increase Candidates, Low-Risk Growth Opportunities |

---

## Design Principles

The Portfolio KPI Catalogue follows the following principles:

- KPIs represent business measures rather than implementation-specific calculations.
- Each KPI is owned by a single analytical capability.
- KPIs may be reused across multiple analytical workflows through their associated analytical capability.
- KPI calculations are derived from the Portfolio Analytical Data Foundation and remain independent of presentation or visualisation.
- Additional KPIs can be introduced without impacting the overall analytical architecture.

The next section defines the Portfolio Analytical Data Foundation that provides the derived metrics, analytical views and business dimensions required to compute these KPIs.

-------

# 10. Portfolio Analytical Data Foundation

The Portfolio Analytical Data Foundation provides the analytically prepared datasets required to support Portfolio Intelligence.

Unlike the operational customer repository, which stores transactional customer information, the analytical data foundation contains pre-computed portfolio metrics, derived measures and analytical views that enable efficient portfolio analysis without performing complex calculations during query execution.

---

## Design Principles

The Portfolio Analytical Data Foundation follows the following principles:

- Stores analytical data rather than operational transactions.
- Contains derived metrics prepared for analytical consumption.
- Optimised for read-heavy analytical workloads.
- Supports reusable analytical capabilities and KPI generation.
- Provides a consistent analytical view across all portfolio workflows.

---

## Analytical Data Components

| Analytical Component | Purpose |
|----------------------|---------|
| **Portfolio Summary View** | Provides portfolio-level aggregated metrics and health indicators. |
| **Portfolio Risk View** | Stores portfolio-wide risk distributions and default-related measures. |
| **Portfolio Exposure View** | Maintains aggregated exposure and concentration metrics across the portfolio. |
| **Portfolio Segmentation View** | Provides customer, product and geographic segmentation metrics. |
| **Portfolio Trend View** | Stores time-series analytical measures for trend and behavioural analysis. |
| **Portfolio Opportunity View** | Contains derived opportunity indicators supporting portfolio optimisation and growth analysis. |

---

## Common Business Dimensions

Portfolio analytics are organised using a consistent set of business dimensions to enable comparative and multidimensional analysis.

| Business Dimension | Purpose |
|--------------------|---------|
| Customer Segment | Compare analytical outcomes across customer groups. |
| Product | Analyse portfolio performance by lending product. |
| Geography | Evaluate regional portfolio performance and risk. |
| Risk Rating | Compare analytical measures across portfolio risk categories. |
| Time | Support trend analysis and period comparisons. |

---

## Architectural Significance

The Portfolio Analytical Data Foundation serves as the analytical backbone of Portfolio Intelligence.

It decouples analytical computation from portfolio query execution by providing reusable, analytically ready datasets that support Portfolio Analytics Services, KPI generation and executive portfolio reporting.

The subsequent sections define the Portfolio Response Model and the logical architecture that orchestrates these analytical components.

-----------

# 11. Portfolio Response Model

The Portfolio Response Model defines the standard output produced by the Portfolio Agent following the execution of a portfolio analytical workflow.

The response is designed to support two distinct consumers:

- Business users requiring concise portfolio insights.
- Downstream agents, particularly the Recommendation Agent, requiring structured analytical evidence for recommendation generation.

The response model separates analytical computation from business interpretation and recommendation generation, ensuring each capability within CRISP maintains a single responsibility.

---

## Response Structure

| Response Component | Purpose | Primary Consumer |
|--------------------|---------|------------------|
| **Business Objective** | Identifies the analytical objective satisfied by the Portfolio Agent. | Recommendation Agent, Audit |
| **Portfolio Summary** | Executive summary describing the overall portfolio assessment. | Business User |
| **Portfolio KPIs** | Key business measures supporting the assessment. | Business User, Recommendation Agent |
| **Business Insights** | Human-readable interpretation of the analytical results. | Business User |
| **Business Findings** | Significant positive observations, risks and opportunities identified during analysis. | Recommendation Agent |
| **Supporting Visualisations** | Charts and dashboards supporting interpretation of portfolio performance. | Business User |
| **Recommendation Context** | Structured analytical evidence used by the Recommendation Agent to generate contextual recommendations. | Recommendation Agent |

---

## Conceptual Response Model

```text
Portfolio Business Objective
            │
            ▼
Portfolio Summary
            │
            ▼
Portfolio KPIs
            │
            ▼
Business Insights
            │
            ▼
Business Findings
            │
            ▼
Recommendation Context
```

---

## Recommendation Context

Rather than producing recommendations directly, the Portfolio Agent provides a structured recommendation context describing the analytical outcome.

Typical recommendation context includes:

- Overall portfolio assessment
- Areas requiring management attention
- Emerging portfolio risks
- Portfolio optimisation opportunities
- Supporting business evidence
- Confidence in analytical findings

This enables the Recommendation Agent to generate recommendations that are contextual, explainable and aligned with the user's original business objective.

---

## Design Principles

The Portfolio Response Model follows the following principles:

- Maintain clear separation between analytics and recommendations.
- Produce structured outputs suitable for both human and machine consumption.
- Provide sufficient analytical evidence to support explainable recommendations.
- Ensure consistency across all portfolio analytical workflows.
- Remain extensible to support future analytical capabilities without changing the response contract.


------------
