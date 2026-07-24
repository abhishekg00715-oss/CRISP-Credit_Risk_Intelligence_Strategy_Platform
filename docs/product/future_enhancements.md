
As we explore more about the Agentic AI capabilities and current Business landscape , there are many possibilities that can be 
explored,analyzed for feasibility and added into the future phases. A set of such capabilities are captured in the backlog below:

## Future Enhancements Backlog

| ID | Enhancement | Description | Category | Business Value | Complexity | Related Capability | Status |
|----|-------------|-------------|----------|----------------|------------|--------------------|--------|
| **FE-01** | Agent Memory | Enable persistent memory so agents can retain user preferences, previous interactions, and intermediate reasoning across conversations, improving continuity and personalization. | Candidate | High | High | Multi-Agent Platform | Deferred |
| **FE-02** | LangGraph / CrewAI Integration | Evaluate orchestration frameworks to simplify agent workflows, state management, and execution while preserving the existing framework-independent architecture. | Exploratory | Low | Medium | Multi-Agent Platform | Deferred |
| **FE-03** | Multi-session Conversation Context | Allow users to resume previous conversations by maintaining conversational context across multiple sessions for long-running analytical workflows. | Candidate | Medium | Medium | User Experience | Future Release |
| **FE-04** | Human-in-the-loop Review | Introduce configurable approval workflows where analysts can review, override, or approve AI-generated recommendations before final decisions are made. | Candidate | High | Medium | Governance & Explainability | Future Release |
| **FE-05** | Decision Trace Visualization | Provide interactive visualization of multi-agent execution flow, reasoning paths, supporting evidence, and decision lineage to improve transparency and auditability. | Candidate | Very High | Medium | Explainability | Future Release |
| **FE-06** | Intelligent Intent Classification & Routing | Replace deterministic keyword routing with semantic intent classification using embedding-based similarity or an equivalent intelligent routing mechanism to improve scalability and routing accuracy. | Candidate | Very High | Medium | Coordinator Agent | **Planned – Phase 3** |
| **FE-07** | Policy Decision Engine | Introduce a configurable decision engine that evaluates customer assessments against organizational policies to determine eligibility, compliance, and decision outcomes consistently. | Candidate | Very High | High | Recommendation Engine | Future Release |
| **FE-08** | Regulatory Intelligence Agent | Introduce a specialized agent capable of interpreting regulatory publications, monitoring compliance changes, and assessing their impact on lending policies and credit decisions. | Strategic | Very High | High | Regulatory Intelligence | Future Release |
| **FE-09** | Fraud Risk Agent | Introduce a dedicated fraud assessment agent that evaluates fraud indicators, behavioural anomalies, and suspicious activities to complement customer credit risk assessments. | Strategic | Very High | High | Fraud Risk Assessment | Future Release |
| **FE-10** | Market Intelligence Agent | Develop an agent that monitors macroeconomic indicators, industry trends, and market conditions to provide external context for portfolio and lending decisions. | Strategic | High | High | Market Intelligence | Future Release |
| **FE-11** | Collections Intelligence Agent | Develop an agent that identifies early delinquency signals, predicts collection priorities, and recommends optimized recovery strategies for overdue accounts. | Strategic | High | Medium | Collections & Recovery | Future Release |
| **FE-12** | Enhanced Analyst Dashboard | Redesign the Streamlit interface into a modern analyst dashboard with intuitive navigation, rich visualizations, interactive portfolio views, and improved usability. | Strategic | Medium | High | User Experience | Deferred |
| **FE-13** | Pluggable Enterprise Data Connectors | Extend the customer data ingestion layer to support configurable enterprise data sources such as SQLite, Amazon S3, Snowflake, Amazon Redshift, and other repositories through a common connector interface. | Strategic | High | High | Data Integration | Future Release |
| **FE-14** | Predictive Customer Opportunity Intelligence | Extend the platform beyond credit risk assessment by incorporating predictive models to identify profitable customers for cross-selling, upselling, and next-best-product recommendations. | Strategic | Very High | High | Customer Intelligence | Future Release |
| **FE-15** | Configurable Business Rules Engine | Externalize credit assessment rules, thresholds, and decision policies into configurable rule definitions or decision tables, enabling business users to modify rules without code changes. | Candidate | High | High | Decision Management | Future Release |

-----------------------------------------


# Requirements Analysis & Detailed assessment

## FE-01 — Agent Memory

**Business Value: High**

**Enablement of Memory capability for the agentic solution will provide:

- follow-up questions
- reduced repeated inputs
- richer customer conversations
- persistent analyst sessions

Example:

*Assess customer CUST000001*

...

*Now compare with last customer.*

...

*What was their utilization?*


**Complexity: High**

