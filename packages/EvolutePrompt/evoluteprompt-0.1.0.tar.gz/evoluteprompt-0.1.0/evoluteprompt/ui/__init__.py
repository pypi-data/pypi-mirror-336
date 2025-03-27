"""
UI components for PromptFlow.
"""

# Don't import streamlit modules here - they'll be imported on demand
# when the functions are called


def run_streamlit_app():
    """Run the Streamlit app."""
    # Only import streamlit when this function is called
    from promptflow.ui.streamlit_app import main

    return main()


__all__ = ["run_streamlit_app"]
