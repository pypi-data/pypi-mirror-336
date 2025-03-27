# PromptFlow

A comprehensive prompt management library for Large Language Models with built-in version control, storage, and activation strategies.

## Features

- **Prompt Version Control & Storage**: Keep track of prompt versions and their changes over time
- **SQLite Database Integration**: Lightweight persistence using Tortoise ORM with SQLite
- **Dynamic Prompt Switching & Activation Logic**: Flexible strategies for prompt selection
- **Prompt Categorization**: Organize prompts by use case (Chat, Search, Summarization, etc.)
- **Fallback Prompts**: Define fallback prompts when primary prompts fail
- **Easy-to-use Python API**: Simple to embed and use in your applications
- **Strong Schema Validation**: Type-safety with Pydantic
- **Optional FastAPI Integration**: Expose prompt management via REST API
- **Native Streamlit UI**: Visual interface for prompt management and testing
- **LangChain Integration**: Use PromptFlow with LangChain for enhanced prompt management

## Installation

```bash
# Basic installation
pip install promptflow

# With UI support
pip install promptflow[ui]

# With API and UI support
pip install promptflow[all]
```

## Quick Start

```python
from promptflow import PromptFlow
from promptflow import PromptCategory

# Initialize PromptFlow
flow = PromptFlow()
flow.init()

# Create a prompt
prompt_builder = flow.create_prompt()
prompt_builder.add_system("You are a helpful assistant.")
prompt_builder.add_user("What is the capital of France?")
prompt = prompt_builder.build()

# Add metadata
prompt.update_metadata(
    description="A simple geography question",
    tags=["geography", "test"],
    category=PromptCategory.QA
)

# Save the prompt
version = flow.save_prompt("capital_question", prompt)
print(f"Saved prompt version: {version}")

# Retrieve the prompt
retrieved = flow.get_prompt("capital_question")
```

## Using the UI

PromptFlow includes a native Streamlit UI for prompt management and testing. To use it:

```bash
# If installed with pip
promptflow ui

# Or directly from the module
python -m promptflow.cli ui
```

The UI provides:
- Prompt creation and management
- Version control and history
- Fallback configuration
- Prompt testing interface
- Database settings

## Templates

```python
# Create a template
template = flow.template_from_string(
    "What is the capital of {{country}}?", 
    variables={"country": "France"}
)

# Render the template
rendered = template.render()

# Or with different variables
rendered = template.render(country="Germany")
```

## Strategies

```python
# Simple active prompt selection
prompt = flow.get_active_prompt("my_prompt")

# With fallback
strategy = flow.with_fallback()
prompt = flow.select_prompt("my_prompt", strategy=strategy)

# A/B testing
ab_strategy = flow.create_ab_testing(
    prompt_variants=["prompt_a", "prompt_b"],
    weights=[0.7, 0.3]
)
prompt = flow.select_prompt("doesn't_matter", strategy=ab_strategy)

# Context-aware selection
context_strategy = flow.create_context_aware(
    context_key="language",
    prompt_mapping={
        "en": "english_prompt",
        "es": "spanish_prompt",
        "fr": "french_prompt"
    }
)
prompt = flow.select_prompt(
    "fallback_prompt", 
    strategy=context_strategy,
    context={"language": "es"}
)
```

## FastAPI Integration

```python
# See examples/fastapi_integration.py for a complete example
```

## LangChain Integration

PromptFlow can be easily integrated with LangChain to combine robust prompt management with LangChain's orchestration capabilities:

```python
# Convert a PromptFlow prompt to LangChain format
def promptflow_to_langchain_messages(pf_prompt):
    lc_messages = []
    for msg in pf_prompt.messages:
        if msg.role.value == "system":
            lc_messages.append(SystemMessage(content=msg.content))
        elif msg.role.value == "user":
            lc_messages.append(HumanMessage(content=msg.content))
    return lc_messages

# Use PromptFlow's versioning with LangChain
prompt = flow.get_active_prompt("my_prompt")
lc_messages = promptflow_to_langchain_messages(prompt)
result = llm.generate([lc_messages])
```

For detailed examples, see [LangChain Integration](docs/langchain_integration.md).

## Version Control

```python
# List all prompts
prompts = flow.list_prompts()

# List all versions of a prompt
versions = flow.list_versions("my_prompt")

# Get a specific version
prompt = flow.get_prompt("my_prompt", version="0.1.0")

# Set a version as active
flow.set_active("my_prompt", "0.2.0")
```

## Development

For information about setting up the development environment, running tests, and contributing to PromptFlow, see the following resources:

- [Testing Documentation](docs/testing.md): Instructions for running and writing tests
- [Contributing Guidelines](CONTRIBUTING.md): Guidelines for contributing to the project

## License

MIT
