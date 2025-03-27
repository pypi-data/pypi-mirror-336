"""
Anthropic provider integration.
"""

import os
from typing import Any, Dict, Optional

from evoluteprompt.core.prompt import Prompt
from evoluteprompt.core.provider import LLMProvider
from evoluteprompt.core.response import LLMResponse


class AnthropicProvider(LLMProvider):
    """Provider for Anthropic's Claude API."""

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: str = "claude-2.1",
            **kwargs):
        """
        Initialize the Anthropic provider.

        Args:
            api_key: Anthropic API key. If not provided, will use ANTHROPIC_API_KEY env var.
            model: Model to use. Default is claude-2.1.
            **kwargs: Additional provider-specific arguments.
        """
        # Get API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")

        if api_key is None:
            raise ValueError(
                "Anthropic API key not provided. Either pass it as an argument or set ANTHROPIC_API_KEY environment variable."
            )

        super().__init__(api_key=api_key, **kwargs)
        self.model = model

    async def complete_async(self, prompt: Prompt) -> LLMResponse:
        """
        Complete a prompt asynchronously.

        Args:
            prompt: The prompt to complete.

        Returns:
            The response from the LLM.
        """
        # This is a stub - implementation will be added in the future
        raise NotImplementedError("Anthropic provider not yet implemented")

    async def stream_async(self, prompt: Prompt) -> LLMResponse:
        """
        Stream a response to a prompt asynchronously.

        Args:
            prompt: The prompt to complete.

        Returns:
            The streaming response from the LLM.
        """
        # This is a stub - implementation will be added in the future
        raise NotImplementedError("Anthropic provider not yet implemented")
