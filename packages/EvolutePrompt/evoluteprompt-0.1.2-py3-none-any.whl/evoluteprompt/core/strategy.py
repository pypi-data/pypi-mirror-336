"""
Strategy patterns for prompt selection and fallback management.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Union

from evoluteprompt.core.database import DBPromptRepo
from evoluteprompt.core.prompt import Prompt
from evoluteprompt.core.types import PromptCategory


class PromptStrategy(ABC):
    """Base class for prompt selection strategies."""

    @abstractmethod
    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Select a prompt based on the strategy.

        Args:
            prompt_name: The name of the prompt.
            context: Additional context for prompt selection.

        Returns:
            The selected prompt, or None if not found.
        """
        pass


class ActivePromptStrategy(PromptStrategy):
    """Strategy that selects the active prompt."""

    def __init__(self, repo: DBPromptRepo):
        """
        Initialize the strategy.

        Args:
            repo: The prompt repository.
        """
        self.repo = repo

    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Select the active prompt.

        Args:
            prompt_name: The name of the prompt.
            context: Additional context for prompt selection (not used).

        Returns:
            The active prompt, or None if not found.
        """
        return await self.repo.get_active_prompt(prompt_name)


class FallbackPromptStrategy(PromptStrategy):
    """Strategy that selects a prompt with fallback."""

    def __init__(self, repo: DBPromptRepo, primary_strategy: PromptStrategy):
        """
        Initialize the strategy.

        Args:
            repo: The prompt repository.
            primary_strategy: The primary strategy to try first.
        """
        self.repo = repo
        self.primary_strategy = primary_strategy

    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Select a prompt with fallback.

        Args:
            prompt_name: The name of the prompt.
            context: Additional context for prompt selection.

        Returns:
            The selected prompt, or the fallback prompt if the primary strategy fails.
        """
        # Try the primary strategy first
        prompt = await self.primary_strategy.select_prompt(prompt_name, context)
        if prompt is not None:
            return prompt

        # Fall back to the fallback prompt
        return await self.repo.get_fallback_prompt(prompt_name)


class LatestPromptStrategy(PromptStrategy):
    """Strategy that selects the latest prompt version."""

    def __init__(self, repo: DBPromptRepo):
        """
        Initialize the strategy.

        Args:
            repo: The prompt repository.
        """
        self.repo = repo

    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Select the latest prompt version.

        Args:
            prompt_name: The name of the prompt.
            context: Additional context for prompt selection (not used).

        Returns:
            The latest prompt version, or None if not found.
        """
        return await self.repo.get_prompt(prompt_name)


class ConditionalPromptStrategy(PromptStrategy):
    """Strategy that selects a prompt based on a condition."""

    def __init__(
        self,
        repo: DBPromptRepo,
        condition_fn: Callable[[Dict[str, Any]], bool],
        if_true: PromptStrategy,
        if_false: PromptStrategy,
    ):
        """
        Initialize the strategy.

        Args:
            repo: The prompt repository.
            condition_fn: A function that takes the context and returns a boolean.
            if_true: The strategy to use if the condition is true.
            if_false: The strategy to use if the condition is false.
        """
        self.repo = repo
        self.condition_fn = condition_fn
        self.if_true = if_true
        self.if_false = if_false

    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Select a prompt based on a condition.

        Args:
            prompt_name: The name of the prompt.
            context: Additional context for prompt selection.

        Returns:
            The selected prompt, or None if not found.
        """
        context = context or {}

        if self.condition_fn(context):
            return await self.if_true.select_prompt(prompt_name, context)
        else:
            return await self.if_false.select_prompt(prompt_name, context)


class ABTestingPromptStrategy(PromptStrategy):
    """Strategy that randomly selects between different prompts for A/B testing."""

    def __init__(self,
                 repo: DBPromptRepo,
                 prompt_variants: List[str],
                 weights: Optional[List[float]] = None):
        """
        Initialize the strategy.

        Args:
            repo: The prompt repository.
            prompt_variants: List of prompt names to test.
            weights: Optional weights for the variants (must sum to 1.0).
        """
        import random

        self.repo = repo
        self.prompt_variants = prompt_variants
        self.weights = weights
        self.random = random

    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Randomly select a prompt variant for A/B testing.

        Args:
            prompt_name: The name of the prompt (ignored).
            context: Additional context for prompt selection (not used).

        Returns:
            A randomly selected prompt, or None if none are found.
        """
        if not self.prompt_variants:
            return None

        # Randomly select a variant
        variant_name = self.random.choices(
            self.prompt_variants, weights=self.weights, k=1)[0]

        # Get the active prompt for the selected variant
        return await self.repo.get_active_prompt(variant_name)


class ContextAwarePromptStrategy(PromptStrategy):
    """Strategy that selects a prompt based on context."""

    def __init__(self, repo: DBPromptRepo, context_key: str,
                 prompt_mapping: Dict[Any, str]):
        """
        Initialize the strategy.

        Args:
            repo: The prompt repository.
            context_key: The key to look up in the context.
            prompt_mapping: A mapping from context values to prompt names.
        """
        self.repo = repo
        self.context_key = context_key
        self.prompt_mapping = prompt_mapping

    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Select a prompt based on context.

        Args:
            prompt_name: The default prompt name.
            context: Additional context for prompt selection.

        Returns:
            The selected prompt, or None if not found.
        """
        context = context or {}

        # Get the context value
        context_value = context.get(self.context_key)

        # If the context value is in the mapping, use that prompt
        if context_value in self.prompt_mapping:
            mapped_prompt_name = self.prompt_mapping[context_value]
            return await self.repo.get_active_prompt(mapped_prompt_name)

        # Otherwise, use the default prompt
        return await self.repo.get_active_prompt(prompt_name)


