"""
routing_test_cases.py

Purpose
-------
Provides the canonical routing benchmark dataset
used for validating semantic intent routing.

Responsibilities
----------------
- Define representative routing scenarios
- Specify expected specialist agents
- Support routing regression testing

Notes
-----
This module contains only test data.

It intentionally contains no routing logic,
evaluation logic or assertions.

Author
------
Credit Risk Research Agent
"""

from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------
# Test Case Model
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RoutingTestCase:
    """
    Represents a routing validation scenario.
    """

    name: str

    query: str

    expected_agents: List[str]

    description: str = ""


# ---------------------------------------------------------------------
# Canonical Routing Dataset
# ---------------------------------------------------------------------

ROUTING_TEST_CASES = [

    RoutingTestCase(

        name="Policy Query",

        query=(
            "What is the minimum credit score "
            "required for a premium credit card?"
        ),

        expected_agents=[
            "policy"
        ],

        description=(
            "Pure lending policy enquiry."
        )

    ),

    RoutingTestCase(

        name="Customer Assessment",

        query=(
            "Assess customer CUST000001"
        ),

        expected_agents=[
            "customer"
        ],

        description=(
            "Customer-specific credit assessment."
        )

    ),

    RoutingTestCase(

        name="Eligibility Assessment",

        query=(
            "Can customer CUST000001 "
            "receive a premium credit card?"
        ),

        expected_agents=[
            "customer",
            "policy"
        ],

        description=(
            "Requires both customer assessment "
            "and policy eligibility evaluation."
        )

    ),

    RoutingTestCase(

        name="Portfolio Analytics",

        query=(
            "Show portfolio default trends"
        ),

        expected_agents=[
            "portfolio"
        ],

        description=(
            "Portfolio-level analytics request."
        )

    ),

    RoutingTestCase(

        name="Recommendation",

        query=(
            "Recommend whether customer "
            "CUST000001 should be approved."
        ),

        expected_agents=[
            "recommendation",
            "customer",
            "policy"
        ],

        description=(
            "End-to-end lending recommendation."
        )

    )

]
