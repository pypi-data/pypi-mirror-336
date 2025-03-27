"""
EvolutePrompt: A comprehensive prompt management library for Large Language Models.
"""

__version__ = "0.1.0"

from evoluteprompt.api import EvolutePrompt
from evoluteprompt.core.database import DBPromptRepo
from evoluteprompt.core.prompt import Prompt, PromptBuilder
from evoluteprompt.core.provider import LLMProvider
from evoluteprompt.core.repository import PromptRepo
from evoluteprompt.core.response import LLMResponse
from evoluteprompt.core.strategy import (
    ABTestingPromptStrategy,
    ActivePromptStrategy,
    CategoryPromptStrategy,
    ConditionalPromptStrategy,
    ContextAwarePromptStrategy,
    FallbackPromptStrategy,
    LatestPromptStrategy,
    PromptSelector,
    PromptStrategy,
)
from evoluteprompt.core.template import MultiMessageTemplate, PromptTemplate
from evoluteprompt.core.types import (
    Message,
    MessageRole,
    PromptCategory,
    PromptMetadata,
    PromptParameters,
    PromptStats,
)

# Define UI availability flag without importing Streamlit
HAS_UI = False


# Define a function to get UI components only when needed
def get_ui_components():
    """Get UI components if streamlit is installed."""
    try:
        from evoluteprompt.ui import run_streamlit_app

        return {"run_streamlit_app": run_streamlit_app}
    except ImportError:
        raise ImportError(
            "Streamlit is not installed. Install with 'pip install streamlit' "
            "or 'pip install evoluteprompt[ui]' to use UI components."
        )


__all__ = [
    # Core classes
    "Prompt",
    "PromptBuilder",
    "PromptTemplate",
    "MultiMessageTemplate",
    "PromptRepo",
    "LLMProvider",
    "LLMResponse",
    # Database
    "DBPromptRepo",
    # Strategies
    "PromptStrategy",
    "ActivePromptStrategy",
    "FallbackPromptStrategy",
    "LatestPromptStrategy",
    "ConditionalPromptStrategy",
    "ABTestingPromptStrategy",
    "ContextAwarePromptStrategy",
    "CategoryPromptStrategy",
    "PromptSelector",
    # Types
    "MessageRole",
    "Message",
    "PromptMetadata",
    "PromptParameters",
    "PromptStats",
    "PromptCategory",
    # High-level API
    "EvolutePrompt",
    # UI
    "HAS_UI",
    "get_ui_components",
]