Following factors justify the complexity level:

- memory architecture
- session management
- context pruning
- retrieval strategy
- It also impacts almost every agent.

## Recommendation & Direction:

**Move until after multi-agent workflows exist.**

---------

## FE-02 — LangGraph / CrewAI Integration

**Business Value: Low**

Today the architecture already supports:

- orchestration
- routing
- modular agents

Adding LangGraph would mainly replace infrastructure that is already built.
Little new business capability.


**Complexity: Medium**

Migration & Introduction of the new framework would require the following:

- redesigning Coordinator
- changing execution model
- introducing framework dependency

## Recommendation & Direction:

Trea & Keep as an architecture experiment only.Not to be considered in future roadmap plan.

-----------------------


## FE-03 — Multi-session Conversation Context

**Business Value: Medium**

Enabling this capability would allow the agentic framework:

- Recall the converstation past conversationa and build context from it.
- Useful,Not essential.

**Complexity: Medium**

Enabling the capability would require the following:

- conversation persistence
- retrieval
- session management

## Recommendation & Direction:

Possible implemantion to be planned after Agent Memory.

---------------

## FE-04 — Human-in-the-loop Review

**Business Value: High**

Folloiwing would be achieved with the capability:

- Very valuable & effective  for credit decisions.
- Example:Recommendation -> Analyst Review -> Approve -> Store Decision
- Much closer to enterprise lending systems.
- Reduces risk concerns & brings transparency around whole process


**Complexity: Medium**

- Mostly UI and workflow related impact.
- minimal impact on existing agents.

## Recommendation & Direction
To be planned in future Phases as capacity is available.

-----------------

## FE-05 — Decision Trace Visualization

**Business Value: High**

Following are to be considered :

- Financial institutions care enormously about explainability.
- Builds credebility of the outcomes reached.
- Helps in monitoring and reviewing the decisions.

**Complexity:Medium**

- Almost everything already exists.
- Visualization work needs to be finished.

## Recommendation & Direction
To be plannned for the future phases as the capacity becomes available.

------------------------

## FE-06 — Intelligent Intent Classification & Routing

**Business Value: Very High**

Following considerations are associated with the capability:

- substatially reduces the dependency on dictionaries (No dictionary in a sense)
- Keyword maintencence overhead is removed completely.
- Better improved composite routing.
- Highly scalable as the solution grows with more agents.

**Complexity: Medium**

- Routing service already functioning as a separate component.
- Only a single component change required. Minimal impact to current solution.

## Recommendation & Direction
To be planned & prioritized as in the current Roadmap to reap benefits as early as possible.

---------------------

## FE-07 — Policy Decision Engine

**Concept**

The Policy Decision Engine is a deterministic business rule evaluation component responsible for translating organizational credit policies into executable decision logic.

Rather than relying on an LLM to determine approval outcomes, the engine evaluates structured customer assessment data against configurable policy rules to produce consistent, explainable, and auditable lending decisions.

The engine acts as the business decision layer between analytical agents (Policy, Customer, Portfolio) and the Recommendation Agent.

**Inputs**

The engine consumes structured outputs generated by multiple agents and supporting repositories.

- ***Customer Assessment***
- ***Policy Findings***
- ***Portfolio Insights***
- ***Product Information***


**Responsibilities**

The Policy Decision Engine will:

- Evaluate customer eligibility against policy rules.
- Execute configurable business decision logic.
- Detect policy violations.
- Identify mandatory approval or rejection conditions.
- Apply rule precedence and conflict resolution.
- Produce standardized decision outcomes.
- Capture supporting evidence for each decision.
- Maintain complete auditability of evaluated rules.
- Support future configurable rule repositories.

Importantly, the engine performs deterministic evaluation rather than AI reasoning.

**Typical Output**

JSON based structured output containing fields like decision,decision reason, policy compliance, rules evaluated, confidence etc.
The structured JSON is then formatted with more human readable version.

**Business Value:Very High**

The Policy Decision Engine delivers significant business benefits by ensuring that lending decisions are consistent, transparent, and policy-compliant.

- Improved regulatory compliance and audit readiness.
- Clear separation between analytical insights and business decisions.
- Explainable decision outcomes supported by evaluated rules.
- Easier maintenance through configurable policy rules.
- Reduced dependence on LLM reasoning for high-stakes decisions.

**Complexity:High**

Major complexity drivers include:

- Designing a configurable rule execution framework.
- Supporting rule precedence and dependency management.
- Handling conflicting or overlapping policy conditions.
- Maintaining backward compatibility as policies evolve.
- Providing comprehensive audit trails and rule traceability.
- Integrating outputs from multiple specialist agents.
- Preparing for future externalization of rules into configuration or rule repositories.




