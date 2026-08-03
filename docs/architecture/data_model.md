
# Data Model

## Overview

The CRISP (Credit Risk Intelligence & Strategy Platform) combines unstructured policy documents, structured customer data, portfolio datasets, and generated decision intelligence to support policy research, credit risk assessment, and recommendation generation.

The solution follows a local-first architecture using PDFs, ChromaDB, SQLite, and CSV files.

---

## Data Domains

| Domain                | Purpose                                      | Agent                                  |
| --------------------- | -------------------------------------------- | -------------------------------------- |
| Policy Knowledge      | Credit policies and underwriting rules       | Policy Agent                           |
| Customer Data         | Customer credit profiles and risk indicators | Customer Agent                         |
| Portfolio Intelligence| Portfolio-level analytical datasets, KPIs and derived metrics| Portfolio Agent        |
| Decision Intelligence | Recommendations, evidence, and explanations  | Recommendation & Explainability Agents |

---

## Core Business Entities

```text
Policy Document
    └── Policy Rule

Customer
    └── Credit Profile

Portfolio
    ├── Portfolio Summary
    ├── Portfolio Risk
    ├── Portfolio Exposure
    ├── Portfolio Segmentation
    ├── Portfolio Trends
    └── Portfolio Opportunities

Assessment
    ├── Recommendation
    └── Evidence
```

---

## Entity Summary

| Entity | Description |
|---------|-------------|
| Policy Document | Lending policies and underwriting guidelines |
| Policy Rule | Eligibility and credit risk rules extracted from policies |
| Customer | Customer demographic and financial information |
| Credit Profile | Credit score, utilisation and repayment indicators |
| Portfolio | Logical representation of the overall credit portfolio |
| Portfolio Summary | Aggregated portfolio health and performance measures |
| Portfolio Risk | Portfolio-wide credit risk indicators |
| Portfolio Exposure | Portfolio exposure and concentration metrics |
| Portfolio Segmentation | Comparative analytics across business dimensions |
| Portfolio Trends | Historical portfolio performance indicators |
| Portfolio Opportunities | Derived portfolio growth and optimisation indicators |
| Assessment | Credit evaluation outcome |
| Evidence | Supporting information used in recommendations |

---

## Key Relationships

```text
Policy Document
    └── Policy Rules

Customer
    └── Credit Profile

Customer
    └── Assessments

Assessment
    └── Evidence

Portfolio
    ├── Portfolio Summary
    ├── Portfolio Risk
    ├── Portfolio Exposure
    ├── Portfolio Segmentation
    ├── Portfolio Trends
    └── Portfolio Opportunities
```

---

## Physical Data Model

### Policy Knowledge Store

| Component        | Technology        |
| ---------------- | ----------------- |
| Policy Documents | PDF               |
| Embeddings       | OpenAI Embeddings |
| Vector Store     | ChromaDB          |

**Storage Locations**

```text
docs/policies/
data/vector_store/chroma_db/
```

---

### Customer  Data Repository

| Repository Artifact     | Implementation |
| ------------- | ---------- |
| Database Technology | SQLite     |
| Database File | src/database/customer_risk.db     |
| Database Schema | shema.py |
| Database Utility | database_utils.py    |
| Data Loader | database_loader.py     |
| Data Generator Pipeline | customer_data_generator/ |

**Database Tables**


|Table	|Purpose |
|-------|--------|
|customer_master|	Customer demographic and relationship information|
|credit_bureau|	Credit bureau profile, score, utilization, DTI and repayment history|
|credit_card_accounts|	Customer credit card portfolio and utilization details|
|loan_accounts|	Loan portfolio including EMI, outstanding balance and tenure|
|transactions|	Customer banking transaction history|
|digital_behavior|	Digital banking login and behavioural activity|

---

### Portfolio Analytical Repository

| Repository Artifact | Implementation |
|---------------------|----------------|
| Database Technology | SQLite |
| Database File | src/database/portfolio_analytics.db |
| Repository | PortfolioRepository |
| Data Generator Pipeline | portfolio_data_generator/ |
| Data Source | Customer Operational Repository |

**Analytical Datasets**

| Dataset | Purpose |
|---------|---------|
| Portfolio Summary | Portfolio health and performance metrics |
| Portfolio Risk | Portfolio-wide risk measures |
| Portfolio Exposure | Exposure and concentration metrics |
| Portfolio Segmentation | Customer, product and geographic analytics |
| Portfolio Trends | Historical portfolio analytics |
| Portfolio Opportunities | Portfolio optimisation indicators |

```

---

## Data Ownership

| Agent                | Data Owned                   |
| -------------------- | ---------------------------- |
| Policy Agent         | Policy Documents, Embeddings |
| Customer Agent       | Customer Profiles            |
| Portfolio Agent      | Portfolio Analytical Datasets|
| Recommendation Agent | Recommendations, Recommendation Context|
| Explainability Agent | Evidence, Citations          |

---

## Data Lifecycle

### Policy Research

```text
PDF
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Semantic Search
```

### Customer Assessment

```text
Customer Data
 ↓
SQLite
 ↓
Risk Assessment
 ↓
Recommendation
```

### Portfolio Intelligence

```text
Customer Operational Repository
 ↓
Portfolio Data Generator
 ↓
Portfolio Analytical Repository
 ↓
Portfolio Analytics
 ↓
Portfolio Summary
```
---

## Data Design Principles

1. Separate operational, analytical and unstructured data.
2. Maintain explainable evidence for all analytical outcomes and recommendations.
3. Store derived portfolio analytics separately from transactional customer data.
4. Prefer local storage over cloud dependencies.
5. Support modular agent expansion without major redesign.
