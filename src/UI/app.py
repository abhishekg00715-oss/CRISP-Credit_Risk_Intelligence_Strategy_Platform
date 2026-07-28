"""
app.py

Purpose:
Streamlit user interface for the
Credit Risk Research Agent MVP.

Author:
Credit Risk Research Agent
"""
import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

print(PROJECT_ROOT)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.agents.coordinator_agent import (CoordinatorAgent)
from src.initialization.application_startup import (ApplicationStartup)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Credit Risk Research Agent",
    page_icon="📊",
    initial_sidebar_state="expanded",
    layout="wide"
)

# --------------------------------------------------
# Sidebar Configuration
# --------------------------------------------------

with st.sidebar:

    st.title("Navigation")

    st.markdown("---")

    st.markdown("### Project")

    st.write("Credit Risk Research Agent")

    st.markdown("---")

    st.markdown("### Status")

    st.success("Coordinator Agent Ready")

    st.success("Policy Agent Ready")

    st.success("Customer Agent Ready")

    st.success("Vector Database Connected")

    st.success("LLM Connected")

    st.markdown("---")

    st.markdown("### Version")

    st.write("MVP 1.0")

if "history" not in st.session_state:

    st.session_state.history = []


# --------------------------------------------------
# Coordinator Initialization
# --------------------------------------------------

@st.cache_resource
def load_coordinator():

    startup = (
        ApplicationStartup()
        .initialize()
    )

    return startup.coordinator

# --------------------------------------------------
# Response Renderer
# --------------------------------------------------

def render_response(
    response
):
    """
    Render formatted response.
    """

    if not response["success"]:

        st.error(
            response["message"]
        )

        return

    st.markdown(
        f"## {response['title']}"
    )

    for section in response["sections"]:

        st.subheader(
            section["heading"]
        )

        # --------------------------------------------------
        # Policy / Text Sections
        # --------------------------------------------------

        if section["type"] == "text":

            st.markdown(
                section["content"]
            )

        # --------------------------------------------------
        # Customer Assessment Section
        # --------------------------------------------------

        elif section["type"] == "customer":

            customer = section["content"]

            st.success(
                customer["message"]
            )

            risk_summary = customer["risk_summary"]

            # ----------------------------------------------
            # Overall Risk
            # ----------------------------------------------

            st.markdown("### Overall Risk")

            overall_risk = risk_summary["overall_risk"]

            if overall_risk == "Low Risk":

                st.success(overall_risk)

            elif overall_risk == "Moderate Risk":

                st.warning(overall_risk)

            else:

                st.error(overall_risk)

            # ----------------------------------------------
            # Executive Summary
            # ----------------------------------------------

            st.markdown(
                "### Executive Summary"
            )

            st.write(
                risk_summary["executive_summary"]
            )

            # ----------------------------------------------
            # Strengths
            # ----------------------------------------------

            strengths = risk_summary.get(
                "strengths",
                []
            )

            if strengths:

                st.markdown(
                    "### Strengths"
                )

                for item in strengths:

                    st.markdown(
                        f"✅ {item}"
                    )

            # ----------------------------------------------
            # Risk Factors
            # ----------------------------------------------

            risk_factors = risk_summary.get(
                "risk_factors",
                []
            )

            st.markdown(
                "### Risk Factors"
            )

            if risk_factors:

                for item in risk_factors:

                    st.markdown(
                        f"⚠️ {item}"
                    )

            else:

                st.info(
                    "No significant risk factors identified."
                )

            # ----------------------------------------------
            # Key Observations
            # ----------------------------------------------

            observations = risk_summary.get(
                "key_observations",
                []
            )

            if observations:

                st.markdown(
                    "### Key Observations"
                )

                for item in observations:

                    st.markdown(
                        f"• {item}"
                    )

            # ----------------------------------------------
            # Supporting Evidence
            # ----------------------------------------------

            evidence = risk_summary.get(
                "supporting_evidence",
                []
            )

            if evidence:

                st.markdown(
                    "### Supporting Evidence"
                )

                for item in evidence:

                    st.markdown(
                        f"- {item}"
                    )

            # ----------------------------------------------
            # Expandable Details
            # ----------------------------------------------

            with st.expander(
                "Customer Profile"
            ):

                st.json(
                    customer["customer_profile"]
                )

            with st.expander(
                "Assessment Details"
            ):

                st.json(
                    customer["assessment"]
                )


coordinator = load_coordinator()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title(
    "📊 Credit Risk Research Agent"
)

st.markdown(
    """
    Ask questions about:
    • Credit policies
    • Customer assessments
    • Eligibility rules
    • Credit risk
    """
)


# --------------------------------------------------
# Query Input
# --------------------------------------------------

query = st.text_area(
    "Ask a Credit Risk Question",
    height=120,
    placeholder=(
        "Example:\n"
        "What is the minimum credit score "
        "required for a premium credit card?"
    )
)


# --------------------------------------------------
# Submit Button
# --------------------------------------------------

if st.button(
    "Submit Question"
):

    if not query.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Processing Request..."
        ):

            try:
                start = time.time()
                response = (
                    coordinator.process_query(
                        query
                    )
                )

                st.success(
                    "Response Generated"
                )
                end = time.time()
                st.markdown(
                    "### Answer"
                )

                render_response(
                    response
                )
                
                st.caption(
                    f"Response generated in {end-start:.2f} seconds"
                )

                st.session_state.history.append(
                {
                    "query": query,
                    "response": response
                }
                )
                
            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )



if st.sidebar.button("Clear History"):

    st.session_state.history=[]

# --------------------------------------------------
# Sample Questions
# --------------------------------------------------

st.markdown("---")

st.markdown(
    "### Sample Questions"
)

st.markdown(
    """
    - What is the minimum credit score required for a premium credit card?

    - Can a customer with a credit score of 640 be approved?

    - What utilization ratio is considered low risk?

    - What annual income is required for self-employed applicants?

    - What conditions result in automatic decline?
    """
)
