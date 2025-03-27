"""
Safety filters for prompts.
"""

import re
from typing import Any, Dict, List, Optional, Pattern, Set, Union

import tiktoken

try:
    import better_profanity

    PROFANITY_AVAILABLE = True
except ImportError:
    PROFANITY_AVAILABLE = False

from promptflow.core.prompt import Prompt
from promptflow.prompt_filters.base import FilterResult, PromptFilter


class KeywordFilter(PromptFilter):
    """
    Filter prompts based on banned keywords.
    """

    def __init__(
        self,
        keywords: List[str],
        case_sensitive: bool = False,
        check_user_messages_only: bool = True,
        name: Optional[str] = None,
    ):
        """
        Initialize a keyword filter.

        Args:
            keywords: List of banned keywords.
            case_sensitive: Whether to do case-sensitive matching.
            check_user_messages_only: Whether to only check user messages.
            name: Name of the filter.
        """
        super().__init__(name=name)
        self.keywords = keywords
        self.case_sensitive = case_sensitive
        self.check_user_messages_only = check_user_messages_only

    def check(self, prompt: Prompt) -> FilterResult:
        """
        Check if a prompt contains banned keywords.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed.
        """
        for message in prompt.messages:
            # Skip non-user messages if configured to do so
            if self.check_user_messages_only and message.role != "user":
                continue

            content = message.content
            if not self.case_sensitive:
                content = content.lower()

            for keyword in self.keywords:
                search_keyword = keyword if self.case_sensitive else keyword.lower()
                if search_keyword in content:
                    return FilterResult(
                        passed=False, reason=f"Prompt contains banned keyword: {keyword}", details={
                            "keyword": keyword, "message_role": message.role}, )

        return FilterResult(passed=True)


class RegexFilter(PromptFilter):
    """
    Filter prompts based on regular expressions.
    """

    def __init__(
        self,
        patterns: List[Union[str, Pattern]],
        check_user_messages_only: bool = True,
        name: Optional[str] = None,
    ):
        """
        Initialize a regex filter.

        Args:
            patterns: List of regex patterns to match against.
            check_user_messages_only: Whether to only check user messages.
            name: Name of the filter.
        """
        super().__init__(name=name)
        self.patterns = [re.compile(pattern) if isinstance(
            pattern, str) else pattern for pattern in patterns]
        self.check_user_messages_only = check_user_messages_only

    def check(self, prompt: Prompt) -> FilterResult:
        """
        Check if a prompt matches any banned patterns.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed.
        """
        for message in prompt.messages:
            # Skip non-user messages if configured to do so
            if self.check_user_messages_only and message.role != "user":
                continue

            content = message.content

            for pattern in self.patterns:
                match = pattern.search(content)
                if match:
                    return FilterResult(
                        passed=False,
                        reason=f"Prompt matches banned pattern: {
                            pattern.pattern}",
                        details={
                            "pattern": pattern.pattern,
                            "matched_text": match.group(0),
                            "message_role": message.role,
                        },
                    )

        return FilterResult(passed=True)


class ProfanityFilter(PromptFilter):
    """
    Filter prompts that contain profanity.
    """

    def __init__(
        self,
        custom_words: Optional[List[str]] = None,
        censor_char: str = "*",
        check_user_messages_only: bool = True,
        name: Optional[str] = None,
    ):
        """
        Initialize a profanity filter.

        Args:
            custom_words: Additional custom words to consider profanity.
            censor_char: Character to use for censoring profanity.
            check_user_messages_only: Whether to only check user messages.
            name: Name of the filter.
        """
        super().__init__(name=name)

        if not PROFANITY_AVAILABLE:
            raise ImportError(
                "The 'better_profanity' package is required for ProfanityFilter. "
                "Install it with 'pip install better-profanity'.")

        self.profanity = better_profanity.Profanity()
        if custom_words:
            self.profanity.add_censor_words(custom_words)

        self.censor_char = censor_char
        self.check_user_messages_only = check_user_messages_only

    def check(self, prompt: Prompt) -> FilterResult:
        """
        Check if a prompt contains profanity.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed.
        """
        for message in prompt.messages:
            # Skip non-user messages if configured to do so
            if self.check_user_messages_only and message.role != "user":
                continue

            content = message.content

            if self.profanity.contains_profanity(content):
                # Get the censored version to identify what was censored
                censored = self.profanity.censor(content, self.censor_char)
                return FilterResult(
                    passed=False,
                    reason="Prompt contains profanity",
                    details={"message_role": message.role, "censored_content": censored},
                )

        return FilterResult(passed=True)


