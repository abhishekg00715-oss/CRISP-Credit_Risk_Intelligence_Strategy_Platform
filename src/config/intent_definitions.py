"""
Intent Definitions Configuration

This module contains the semantic intent definitions used by the
Semantic Intent Router.

Each agent registers:
    - agent identifier
    - display name
    - description
    - representative intent examples

The examples are embedded during application startup and reused for
semantic similarity matching.

Author: Abhishek Gupta
Project: Credit Decision Intelligence Platform
"""

from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class AgentIntentDefinition:
    """
    Represents the semantic intent definition for an agent.
    """

    agent_name: str
    display_name: str
    description: str
    intent_examples: List[str]


# ---------------------------------------------------------------------
# Policy Agent
# ---------------------------------------------------------------------

POLICY_AGENT = AgentIntentDefinition(

    agent_name="policy",

    display_name="Policy Agent",

    description=(
        "Answers questions related to lending policies, "
        "underwriting guidelines and eligibility criteria."
    ),

    intent_examples=[

        "What is the minimum credit score?",

        "Show me the premium credit card eligibility.",

        "Explain the lending policy.",

        "What are the underwriting guidelines?",

        "Who is eligible for a platinum card?",

        "What is the income requirement?",

        "What is the debt-to-income threshold?",

        "Summarize the policy.",

        "Explain the approval criteria.",

        "Show policy for premium credit cards.",

        "What are the platinum card requirements?",

        "Premium card policy.",

        "Luxury card eligibility.",

        "Income requirement for platinum cards.",

        "Eligibility criteria for premium products.",

        "Loan approval policy.",

        "Underwriting rules.",

        "Risk acceptance policy.",

        "Credit assessment policy.",

        "Approval guidelines."
    ]
)


# ---------------------------------------------------------------------
# Customer Agent
# ---------------------------------------------------------------------

CUSTOMER_AGENT = AgentIntentDefinition(

    agent_name="customer",

    display_name="Customer Agent",

    description=(
        "Retrieves customer information and performs "
        "customer credit risk assessments."
    ),

    intent_examples=[

        "Assess customer CUST000001.",

        "Retrieve customer profile.",

        "Show customer risk summary.",

        "Evaluate customer credit score.",

        "Show bureau information.",

        "Display customer profile.",

        "Calculate customer risk.",

        "Analyze customer utilisation.",

        "Retrieve customer assessment.",

        "Show customer details.",

        "Can customer CUST000001 qualify?",

        "Is customer CUST000001 eligible for a premium credit card?",

        "Evaluate customer's eligibility.",

        "Assess whether customer qualifies.",

        "Check if this customer meets lending requirements.",

        "Review customer before approval.",

        "Analyze customer's financial profile.",

        "Evaluate customer's repayment capability.",

        "Assess customer's borrowing capacity.",

        "Review customer risk before decision.",

        "Explain customer's credit profile.",

        "Summarize customer risk.",

        "Analyze customer behaviour.",

        "Review customer credit history.",

        "Evaluate customer financial position."
    ]
)


# ---------------------------------------------------------------------
# Future Agent Placeholders
# ---------------------------------------------------------------------

PORTFOLIO_AGENT = AgentIntentDefinition(

    agent_name="portfolio",

    display_name="Portfolio Agent",

    description=(
        "Provides portfolio-level risk analytics and trend analysis."
    ),

    intent_examples=[

        "Show portfolio risk.",

        "Analyze portfolio performance.",

        "Which customer segment is riskiest?",

        "Show portfolio trends.",

        "Portfolio default rates.",

        "Portfolio exposure.",

        "Portfolio concentration.",

        "Delinquency trends.",

        "Default hotspots.",

        "Portfolio health.",

        "Portfolio performance dashboard.",

        "Portfolio risk summary."
    ]
)


RECOMMENDATION_AGENT = AgentIntentDefinition(

    agent_name="recommendation",

    display_name="Recommendation Agent",

    description=(
        "Generates lending recommendations using multiple sources."
    ),

    intent_examples=[

        "Should this customer be approved?",

        "Generate recommendation.",

        "Approve or decline.",

        "Recommend credit decision.",

        "Final lending recommendation.",

        "Should we approve this application?",

        "Would you approve this customer?",

        "Recommend a lending decision.",

        "Provide final recommendation.",

        "Make a credit decision.",

        "Approve or review this applicant."
    ]
)


# ---------------------------------------------------------------------
# Registered Agents
# ---------------------------------------------------------------------

REGISTERED_INTENTS = [

    POLICY_AGENT,

    CUSTOMER_AGENT,

    # Future agents

    PORTFOLIO_AGENT,

    RECOMMENDATION_AGENT
]
