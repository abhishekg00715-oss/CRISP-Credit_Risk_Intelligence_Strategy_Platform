"""
llm_provider.py

Provider abstraction for LLM-based reasoning.

The interface deliberately contains no dependency on a specific
LLM framework or vendor.
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract interface for an LLM provider.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the supplied prompt.
        """

        raise NotImplementedError
