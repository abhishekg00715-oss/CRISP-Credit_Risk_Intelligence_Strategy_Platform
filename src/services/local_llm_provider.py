"""
local_llm_provider.py

Local LLM implementation using Ollama.

This component isolates local model invocation from the
Portfolio Reasoning Service.
"""

from typing import Optional

from src.services.llm_provider import (
    LLMProvider,
)


class LocalLLMProvider(LLMProvider):
    """
    LLM provider for a locally hosted model.

    The implementation can be replaced without changing
    PortfolioReasoningService.
    """

    def __init__(
        self,
        model_name: str = "llama3.1:latest",
        base_url: str = "http://localhost:11434",
    ) -> None:

        self.model_name = model_name

        self.base_url = base_url

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an LLM response.

        The actual Ollama invocation is isolated here.
        """

        import requests

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        response_data = response.json()

        return response_data.get(
            "response",
            "",
        )
