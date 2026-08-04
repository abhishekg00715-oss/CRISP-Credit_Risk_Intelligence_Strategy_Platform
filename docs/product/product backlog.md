# Product Backlog 

## Epic: Policy Research Assistant

| ID | Feature / User Story | Priority |
|----|----------------------|----------|
| CRA-1 | Upload and ingest policy PDFs | Must |
| CRA-2 | Extract text and chunk documents | Must |
| CRA-3 | Generate embeddings for document chunks | Must |
| CRA-4 | Store embeddings in ChromaDB / FAISS | Must |
| CRA-5 | Implement semantic search over policies | Must |
| CRA-6 | Generate RAG-based answers with citations | Must |

---

## Epic: Customer Risk Assessment

| ID | Feature / User Story | Priority |
|----|----------------------|----------|
| CRA-7 | Customer Data Foundation (SQLite) | Must |
| CRA-8 | Implement customer lookup by customer_id | Must |
| CRA-9 | Calculate credit score assessment | Should |
| CRA-10 | Analyze income and credit utilization | Should |
| CRA-11 | Generate customer risk summary | Should |

---

## Epic: Portfolio Intelligence

| ID | Feature / User Story | Priority |
|----|----------------------|----------|
| CRA-12 | Implement Portfolio Repository and portfolio data foundation | Must |
| CRA-13 | Implement Portfolio Analytics Service(Portfolio KPIs, Segment Analysis, Risk Distribution,Exposure Analysis, Concentration Analysis,Default Analysis, Risk Trend Analysis,Portfolio Health Metrics) | Must |
| CRA-14 | Implement Portfolio Summary Service for executive and analyst-friendly portfolio insights| Should |
| CRA-15 | Implement Portfolio Agent | Must |

---

## Epic: Recommendation Engine

| ID | Feature / User Story | Priority |
|----|----------------------|----------|
| CRA-16 | Implement rule evaluation engine | Should |
| CRA-17 | Calculate risk score | Should |
| CRA-18 | Generate recommendation (Approve / Decline / Review) | Should |
| CRA-19 | Generate recommendation rationale | Should |

---

## Epic: Explainability & Governance

| ID | Feature / User Story | Priority |
|----|----------------------|----------|
| CRA-20 | Attach policy citations to responses | Must |
| CRA-21 | Collect supporting evidence from all agents | Should |
| CRA-22 | Generate confidence score | Could |
| CRA-23 | Persist decision trace / audit trail | Could |

---

## Epic: Multi-Agent Orchestration

| ID | Feature / User Story | Priority |
|----|----------------------|----------|
| CRA-24 | Implement Coordinator Agent | Must |
| CRA-25 | Integrate Policy Agent with Coordinator Agent | Must |
| CRA-26 | Integrate Customer Agent with Coordinator Agent| Must |
| CRA-27 | Integrate Portfolio Agent with Coordinator Agent | Must |
| CRA-28 | Integrate Recommendation Agent with Coordinator Agent | Must |
| CRA-29 | Implement Explainability Agent | Should |
| CRA-30 | Create end-to-end credit assessment workflow | Should |

---

## Epic: User Experience & Demo

| ID | Feature / User Story | Priority |
|----|----------------------|----------|
| CRA-31 | Build Streamlit UI for Policy Research | Must |
| CRA-32 | Build Streamlit UI for Customer Assessment | Should |
| CRA-33 | Build Streamlit UI for Portfolio Analysis | Should |
| CRA-34 | Add sample queries and demo scenarios | Must |
| CRA-35 | Capture screenshots and walkthroughs for README | Should |
|CRA-36| Format and Enhance composite reponses from multiple agents |Must|
|CRA-37| Implement semantic intent routing using the selected approach |Must|
|CRA-38| Implement reusable Intent Repository for semantic routing |Should|
|CRA-39| Build routing evaluation framework (confidence scoring, fallback logic and routing accuracy tests) |Should|

---


# Phasewise allocation plan of Backlog items


---------------------
# MVP Scope (Release 1.0)

