"""
Base class for prompt filters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from promptflow.core.prompt import Prompt


class FilterResult:
    """Result of a filter check."""

    def __init__(self,
                 passed: bool,
                 reason: Optional[str] = None,
                 details: Optional[Dict[str,
                                        Any]] = None):
        """
        Initialize a filter result.

        Args:
            passed: Whether the prompt passed the filter.
            reason: The reason the prompt failed, if it did.
            details: Additional details about the filter check.
        """
        self.passed = passed
        self.reason = reason
        self.details = details or {}

    def __bool__(self) -> bool:
        """Convert to boolean."""
        return self.passed


class PromptFilter(ABC):
    """
    Base class for prompt filters.
    """

    def __init__(self, name: Optional[str] = None):
        """
        Initialize a prompt filter.

        Args:
            name: Name of the filter.
        """
        self.name = name or self.__class__.__name__

    @abstractmethod
    def check(self, prompt: Prompt) -> FilterResult:
        """
        Check if a prompt passes this filter.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed.
        """
        pass

    def __call__(self, prompt: Prompt) -> FilterResult:
        """
        Call the filter on a prompt.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed.
        """
        return self.check(prompt)
