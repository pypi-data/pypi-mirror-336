"""
Core prompt functionality for the PromptFlow library.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from promptflow.core.types import (
    FunctionDefinition,
    Message,
    MessageRole,
    PromptMetadata,
    PromptParameters,
    PromptStats,
)


class Prompt(BaseModel):
    """
    A prompt for a language model, consisting of a list of messages.
    """

    messages: List[Message]
    metadata: Optional[PromptMetadata] = None
    parameters: Optional[PromptParameters] = None
    stats: Optional[PromptStats] = None

    def add_message(
        self, role: Union[str, MessageRole], content: str, name: Optional[str] = None
    ) -> "Prompt":
        """Add a message to the prompt."""
        if isinstance(role, str):
            role = MessageRole(role)

        self.messages.append(Message(role=role, content=content, name=name))
        return self

    def add_system(self, content: str) -> "Prompt":
        """Add a system message to the prompt."""
        return self.add_message(MessageRole.SYSTEM, content)

    def add_user(self, content: str) -> "Prompt":
        """Add a user message to the prompt."""
        return self.add_message(MessageRole.USER, content)

    def add_assistant(self, content: str) -> "Prompt":
        """Add an assistant message to the prompt."""
        return self.add_message(MessageRole.ASSISTANT, content)

    def add_function_call(self, function_name: str,
                          function_args: Dict[str, Any]) -> "Prompt":
        """Add a function call message to the prompt."""
        return self.add_message(
            MessageRole.FUNCTION,
            json.dumps(function_args),
            name=function_name)

    def set_parameters(self, **kwargs) -> "Prompt":
        """Set prompt parameters."""
        if self.parameters is None:
            self.parameters = PromptParameters()

        for key, value in kwargs.items():
            if hasattr(self.parameters, key):
                setattr(self.parameters, key, value)

        return self

    def add_function_definition(
        self,
        name: str,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> "Prompt":
        """Add a function definition to the prompt parameters."""
        if self.parameters is None:
            self.parameters = PromptParameters()

        if self.parameters.functions is None:
            self.parameters.functions = []

        function_def = FunctionDefinition(
            name=name, description=description, parameters=parameters or {}
        )

        self.parameters.functions.append(function_def)
        return self

    def update_metadata(self, **kwargs) -> "Prompt":
        """Update prompt metadata."""
        if self.metadata is None:
            self.metadata = PromptMetadata(
                version="0.1.0", created_at=datetime.now().isoformat())

        self.metadata.updated_at = datetime.now().isoformat()

        for key, value in kwargs.items():
            if hasattr(self.metadata, key):
                setattr(self.metadata, key, value)

        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert the prompt to a dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert the prompt to a JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prompt":
        """Create a prompt from a dictionary."""
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, json_str: str) -> "Prompt":
        """Create a prompt from a JSON string."""
        return cls.model_validate_json(json_str)


class PromptBuilder:
    """
    Builder for creating prompts with a fluent API.
    """

    def __init__(self):
        self._messages: List[Message] = []
        self._metadata: Optional[PromptMetadata] = None
        self._parameters: Optional[PromptParameters] = None

    def add_message(
        self, role: Union[str, MessageRole], content: str, name: Optional[str] = None
    ) -> "PromptBuilder":
        """Add a message to the prompt."""
        if isinstance(role, str):
            role = MessageRole(role)

        self._messages.append(Message(role=role, content=content, name=name))
        return self

    def add_system(self, content: str) -> "PromptBuilder":
        """Add a system message to the prompt."""
        return self.add_message(MessageRole.SYSTEM, content)

    def add_user(self, content: str) -> "PromptBuilder":
        """Add a user message to the prompt."""
        return self.add_message(MessageRole.USER, content)

    def add_assistant(self, content: str) -> "PromptBuilder":
        """Add an assistant message to the prompt."""
        return self.add_message(MessageRole.ASSISTANT, content)

    def add_function_call(
        self, function_name: str, function_args: Dict[str, Any]
    ) -> "PromptBuilder":
        """Add a function call message to the prompt."""
        return self.add_message(
            MessageRole.FUNCTION,
            json.dumps(function_args),
            name=function_name)

    def set_metadata(self, **kwargs) -> "PromptBuilder":
        """Set prompt metadata."""
        if self._metadata is None:
            self._metadata = PromptMetadata(
                version="0.1.0", created_at=datetime.now().isoformat())

        self._metadata.updated_at = datetime.now().isoformat()

        for key, value in kwargs.items():
            if hasattr(self._metadata, key):
                setattr(self._metadata, key, value)

        return self

    def set_parameters(self, **kwargs) -> "PromptBuilder":
        """Set prompt parameters."""
        if self._parameters is None:
            self._parameters = PromptParameters()

        for key, value in kwargs.items():
            if hasattr(self._parameters, key):
                setattr(self._parameters, key, value)

        return self

    def add_function_definition(
        self,
        name: str,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> "PromptBuilder":
        """Add a function definition to the prompt parameters."""
        if self._parameters is None:
            self._parameters = PromptParameters()

        if self._parameters.functions is None:
            self._parameters.functions = []

        function_def = FunctionDefinition(
            name=name, description=description, parameters=parameters or {}
        )

        self._parameters.functions.append(function_def)
        return self

    def build(self, require_user_message: bool = False) -> Prompt:
        """
        Build the prompt.

        Args:
            require_user_message: If True, an error will be raised if there's no user message.
                                  If False, an empty prompt can be created without any user message.

        Returns:
            A Prompt object.

        Raises:
            ValueError: If require_user_message is True and there are no user messages.
        """
        # Check if we need to validate for user messages
        if require_user_message:
            has_user_message = any(
                msg.role == MessageRole.USER for msg in self._messages)
            if not has_user_message:
                raise ValueError(
                    "Prompt must contain at least one user message when require_user_message=True"
                )

        return Prompt(
            messages=self._messages,
            metadata=self._metadata,
            parameters=self._parameters)
