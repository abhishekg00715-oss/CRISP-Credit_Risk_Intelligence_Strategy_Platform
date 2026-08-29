"""
portfolio_reasoning_prompt.py

Builds the prompt supplied to the LLM for Portfolio Intelligence.
"""

import json

from typing import Any, Dict


class PortfolioReasoningPromptBuilder:
    """
    Builds structured prompts for portfolio reasoning.
    """

    def build(
        self,
        query: str,
        analytical_context: Dict[str, Any],
    ) -> str:
        """
        Construct the portfolio reasoning prompt.
        """

        context_json = json.dumps(
            analytical_context,
            indent=2,
            default=str,
        )

        return f"""
You are a Portfolio Intelligence reasoning assistant.

User request:
{query}

The following portfolio analytical context has been
calculated by deterministic analytics services.

Use ONLY the supplied analytical context.
Do not invent metrics or perform unsupported calculations.

Portfolio analytical context:
{context_json}

Analyse the information relevant to the user's request.

Return a structured response containing:

1. observations
2. risks
3. trends
4. opportunities
5. evidence

Keep observations factual and concise.

Every important observation, risk, trend or opportunity
should be supported by the supplied analytical context.
"""