class CategoryPromptStrategy(PromptStrategy):
    """Strategy that selects a prompt based on category."""

    def __init__(self, repo: DBPromptRepo, category: PromptCategory):
        """
        Initialize the strategy.

        Args:
            repo: The prompt repository.
            category: The category to filter by.
        """
        self.repo = repo
        self.category = category

    async def select_prompt(
        self, prompt_name: str, context: Dict[str, Any] = None
    ) -> Optional[Prompt]:
        """
        Select a prompt based on category.

        Args:
            prompt_name: The name of the prompt.
            context: Additional context for prompt selection (not used).

        Returns:
            The selected prompt, or None if not found.
        """
        # First try to get an active prompt with this name and category
        prompt_model = await self.repo.get_active_prompt(prompt_name)

        if prompt_model is not None and prompt_model.metadata.category == self.category:
            return prompt_model

        # If not found, get the first active prompt in this category
        prompt_names = await self.repo.list_prompts(category=self.category)

        for name in prompt_names:
            prompt = await self.repo.get_active_prompt(name)
            if prompt is not None:
                return prompt

        return None


class PromptSelector:
    """
    A utility class for selecting prompts using different strategies.
    """

    def __init__(
            self,
            repo: DBPromptRepo,
            default_strategy: PromptStrategy = None):
        """
        Initialize the prompt selector.

        Args:
            repo: The prompt repository.
            default_strategy: The default strategy to use.
        """
        self.repo = repo
        self.default_strategy = default_strategy or ActivePromptStrategy(repo)

        # Common strategies
        self.active_strategy = ActivePromptStrategy(repo)
        self.fallback_strategy = FallbackPromptStrategy(
            repo, self.active_strategy)
        self.latest_strategy = LatestPromptStrategy(repo)

    async def select_prompt(
        self,
        prompt_name: str,
        strategy: Optional[PromptStrategy] = None,
        context: Dict[str, Any] = None,
    ) -> Optional[Prompt]:
        """
        Select a prompt using the specified strategy.

        Args:
            prompt_name: The name of the prompt.
            strategy: The strategy to use, or None to use the default.
            context: Additional context for prompt selection.

        Returns:
            The selected prompt, or None if not found.
        """
        strategy = strategy or self.default_strategy
        return await strategy.select_prompt(prompt_name, context)

    def create_ab_testing_strategy(
        self, prompt_variants: List[str], weights: Optional[List[float]] = None
    ) -> ABTestingPromptStrategy:
        """
        Create an A/B testing strategy.

        Args:
            prompt_variants: List of prompt names to test.
            weights: Optional weights for the variants.

        Returns:
            An A/B testing strategy.
        """
        return ABTestingPromptStrategy(self.repo, prompt_variants, weights)

    def create_context_aware_strategy(
        self, context_key: str, prompt_mapping: Dict[Any, str]
    ) -> ContextAwarePromptStrategy:
        """
        Create a context-aware strategy.

        Args:
            context_key: The key to look up in the context.
            prompt_mapping: A mapping from context values to prompt names.

        Returns:
            A context-aware strategy.
        """
        return ContextAwarePromptStrategy(
            self.repo, context_key, prompt_mapping)

    def create_conditional_strategy(
        self,
        condition_fn: Callable[[Dict[str, Any]], bool],
        if_true: PromptStrategy,
        if_false: PromptStrategy,
    ) -> ConditionalPromptStrategy:
        """
        Create a conditional strategy.

        Args:
            condition_fn: A function that takes the context and returns a boolean.
            if_true: The strategy to use if the condition is true.
            if_false: The strategy to use if the condition is false.

        Returns:
            A conditional strategy.
        """
        return ConditionalPromptStrategy(
            self.repo, condition_fn, if_true, if_false)

    def create_category_strategy(
            self, category: PromptCategory) -> CategoryPromptStrategy:
        """
        Create a category-based strategy.

        Args:
            category: The category to filter by.

        Returns:
            A category-based strategy.
        """
        return CategoryPromptStrategy(self.repo, category)
