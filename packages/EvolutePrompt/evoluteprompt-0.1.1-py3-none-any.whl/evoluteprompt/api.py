"""
High-level API for EvolutePrompt.
"""

import asyncio
from typing import Any, Callable, Dict, List, Optional

from evoluteprompt.core.database import DBPromptRepo
from evoluteprompt.core.prompt import Prompt, PromptBuilder
from evoluteprompt.core.strategy import (
    ActivePromptStrategy,
    FallbackPromptStrategy,
    LatestPromptStrategy,
    PromptSelector,
    PromptStrategy,
)
from evoluteprompt.core.template import MultiMessageTemplate, PromptTemplate
from evoluteprompt.core.types import MessageRole, PromptCategory


class EvolutePrompt:
    """Main class for interacting with EvolutePrompt."""

    def __init__(self, db_url: str = "sqlite:///:memory:"):
        """Initialize EvolutePrompt.

        Args:
            db_url: URL for the database. Defaults to in-memory SQLite.
        """
        self.repo = DBPromptRepo(db_url)
        self.selector = PromptSelector(self.repo)

    def _get_or_create_event_loop(self):
        """Get the current event loop or create a new one if it doesn't exist."""
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            # Create a new event loop if one doesn't exist in the current
            # thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

    def init(self):
        """Initialize the database."""
        self.repo.init()

    def close(self):
        """Close the database connection."""
        self.repo.close()

    def create_prompt(self) -> PromptBuilder:
        """Create a new prompt.

        Returns:
            A PromptBuilder for building the prompt.
        """
        return PromptBuilder()

    def save_prompt(self, name: str, prompt: Prompt) -> str:
        """Save a prompt.

        Args:
            name: Name of the prompt.
            prompt: The prompt to save.

        Returns:
            The version of the saved prompt.
        """
        return self.repo.save_prompt(name, prompt)

    def get_prompt(
        self,
        name: str,
        version: Optional[str] = None,
    ) -> Optional[Prompt]:
        """Get a prompt by name and version.

        Args:
            name: Name of the prompt.
            version: Version of the prompt. If None, gets the latest version.

        Returns:
            The prompt, or None if not found.
        """
        return self.repo.get_prompt(name, version)

    def get_active_prompt(self, name: str) -> Optional[Prompt]:
        """Get the active version of a prompt.

        Args:
            name: Name of the prompt.

        Returns:
            The active prompt, or None if not found.
        """
        return self.repo.get_active_prompt(name)

    def get_fallback_prompt(self, name: str) -> Optional[Prompt]:
        """Get the fallback prompt for a prompt.

        Args:
            name: Name of the prompt.

        Returns:
            The fallback prompt, or None if not found.
        """
        return self.repo.get_fallback_prompt(name)

    def list_prompts(
        self,
        category: Optional[PromptCategory] = None,
    ) -> List[str]:
        """List all prompts.

        Args:
            category: Optional category to filter by.

        Returns:
            List of prompt names.
        """
        return self.repo.list_prompts(category)

    def list_versions(self, name: str) -> List[str]:
        """List all versions of a prompt.

        Args:
            name: Name of the prompt.

        Returns:
            List of versions.
        """
        return self.repo.list_versions(name)

    def set_active(self, name: str, version: str):
        """Set a prompt version as active.

        Args:
            name: Name of the prompt.
            version: Version to set as active.
        """
        self.repo.set_active(name, version)

    def set_fallback(self, name: str, version: str, fallback_for: str):
        """Set a prompt version as a fallback for another prompt.

        Args:
            name: Name of the prompt.
            version: Version to set as fallback.
            fallback_for: Name of the prompt to set fallback for.
        """
        self.repo.set_fallback(name, version, fallback_for)

    def select_prompt(
        self,
        name: str,
        strategy: Optional[PromptStrategy] = None,
        context: Dict[str, Any] = None,
    ) -> Optional[Prompt]:
        """Select a prompt using a strategy.

        Args:
            name: Name of the prompt.
            strategy: Strategy to use for selection. If None, uses default.
            context: Additional context for prompt selection.

        Returns:
            The selected prompt, or None if not found.
        """
        return self.selector.select_prompt(name, strategy, context)

    def create_fallback_strategy(
        self,
        primary_strategy: Optional[PromptStrategy] = None,
    ) -> FallbackPromptStrategy:
        """Create a fallback strategy.

        Args:
            primary_strategy: The primary strategy to try first.
                If None, uses ActivePromptStrategy.

        Returns:
            A FallbackPromptStrategy.
        """
        if primary_strategy is None:
            primary_strategy = ActivePromptStrategy(self.repo)
        return FallbackPromptStrategy(self.repo, primary_strategy)

    def create_latest_strategy(self) -> LatestPromptStrategy:
        """Create a strategy that selects the latest prompt version.

        Returns:
            A LatestPromptStrategy.
        """
        return LatestPromptStrategy(self.repo)

    def template_from_string(
        self,
        template_str: str,
        variables: Dict[str, Any] = None,
    ) -> PromptTemplate:
        """Create a prompt template from a string.

        Args:
            template_str: The template string.
            variables: Optional default variables for the template.

        Returns:
            A PromptTemplate.
        """
        return PromptTemplate.from_string(template_str, variables)

    def template_from_file(self, file_path: str) -> PromptTemplate:
        """Create a prompt template from a file.

        Args:
            file_path: The path to the template file.

        Returns:
            A PromptTemplate.
        """
        return PromptTemplate.from_file(file_path)

    def multi_message_template_from_file(
        self,
        file_path: str,
        delimiter: str = "---",
    ) -> MultiMessageTemplate:
        """Create a multi-message template from a file.

        Args:
            file_path: The path to the template file.
            delimiter: The delimiter between messages.

        Returns:
            A MultiMessageTemplate.
        """
        return MultiMessageTemplate.from_file(file_path, delimiter)

    def create_ab_testing(
        self,
        prompt_variants: List[str],
        weights: Optional[List[float]] = None,
    ) -> PromptStrategy:
        """Create an A/B testing strategy.

        Args:
            prompt_variants: List of prompt names to test.
            weights: Optional weights for the variants.

        Returns:
            An A/B testing strategy.
        """
        return self.selector.create_ab_testing_strategy(
            prompt_variants,
            weights,
        )

    def create_context_aware(
        self,
        context_key: str,
        prompt_mapping: Dict[Any, str],
    ) -> PromptStrategy:
        """Create a context-aware strategy.

        Args:
            context_key: The key to look up in the context.
            prompt_mapping: A mapping from context values to prompt names.

        Returns:
            A context-aware strategy.
        """
        return self.selector.create_context_aware_strategy(
            context_key,
            prompt_mapping,
        )

    def create_conditional(
        self,
        condition_fn: Callable[[Dict[str, Any]], bool],
        if_true: PromptStrategy,
        if_false: PromptStrategy,
    ) -> PromptStrategy:
        """Create a conditional strategy.

        Args:
            condition_fn: A function that takes the context and returns a boolean.
            if_true: The strategy to use if the condition is true.
            if_false: The strategy to use if the condition is false.

        Returns:
            A conditional strategy.
        """
        return self.selector.create_conditional_strategy(
            condition_fn,
            if_true,
            if_false,
        )

    def category_prompts(
        self,
        category: PromptCategory,
    ) -> PromptStrategy:
        """Create a strategy that selects prompts in a category.

        Args:
            category: The category to filter by.

        Returns:
            A category-based strategy.
        """
        return self.selector.create_category_strategy(category)

    def update_stats(
        self,
        name: str,
        version: str,
        success: bool = True,
    ) -> None:
        """Update the stats for a prompt.

        Args:
            name: The name of the prompt.
            version: The version to update.
            success: Whether the prompt was used successfully.
        """
        loop = self._get_or_create_event_loop()
        loop.run_until_complete(self.repo.update_stats(name, version, success))

    def create_prompt_from_file(
        self,
        template_file: str,
        role: MessageRole = MessageRole.USER,
        variables: Optional[Dict[str, Any]] = None,
        require_user_message: bool = True,
    ) -> Prompt:
        """Create a prompt from a template file.

        Args:
            template_file: Path to the template file.
            role: The role of the message (default: USER).
            variables: Variables to use in the template (default: None).
            require_user_message: Whether to require a user message (default: True).

        Returns:
            A Prompt object.
        """
        template = PromptTemplate.from_file(template_file)
        return template.to_prompt(
            role=role,
            require_user_message=require_user_message,
            **(variables or {}),
        )
