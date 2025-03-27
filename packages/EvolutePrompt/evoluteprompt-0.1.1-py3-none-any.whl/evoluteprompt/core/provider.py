"""Base class for LLM providers."""

from abc import ABC, abstractmethod
from typing import Optional

from evoluteprompt.core.prompt import Prompt
from evoluteprompt.core.response import LLMResponse


class LLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the provider.

        Args:
            api_key: API key for the provider.
        """
        self.api_key = api_key

    @abstractmethod
    async def generate(self, prompt: Prompt) -> LLMResponse:
        """Generate a response from the LLM.

        Args:
            prompt: The prompt to send to the LLM.

        Returns:
            The response from the LLM.
        """
        pass

    @abstractmethod
    async def generate_stream(self, prompt: Prompt) -> LLMResponse:
        """Generate a streaming response from the LLM.

        Args:
            prompt: The prompt to send to the LLM.

        Returns:
            The streaming response from the LLM.
        """
        pass