class MaxTokenFilter(PromptFilter):
    """
    Filter prompts that exceed a maximum token count.
    """

    def __init__(
            self,
            max_tokens: int,
            encoding_name: str = "cl100k_base",
            name: Optional[str] = None):
        """
        Initialize a max token filter.

        Args:
            max_tokens: Maximum allowed tokens.
            encoding_name: Name of the tokenizer encoding to use.
            name: Name of the filter.
        """
        super().__init__(name=name)
        self.max_tokens = max_tokens
        self.encoding = tiktoken.get_encoding(encoding_name)

    def check(self, prompt: Prompt) -> FilterResult:
        """
        Check if a prompt exceeds the maximum token count.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed.
        """
        # Count tokens for each message
        token_count = 0

        for message in prompt.messages:
            # Add tokens for message format (role, content, etc.)
            token_count += 4  # Approx overhead per message

            # Add tokens for content
            if message.content:
                token_count += len(self.encoding.encode(message.content))

            # Add tokens for name if present
            if message.name:
                token_count += len(self.encoding.encode(message.name))

        # Add tokens for the overall message format
        token_count += 3  # Approx overhead for the overall structure

        if token_count > self.max_tokens:
            return FilterResult(
                passed=False, reason=f"Prompt exceeds maximum token count: {token_count} > {
                    self.max_tokens}", details={
                    "token_count": token_count, "max_tokens": self.max_tokens}, )

        return FilterResult(passed=True)


class ContentPolicyFilter(PromptFilter):
    """
    Filter prompts based on content policy rules.
    """

    def __init__(
        self,
        policies: Dict[str, Union[List[str], Pattern]],
        check_user_messages_only: bool = True,
        name: Optional[str] = None,
    ):
        """
        Initialize a content policy filter.

        Args:
            policies: Dictionary mapping policy names to lists of keywords or regex patterns.
            check_user_messages_only: Whether to only check user messages.
            name: Name of the filter.
        """
        super().__init__(name=name)
        self.policies = {}

        # Compile each policy as either a keyword filter or regex filter
        for policy_name, patterns in policies.items():
            if isinstance(
                patterns,
                list) and all(
                isinstance(
                    p,
                    str) for p in patterns):
                # Check if patterns look like regular expressions (contain
                # regex special chars)
                if any(re.search(r"[.*+?^${}()|[\]\\]", p) for p in patterns):
                    # This is a regex policy
                    self.policies[policy_name] = RegexFilter(
                        patterns=patterns,
                        check_user_messages_only=check_user_messages_only,
                        name=f"{policy_name}RegexFilter",
                    )
                else:
                    # This is a keyword policy
                    self.policies[policy_name] = KeywordFilter(
                        keywords=patterns,
                        case_sensitive=False,
                        check_user_messages_only=check_user_messages_only,
                        name=f"{policy_name}KeywordFilter",
                    )
            else:
                # This is a regex policy
                self.policies[policy_name] = RegexFilter(
                    patterns=[patterns] if not isinstance(
                        patterns,
                        list) else patterns,
                    check_user_messages_only=check_user_messages_only,
                    name=f"{policy_name}RegexFilter",
                )

        self.check_user_messages_only = check_user_messages_only

    def check(self, prompt: Prompt) -> FilterResult:
        """
        Check if a prompt violates any content policies.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed.
        """
        violations = {}

        for policy_name, filter_obj in self.policies.items():
            result = filter_obj.check(prompt)
            if not result.passed:
                violations[policy_name] = result.reason

        if violations:
            return FilterResult(
                passed=False,
                reason="Prompt violates content policies",
                details={"violations": violations},
            )

        return FilterResult(passed=True)
