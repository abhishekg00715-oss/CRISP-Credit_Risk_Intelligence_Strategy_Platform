
"""
portfolio_reasoning_prompt.py

Builds the prompt supplied to the LLM for Portfolio Intelligence.

Responsibilities
----------------
- Provide the user request to the reasoning model.
- Provide the complete deterministic analytical context.
- Define the portfolio reasoning contract.
- Constrain the LLM to the supplied analytical context.
- Require machine-readable structured JSON output.

The prompt builder does NOT:
- Perform portfolio calculations.
- Interpret portfolio data itself.
- Select individual analytics services.
- Parse the LLM response.
- Depend on a specific LLM vendor or framework.
"""

import json
from typing import Any, Dict


class PortfolioReasoningPromptBuilder:
    """
    Builds structured prompts for Portfolio Intelligence reasoning.

    The builder establishes the contract consumed by
    PortfolioReasoningService.
    """

    # --------------------------------------------------------------
    # Main Prompt Builder
    # --------------------------------------------------------------

    def build(
        self,
        query: str,
        analytical_context: Dict[str, Any],
    ) -> str:
        """
        Construct the Portfolio Intelligence reasoning prompt.

        Parameters
        ----------
        query:
            User's portfolio-related request.

        analytical_context:
            Complete analytical context produced by
            PortfolioAnalyticsService.

        Returns
        -------
        str
            Prompt to be supplied to the configured LLM.
        """

        context_json = json.dumps(
            analytical_context,
            indent=2,
            default=str,
        )

        return f"""
You are a Portfolio Intelligence reasoning assistant.

Your responsibility is to interpret the supplied portfolio
analytical context and produce concise, evidence-grounded
portfolio insights for the user's request.

------------------------------------------------------------
USER REQUEST
------------------------------------------------------------

{query}

------------------------------------------------------------
PORTFOLIO ANALYTICAL CONTEXT
------------------------------------------------------------

The following information has been calculated by deterministic
Portfolio Analytics services.

Use ONLY this supplied analytical context.

{context_json}

------------------------------------------------------------
REASONING RULES
------------------------------------------------------------

1. Use only information contained in the supplied analytical
   context.

2. Do not use external knowledge or assumptions.

3. Do not invent portfolio metrics, values, thresholds,
   percentages, trends, risks, or opportunities.

4. Do not perform new portfolio calculations.

5. Do not infer numerical values that are not explicitly
   supported by the supplied context.

6. Interpret and synthesize the supplied analytical information
   rather than repeating the entire analytical context.

7. Keep each reasoning item concise and specific.

8. Every observation, risk, trend, and opportunity must be
   supported by one or more analytical domains present in the
   supplied context.

9. If the analytical context does not support a particular
   conclusion, do not manufacture one.

10. The complete analytical context is available to you.
    Consider information across domains when it is relevant to
    the user's request.

------------------------------------------------------------
REASONING SECTIONS
------------------------------------------------------------

Return insights using the following four sections.

observations
    Factual interpretations of the supplied portfolio data.
    These should describe meaningful portfolio characteristics
    without introducing unsupported conclusions.

risks
    Material portfolio risk findings supported by the supplied
    analytical context.

trends
    Meaningful changes, movements, improving conditions, or
    deteriorating conditions supported by the supplied trend or
    related analytical context.

opportunities
    Actionable portfolio opportunities supported by the supplied
    analytical context.

------------------------------------------------------------
SUPPORTING DOMAINS
------------------------------------------------------------

Each reasoning item should identify the analytical domain or
domains that support it.

Use domain names exactly as they appear in the supplied
analytical context.

Examples of possible domains include:

- kpis
- risk
- exposure
- segmentation
- trends
- opportunities

Only use domains that actually exist in the supplied context.

------------------------------------------------------------
OUTPUT CONTRACT
------------------------------------------------------------

Return ONLY a valid JSON object.

Do not return:

- Markdown
- Markdown code fences
- Explanatory text
- Headings outside the JSON object
- Commentary before or after the JSON

The JSON object MUST contain exactly these four reasoning
sections:

{{
  "observations": [],
  "risks": [],
  "trends": [],
  "opportunities": []
}}

Each section MUST be a JSON array.

Each reasoning item should be a JSON object.

Recommended structure:

{{
  "observations": [
    {{
      "title": "Concise observation title",
      "description": "Concise factual interpretation",
      "supporting_domains": ["kpis", "segmentation"]
    }}
  ],
  "risks": [
    {{
      "title": "Concise risk title",
      "description": "Concise explanation of the risk",
      "severity": "high",
      "supporting_domains": ["risk", "exposure"]
    }}
  ],
  "trends": [
    {{
      "title": "Concise trend title",
      "description": "Concise explanation of the observed trend",
      "direction": "deteriorating",
      "supporting_domains": ["trends"]
    }}
  ],
  "opportunities": [
    {{
      "title": "Concise opportunity title",
      "description": "Concise explanation of the opportunity",
      "supporting_domains": ["opportunities", "segmentation"]
    }}
  ]
}}

------------------------------------------------------------
FIELD RULES
------------------------------------------------------------

observations
    Required JSON array.
    Each item should contain:
    - title
    - description
    - supporting_domains

risks
    Required JSON array.
    Each item should contain:
    - title
    - description
    - severity
    - supporting_domains

    Use severity only when supported by the analytical context.
    Do not invent a severity level where the data does not
    support one.

trends
    Required JSON array.
    Each item should contain:
    - title
    - description
    - direction
    - supporting_domains

    Use direction values such as:
    - improving
    - deteriorating
    - stable

    Only use a direction when it is supported by the supplied
    analytical context.

opportunities
    Required JSON array.
    Each item should contain:
    - title
    - description
    - supporting_domains

------------------------------------------------------------
EMPTY SECTIONS
------------------------------------------------------------

If the supplied analytical context does not support a meaningful
item for a section, return an empty array for that section.

For example:

"opportunities": []

Do not create an opportunity merely to populate the section.

------------------------------------------------------------
FINAL REQUIREMENT
------------------------------------------------------------

Return ONLY the JSON object conforming to the contract above.
"""