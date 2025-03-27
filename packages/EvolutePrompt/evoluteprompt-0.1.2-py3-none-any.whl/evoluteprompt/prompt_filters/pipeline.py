"""
Filter pipeline to combine multiple prompt filters.
"""

from typing import Any, Dict, List, Optional

from evoluteprompt.core.prompt import Prompt
from evoluteprompt.prompt_filters.base import FilterResult, PromptFilter


class FilterPipeline(PromptFilter):
    """
    A pipeline of prompt filters that are applied in sequence.
    """

    def __init__(
            self,
            filters: List[PromptFilter],
            name: Optional[str] = None):
        """
        Initialize a filter pipeline.

        Args:
            filters: List of filters to apply in sequence.
            name: Name of the filter pipeline.
        """
        super().__init__(name=name or "FilterPipeline")
        self.filters = filters

    def check(self, prompt: Prompt) -> FilterResult:
        """
        Check if a prompt passes all filters in the pipeline.

        Args:
            prompt: The prompt to check.

        Returns:
            A FilterResult indicating whether the prompt passed all filters.
            If any filter fails, the result will indicate failure with
            information about which filter failed.
        """
        results = {}

        for filter_obj in self.filters:
            result = filter_obj.check(prompt)
            results[filter_obj.name] = result

            if not result.passed:
                return FilterResult(
                    passed=False,
                    reason=f"Filter '{filter_obj.name}' failed: {result.reason}",
                    details={
                        "failed_filter": filter_obj.name,
                        "failed_reason": result.reason,
                        "failed_details": result.details,
                        "filter_results": {
                            name: {"passed": res.passed, "reason": res.reason}
                            for name, res in results.items()
                        },
                    },
                )

        return FilterResult(
            passed=True,
            details={
                "filter_results": {
                    name: {"passed": res.passed, "reason": res.reason}
                    for name, res in results.items()
                }
            },
        )

    def add_filter(self, filter_obj: PromptFilter) -> "FilterPipeline":
        """
        Add a filter to the pipeline.

        Args:
            filter_obj: The filter to add.

        Returns:
            The updated filter pipeline.
        """
        self.filters.append(filter_obj)
        return self
