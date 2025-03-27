"""
HuggingFace provider integration.
"""

import os
from typing import Any, Dict, Optional

from promptflow.core.prompt import Prompt
from promptflow.core.provider import LLMProvider
from promptflow.core.response import LLMResponse


class HuggingFaceProvider(LLMProvider):
    """Provider for HuggingFace's API."""

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: str = "google/flan-t5-xxl",
            **kwargs):
        """
        Initialize the HuggingFace provider.

        Args:
            api_key: HuggingFace API key. If not provided, will use HUGGINGFACE_API_KEY env var.
            model: Model to use. Default is google/flan-t5-xxl.
            **kwargs: Additional provider-specific arguments.
        """
        # Get API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("HUGGINGFACE_API_KEY")

        if api_key is None:
            raise ValueError(
                "HuggingFace API key not provided. Either pass it as an argument or set HUGGINGFACE_API_KEY environment variable."
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
        raise NotImplementedError("HuggingFace provider not yet implemented")

    async def stream_async(self, prompt: Prompt) -> LLMResponse:
        """
        Stream a response to a prompt asynchronously.

        Args:
            prompt: The prompt to complete.

        Returns:
            The streaming response from the LLM.
        """
        # This is a stub - implementation will be added in the future
        raise NotImplementedError("HuggingFace provider not yet implemented")
