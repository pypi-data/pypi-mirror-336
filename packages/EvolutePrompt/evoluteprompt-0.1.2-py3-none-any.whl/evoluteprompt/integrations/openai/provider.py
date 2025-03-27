"""
OpenAI provider integration.
"""

import os
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

import aiohttp
import tiktoken

from evoluteprompt.core.prompt import Prompt
from evoluteprompt.core.provider import LLMProvider
from evoluteprompt.core.response import FunctionCall, LLMResponse, StreamingResponse
from evoluteprompt.core.types import Message, MessageRole


class OpenAIProvider(LLMProvider):
    """Provider for OpenAI API."""

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: str = "gpt-3.5-turbo",
            **kwargs):
        """
        Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key. If not provided, will use OPENAI_API_KEY env var.
            model: Model to use. Default is gpt-3.5-turbo.
            **kwargs: Additional parameters to pass to the OpenAI API.
        """
        # Get API key from environment variable if not provided
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")

        if api_key is None:
            raise ValueError(
                "OpenAI API key not provided. Either pass it as an argument or set OPENAI_API_KEY environment variable."
            )

        super().__init__(api_key=api_key, **kwargs)
        self.model = model
        self.base_url = kwargs.get("base_url", "https://api.openai.com/v1")

    def _convert_prompt_to_messages(
            self, prompt: Prompt) -> List[Dict[str, Any]]:
        """
        Convert a Prompt object to OpenAI messages format.

        Args:
            prompt: The prompt to convert.

        Returns:
            List of messages in OpenAI format.
        """
        openai_messages = []

        for message in prompt.messages:
            msg = {"role": message.role.value, "content": message.content}

            # Add name if present (for function calls)
            if message.name:
                msg["name"] = message.name

            openai_messages.append(msg)

        return openai_messages

    def _get_headers(self) -> Dict[str, str]:
        """
        Get headers for OpenAI API requests.

        Returns:
            Headers dictionary.
        """
        return {
            "Authorization": f"Bearer {
                self.api_key}",
            "Content-Type": "application/json"}

    def _build_request_body(self, prompt: Prompt) -> Dict[str, Any]:
        """
        Build the request body for the OpenAI API.

        Args:
            prompt: The prompt to send.

        Returns:
            Request body dictionary.
        """
        messages = self._convert_prompt_to_messages(prompt)

        # Start with model and messages
        body = {"model": self.model, "messages": messages}

        # Add parameters from prompt if available
        if prompt.parameters:
            params = prompt.parameters.model_dump(exclude_none=True)
            body.update(params)

        # If model not specified in parameters, use the one from constructor
        if "model" not in body:
            body["model"] = self.model

        return body

    def _count_tokens(self, prompt: Prompt) -> int:
        """
        Count the number of tokens in a prompt.

        Args:
            prompt: The prompt to count tokens for.

        Returns:
            Number of tokens.
        """
        # Get the encoder for the model
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # Fallback to cl100k_base for new models not yet in tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")

        # Count tokens for each message
        token_count = 0

        for message in prompt.messages:
            # Add tokens for message format (role, content, etc.)
            token_count += 4  # Approx overhead per message

            # Add tokens for content
            if message.content:
                token_count += len(encoding.encode(message.content))

            # Add tokens for name if present
            if message.name:
                token_count += len(encoding.encode(message.name))

        # Add tokens for the overall message format
        token_count += 3  # Approx overhead for the overall structure

        return token_count

    def _parse_response(self, data: Dict[str, Any]) -> LLMResponse:
        """
        Parse the response from the OpenAI API.

        Args:
            data: Response data from the API.

        Returns:
            LLMResponse object.
        """
        # Extract the message content
        if "choices" not in data or not data["choices"]:
            raise ValueError("Invalid response from OpenAI API")

        choice = data["choices"][0]

        if "message" not in choice:
            raise ValueError("No message in response from OpenAI API")

        message = choice["message"]

        # Get function call if present
        function_call = None
        if "function_call" in message:
            import json

            function_call = FunctionCall(
                name=message["function_call"]["name"],
                arguments=json.loads(message["function_call"]["arguments"]),
            )

        # Extract content
        content = message.get("content", "")

        # Extract usage data if available
        stats = None
        if "usage" in data:
            stats = {
                "prompt_tokens": data["usage"].get("prompt_tokens"),
                "completion_tokens": data["usage"].get("completion_tokens"),
                "total_tokens": data["usage"].get("total_tokens"),
            }

        # Create the response
        response = LLMResponse(
            text=content,
            model=data.get("model", self.model),
            provider="openai",
            function_call=function_call,
            stats=stats,
            raw_response=data,
        )

        return response

    def _parse_streaming_chunk(
        self, chunk: Dict[str, Any], stream_response: StreamingResponse
    ) -> None:
        """
        Parse a chunk from the OpenAI API streaming response.

        Args:
            chunk: Chunk of data from the API.
            stream_response: StreamingResponse object to update.
        """
        if "choices" not in chunk or not chunk["choices"]:
            return

        choice = chunk["choices"][0]

        # For newer models, content is in delta
        if "delta" in choice:
            delta = choice["delta"]

            if "content" in delta and delta["content"]:
                stream_response.add_chunk(delta["content"])

        # For older models, content is directly in text
        elif "text" in choice and choice["text"]:
            stream_response.add_chunk(choice["text"])

    async def complete_async(self, prompt: Prompt) -> LLMResponse:
        """
        Complete a prompt asynchronously.

        Args:
            prompt: The prompt to complete.

        Returns:
            The response from the LLM.
        """
        # Build request
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()
        body = self._build_request_body(prompt)

        # Calculate token count
        token_count = self._count_tokens(prompt)

        # Make the request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise ValueError(
                        f"OpenAI API error ({
                            resp.status}): {error_text}")

                data = await resp.json()

        # Parse the response
        response = self._parse_response(data)

        # Update stats
        if response.stats is None:
            response.stats = {}
        response.stats["token_count"] = token_count

        return response

    async def stream_async(self, prompt: Prompt) -> LLMResponse:
        """
        Stream a response to a prompt asynchronously.

        Args:
            prompt: The prompt to complete.

        Returns:
            The streaming response from the LLM.
        """
        # Build request
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()
        body = self._build_request_body(prompt)

        # Set streaming parameter
        body["stream"] = True

        # Calculate token count
        token_count = self._count_tokens(prompt)

        # Initialize streaming response
        stream_response = StreamingResponse(
            model=self.model, provider="openai")

        # Update stats
        stream_response.stats.token_count = token_count

        # Make the request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as resp:
                if resp.status != 200:
                    error_text = await resp.text()
                    raise ValueError(
                        f"OpenAI API error ({
                            resp.status}): {error_text}")

                # Process the streaming response
                async for line in resp.content:
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Skip the "data: " prefix
                    if line.startswith(b"data: "):
                        line = line[6:]

                    # Skip the "[DONE]" message
                    if line == b"[DONE]":
                        break

                    try:
                        import json

                        chunk = json.loads(line)
                        self._parse_streaming_chunk(chunk, stream_response)
                    except Exception as e:
                        # Skip invalid JSON
                        continue

        # Mark streaming as done
        stream_response.done = True

        # Convert to LLMResponse
        return stream_response.to_response()