The following backlog items constitute the Minimum Viable Product:

| ID | Feature | status |
|----|---------|--------|
| CRA-1 | Upload and ingest policy PDFs | **Done** |
| CRA-2 | Extract text and chunk documents |**Done**|
| CRA-3 | Generate embeddings |**Done**|
| CRA-4 | Store embeddings |**Done**|
| CRA-5 | Semantic search |**Done**|
| CRA-6 | RAG-based answers with citations |**Done**|
| CRA-20 | Attach policy citations to responses |**Done**|
| CRA-24 | Implement Coordinator Agent  |**Done**|
| CRA-25 | Integrate Policy Agent with Coordinator Agent |**Done**|
| CRA-31 | Build Streamlit UI for Policy Research |**Done**|
| CRA-34 | Add Sample queries and demo scenarios |**Done**|

| ID | NFR | status |
|----|---------|--------|
| NFR-5 | Responses must be generated using retrieved context whenever available |**Done**|
| NFR-6 | Policy-related responses should reference source documents|**Done**|
| NFR-7 | Hallucinated policy rules should be minimized through retrieval-augmented generation (RAG)|**Done**|
| NFR-9 | All policy answers must include source citations | **Done** |
| NFR-17 | Agents must follow single-responsibility principles | **Done** |
| NFR-18 | Business logic should be separated from UI logic | **Done** |
| NFR-19 | Shared services should be reusable across agents |**Done** |
| NFR-21 | New agents should be pluggable into the Coordinator Agent | **Done** |



---


---
# Phase 2 Backlog 

| ID | Feature | status |
|----|---------|--------|
| CRA-7 | Customer Data Foundation (SQLite) | **Done** |
| CRA-8 | Implement customer lookup by customer_id | **Done** |
| CRA-9 | Calculate credit score assessment | **Done** |
| CRA-10 | Analyze income and credit utilization | **Done** |
| CRA-11 | Generate customer risk summary | **Done** |
| CRA-26 | Integrate Customer Agent with Coordinator Agent | **Done** |
|CRA-36 | Format and Enhance composite reponses from multiple agents | **Done**|



| ID | NFR | status |
|----|---------|--------|
| NFR-2 | Customer profile retrieval time | **Done** (Under 3 seconds)|
|NFR-10| Customer assessments shall include supporting rationale.|**Done**|
|NFR-11| Evidence used to generate customer assessments shall be visible to users.|***Done**|
|NFR-13| User questions should be logged.| **Done**|
|NFR-14| Agent responses should be logged.| **Done**|


------------------------------------

# Phase 3 Backlog

| ID | Feature | Associated Features| status |
|----|---------|--------|------|
| SPK-01 | Assess intelligent intent routing approaches (keyword, embedding, ML, SLM/LLM, hybrid) and recommend the preferred architecture |CRA-37, CRA-38, CRA-39| **Done** |
| CRA-37 | Implement semantic intent routing using the selected approach | | **Done** |
| CRA-38 | Implement reusable Intent Repository for semantic routing | |  **Done** |
| CRA-39 | Build routing evaluation framework (confidence scoring, fallback logic and routing accuracy tests) | |  **Done**  |
| SPK-02 | Define the Portfolio Intelligence capability, analytics catalogue, business scenarios, data model and implementation roadmap | CRA-12, CRA-13, CRA-14, CRA-15, CRA-27, CRA-33| **Done** |
| CRA-12 | Implement Portfolio Repository and portfolio data foundation | | **Done**  |
| CRA-13 | Implement Portfolio Analytics Service (portfolio KPIs, segment analysis, risk distribution, exposure analysis) |  | **To Do**  |
| CRA-14 | Implement Portfolio Summary Service for executive and analyst-friendly portfolio insights |  | **To Do**  |
| CRA-15 | Implement Portfolio Agent |  | **To Do**  |
| CRA-27 | Integrate Portfolio Agent with Coordinator Agent|  | **To Do**  |
| CRA-33 | Build Streamlit UI for Portfolio Intelligence |  | **To Do**  |





