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

The outcome of this spike is to establish the functional scope and architectural direction required to implement the Portfolio Intelligence capability represented by the following product backlog items.

| Backlog ID | Feature |
|------------|---------|
| CRA-12 | Portfolio Repository & Portfolio Data Foundation |
| CRA-13 | Portfolio Analytics Service |
| CRA-14 | Portfolio Summary Service |
| CRA-15 | Portfolio Agent |

This document intentionally focuses on architecture and functional design rather than implementation details.

---

# 2. Portfolio Intelligence Vision

The Portfolio Intelligence capability transforms portfolio-level analytical data into actionable business intelligence for portfolio managers, credit risk analysts and executive stakeholders.

Rather than retrieving operational data or performing transactional calculations, Portfolio Intelligence consumes reusable analytical services to answer strategic business questions such as:

- How healthy is the current portfolio?
- Where are the major areas of credit risk?
- Which customer segments require attention?
- Where is portfolio exposure concentrated?
- What trends are emerging over time?
- What opportunities exist to improve portfolio performance?

The Portfolio Agent interprets these analytical results and produces concise business narratives supported by visual evidence.

---

# 3. Portfolio Analytical Capabilities

Portfolio Intelligence is organised around five core analytical capabilities.

| Capability | Objective |
|------------|-----------|
| Portfolio Health & Performance | Assess the overall quality and performance of the portfolio. |
| Portfolio Risk Analysis | Evaluate portfolio-wide credit risk, concentration and exposure. |
| Portfolio Segmentation | Compare portfolio performance across customer, product and geographic dimensions. |
| Portfolio Trend Analysis | Monitor portfolio behaviour over time and identify emerging patterns. |
| Portfolio Opportunity Analysis | Identify opportunities to optimise portfolio growth while maintaining acceptable risk. |

These capabilities collectively provide the analytical foundation for executive reporting, portfolio monitoring and strategic decision support.

---

# 4. Illustrative Portfolio Intelligence Outcome

The following example illustrates the type of outcome expected from the Portfolio Intelligence capability.

> **Portfolio Executive Summary**

```
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

The Portfolio Agent complements this narrative with appropriate visualisations such as KPI cards, trend charts, distribution charts and segment comparisons to support business interpretation.

---

## Document Evolution

This document will be progressively elaborated during SPK-02 as the following areas are defined:

- Portfolio Analytics Catalogue
- Portfolio KPI Catalogue
- Portfolio Analytical Data Foundation
- Logical Architecture
- Portfolio Agent Design
