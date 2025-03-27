"""Core types for EvolutePrompt."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Role of a message in a conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class Message(BaseModel):
    """A message in a conversation."""

    role: MessageRole
    content: str
    name: Optional[str] = None


class FunctionDefinition(BaseModel):
    """Definition of a function that can be called by the model."""

    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class PromptCategory(str, Enum):
    """Categories for prompts."""

    CHAT = "chat"
    SEARCH = "search"
    SUMMARIZATION = "summarization"
    QA = "qa"
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"
    GENERATION = "generation"
    CUSTOM = "custom"


class PromptMetadata(BaseModel):
    """Metadata for a prompt."""

    version: str
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    author: Optional[str] = None
    category: Optional[PromptCategory] = None
    is_active: bool = False
    is_fallback: bool = False
    fallback_for: Optional[str] = None
    priority: int = 0  # Higher priority prompts are selected first


class PromptStats(BaseModel):
    """Statistics for a prompt."""

    token_count: Optional[int] = None
    character_count: Optional[int] = None
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    latency_ms: Optional[float] = None
    success_count: int = 0
    failure_count: int = 0
    last_used: Optional[str] = None


class PromptParameters(BaseModel):
    """Parameters for a prompt."""

    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    functions: Optional[List[FunctionDefinition]] = None
    function_call: Optional[Union[str, Dict[str, str]]] = None
    model: Optional[str] = None
