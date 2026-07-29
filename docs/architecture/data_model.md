
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
| Portfolio Data        | Portfolio performance and risk trends        | Portfolio Agent                        |
| Decision Intelligence | Recommendations, evidence, and explanations  | Recommendation & Explainability Agents |

---

## Core Business Entities

```text
Policy Document
    └── Policy Rule

Customer
    └── Credit Profile

Portfolio
    └── Segment Metrics

Assessment
    ├── Recommendation
    └── Evidence
```

---

## Entity Summary

| Entity          | Description                                               |
| --------------- | --------------------------------------------------------- |
| Policy Document | Lending policies and underwriting guidelines              |
| Policy Rule     | Eligibility and credit risk rules extracted from policies |
| Customer        | Customer demographic and financial information            |
| Credit Profile  | Credit score, utilization, and repayment indicators       |
| Portfolio       | Historical portfolio performance metrics                  |
| Assessment      | Credit evaluation outcome                                 |
| Evidence        | Supporting information used in recommendations            |

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
    └── Segment Metrics
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

### Portfolio Repository

| Component         | Technology   |
| ----------------- | ------------ |
| Portfolio Metrics | CSV / SQLite |

**Storage Location**

```text
data/portfolio/
```

---

## Data Ownership

| Agent                | Data Owned                   |
| -------------------- | ---------------------------- |
| Policy Agent         | Policy Documents, Embeddings |
| Customer Agent       | Customer Profiles            |
| Portfolio Agent      | Portfolio Metrics            |
| Recommendation Agent | Assessments, Risk Scores     |
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

### Portfolio Analysis

```text
Portfolio Dataset
 ↓
Trend Analysis
 ↓
Risk Insights
```

---

## Data Design Principles

1. Separate structured and unstructured data.
2. Maintain explainable evidence for all recommendations.
3. Use synthetic data for demonstrations and testing.
4. Prefer local storage over cloud dependencies.
5. Support future agent expansion without major redesign.
