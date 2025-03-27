"""
Streamlit UI for EvolutePrompt LLM Prompt Management and Testing.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import streamlit as st

from evoluteprompt.api import EvolutePrompt
from evoluteprompt.core.prompt import Prompt, PromptBuilder
from evoluteprompt.core.types import Message, MessageRole, PromptCategory

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.flow = None
    st.session_state.prompts = []
    st.session_state.current_prompt = None
    st.session_state.current_version = None
    st.session_state.versions = []
    st.session_state.test_input = ""
    st.session_state.test_result = ""
    st.session_state.test_prompt = None


def initialize_flow():
    """Initialize the PromptFlow instance."""
    if not st.session_state.initialized:
        # Initialize PromptFlow
        flow = EvolutePrompt()
        flow.init()
        st.session_state.flow = flow
        st.session_state.initialized = True

        # Load prompts
        refresh_prompts()


def refresh_prompts():
    """Refresh the list of prompts."""
    if st.session_state.flow:
        st.session_state.prompts = st.session_state.flow.list_prompts()


def load_versions(prompt_name):
    """Load versions for a prompt."""
    if st.session_state.flow and prompt_name:
        st.session_state.versions = st.session_state.flow.list_versions(
            prompt_name)
        if st.session_state.versions:
            # Latest version
            st.session_state.current_version = st.session_state.versions[-1]


def load_prompt(prompt_name, version=None):
    """Load a prompt."""
    if st.session_state.flow and prompt_name:
        prompt = st.session_state.flow.get_prompt(prompt_name, version)
        st.session_state.current_prompt = prompt
        return prompt
    return None


def create_new_prompt(
        name,
        system_message,
        user_message,
        category,
        tags,
        description):
    """Create a new prompt."""
    if st.session_state.flow:
        # Create prompt
        builder = st.session_state.flow.create_prompt()
        if system_message:
            builder.add_system(system_message)
        if user_message:
            builder.add_user(user_message)

        # Build the prompt - allow it to be created without a user message
        has_user_message = bool(user_message)
        prompt = builder.build(require_user_message=has_user_message)

        # Add metadata
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
        prompt.update_metadata(
            description=description,
            tags=tag_list,
            category=category,
            is_active=True)

        # Save prompt
        version = st.session_state.flow.save_prompt(name, prompt)

        # Refresh prompts
        refresh_prompts()

        return version
    return None


def set_active_prompt(prompt_name, version):
    """Set a prompt as active."""
    if st.session_state.flow:
        st.session_state.flow.set_active(prompt_name, version)


def set_fallback_prompt(prompt_name, version, fallback_for):
    """Set a prompt as a fallback."""
    if st.session_state.flow:
        st.session_state.flow.set_fallback(prompt_name, version, fallback_for)


def test_prompt(prompt, test_input):
    """Test a prompt with input."""
    if not prompt:
        return "No prompt selected"

    # Create a copy of the prompt
    builder = st.session_state.flow.create_prompt()

    # Add system messages
    for msg in prompt.messages:
        if msg.role == MessageRole.SYSTEM:
            builder.add_system(msg.content)

    # Add the test input as user message if provided
    if test_input:
        builder.add_user(test_input)
    else:
        # Copy any existing user messages from the original prompt
        for msg in prompt.messages:
            if msg.role == MessageRole.USER:
                builder.add_user(msg.content)

    # Build the test prompt - include a user message only if we have one
    has_user_message = test_input or any(
        msg.role == MessageRole.USER for msg in builder._messages)
    test_prompt = builder.build(require_user_message=has_user_message)

    # Save the test prompt for display
    st.session_state.test_prompt = test_prompt

    # In a real application, you would send this to an LLM provider
    # For now, we'll just return a placeholder
    return f"This is where the LLM response would appear. The prompt has {
        len(
            test_prompt.messages)} messages."


def render_sidebar():
    """Render the sidebar."""
    st.sidebar.title("PromptFlow UI")

    # Initialize button
    if not st.session_state.initialized:
        if st.sidebar.button("Initialize PromptFlow"):
            initialize_flow()
    else:
        st.sidebar.success("PromptFlow initialized")

        # Navigation
        st.sidebar.header("Navigation")
        page = st.sidebar.radio(
            "Select Page", [
                "Prompt Management", "Prompt Testing", "Settings"])

        # Refresh button
        if st.sidebar.button("Refresh Prompts"):
            refresh_prompts()

        return page

    return None


def render_prompt_management():
    """Render the prompt management page."""
    st.title("Prompt Management")

    # Tabs for different actions
    tab1, tab2, tab3 = st.tabs(
        ["Create Prompt", "View/Edit Prompts", "Fallback Configuration"])

    with tab1:
        st.header("Create New Prompt")

        # Form for creating a new prompt
        with st.form("create_prompt_form"):
            name = st.text_input("Prompt Name", key="new_prompt_name")
            system_message = st.text_area(
                "System Message", key="new_system_message")
            user_message = st.text_area("User Message", key="new_user_message")

            # Metadata
            st.subheader("Metadata")
            category = st.selectbox(
                "Category",
                options=[
                    c.value for c in PromptCategory],
                key="new_category")
            tags = st.text_input("Tags (comma separated)", key="new_tags")
            description = st.text_area("Description", key="new_description")

            submitted = st.form_submit_button("Create Prompt")

            if submitted:
                if name:
                    version = create_new_prompt(
                        name,
                        system_message,
                        user_message,
                        PromptCategory(category),
                        tags,
                        description,
                    )
                    if version:
                        st.success(
                            f"Prompt '{name}' created with version {version}")
                else:
                    st.error("Prompt name is required")

    with tab2:
        st.header("View/Edit Prompts")

        # Prompt selection
        if st.session_state.prompts:
            prompt_name = st.selectbox(
                "Select Prompt",
                options=st.session_state.prompts,
                key="view_prompt_name",
                on_change=lambda: load_versions(
                    st.session_state.view_prompt_name),
            )

            # Version selection
            if st.session_state.versions:
                version = st.selectbox(
                    "Select Version",
                    options=st.session_state.versions,
                    key="view_version",
                    on_change=lambda: load_prompt(
                        prompt_name,
                        st.session_state.view_version),
                )

                # Load the prompt if not already loaded
                if (
                    not st.session_state.current_prompt
                    or st.session_state.current_version != version
                ):
                    prompt = load_prompt(prompt_name, version)
                    st.session_state.current_version = version
                else:
                    prompt = st.session_state.current_prompt

                if prompt:
                    # Display prompt details
                    st.subheader("Prompt Details")

                    # Messages
                    st.write("**Messages:**")
                    for i, msg in enumerate(prompt.messages):
                        st.text_area(
                            f"{msg.role.value.capitalize()} Message {i + 1}",
                            value=msg.content,
                            key=f"msg_{i}",
                            disabled=True,
                        )

                    # Metadata
                    if prompt.metadata:
                        st.write("**Metadata:**")
                        metadata_dict = prompt.metadata.dict()
                        metadata_str = json.dumps(metadata_dict, indent=2)
                        st.code(metadata_str, language="json")

                    # Set as active button
                    if st.button("Set as Active Version"):
                        set_active_prompt(prompt_name, version)
                        st.success(
                            f"Set {prompt_name} version {version} as active")
            else:
                st.info("No versions found for this prompt")
        else:
            st.info("No prompts found. Create a prompt first.")

    with tab3:
        st.header("Fallback Configuration")

        # Form for setting fallback prompts
        with st.form("fallback_form"):
            # Primary prompt selection
            primary_prompt = st.selectbox(
                "Primary Prompt",
                options=st.session_state.prompts,
                key="primary_prompt")

            # Fallback prompt selection
            fallback_prompt = st.selectbox(
                "Fallback Prompt",
                options=st.session_state.prompts,
                key="fallback_prompt")

            # Only show version selection if prompts are selected
            if primary_prompt and fallback_prompt:
                # Load versions for fallback prompt
                fallback_versions = st.session_state.flow.list_versions(
                    fallback_prompt)

                if fallback_versions:
                    fallback_version = st.selectbox(
                        "Fallback Version", options=fallback_versions, key="fallback_version")

                    submitted = st.form_submit_button("Set Fallback")

                    if submitted:
                        set_fallback_prompt(
                            fallback_prompt, fallback_version, primary_prompt)
                        st.success(
                            f"Set {fallback_prompt} version {fallback_version} as fallback for {primary_prompt}")
                else:
                    st.info("No versions found for the fallback prompt")
                    st.form_submit_button("Set Fallback", disabled=True)
            else:
                st.form_submit_button("Set Fallback", disabled=True)


def render_prompt_testing():
    """Render the prompt testing page."""
    st.title("Prompt Testing")

    # Prompt selection for testing
    if st.session_state.prompts:
        col1, col2 = st.columns([1, 1])

        with col1:
            prompt_name = st.selectbox(
                "Select Prompt",
                options=st.session_state.prompts,
                key="test_prompt_name",
                on_change=lambda: load_versions(
                    st.session_state.test_prompt_name),
            )

        with col2:
            # Version selection
            version = None  # Initialize version to None
            if "versions" in st.session_state and st.session_state.versions:
                version = st.selectbox(
                    "Select Version",
                    options=st.session_state.versions,
                    key="test_version")

                # Add option to use active version
                use_active = st.checkbox(
                    "Use Active Version", value=True, key="use_active")
            else:
                st.info("No versions found")
                use_active = True  # Default to active version if no versions found

        # Load the prompt
        if prompt_name:
            if use_active:
                prompt = st.session_state.flow.get_active_prompt(prompt_name)
                if not prompt:
                    st.warning(
                        f"No active version found for {prompt_name}. Using latest version.")
                    prompt = st.session_state.flow.get_prompt(prompt_name)
            else:
                # Only use version parameter if it's actually defined
                if version is not None:
                    prompt = st.session_state.flow.get_prompt(
                        prompt_name, version)
                else:
                    prompt = st.session_state.flow.get_prompt(prompt_name)

            if prompt:
                # Display prompt details
                with st.expander("Prompt Details", expanded=False):
                    # Messages
                    st.write("**Messages:**")
                    for i, msg in enumerate(prompt.messages):
                        st.text_area(
                            f"{msg.role.value.capitalize()} Message {i + 1}",
                            value=msg.content,
                            key=f"test_msg_{i}",
                            disabled=True,
                        )

                # Test input
                st.subheader("Test Input")
                test_input = st.text_area(
                    "Enter test input", key="test_input_text")

                if st.button("Test Prompt"):
                    result = test_prompt(prompt, test_input)
                    st.session_state.test_result = result

                # Display test result
                if st.session_state.test_result:
                    st.subheader("Test Result")
                    st.write(st.session_state.test_result)

                    # Display the full test prompt
                    if st.session_state.test_prompt:
                        with st.expander("Full Test Prompt", expanded=False):
                            for i, msg in enumerate(
                                    st.session_state.test_prompt.messages):
                                st.text_area(
                                    f"{msg.role.value.capitalize()} Message {i + 1}",
                                    value=msg.content,
                                    key=f"full_test_msg_{i}",
                                    disabled=True,
                                )
            else:
                st.error("Failed to load prompt")
    else:
        st.info("No prompts found. Create a prompt first.")


def render_settings():
    """Render the settings page."""
    st.title("Settings")

    # Database settings
    st.header("Database Settings")

    # Display current database path
    if st.session_state.flow:
        st.write(
            f"**Current Database URL:** {st.session_state.flow.repo.db_url}")

    # Option to change database path
    new_db_path = st.text_input(
        "New Database Path (relative to current directory)")

    if st.button("Change Database") and new_db_path:
        # Close current connection
        if st.session_state.flow:
            st.session_state.flow.close()

        # Initialize with new path
        flow = EvolutePrompt(f"sqlite://{os.path.abspath(new_db_path)}")
        flow.init()
        st.session_state.flow = flow
        st.session_state.initialized = True

        # Refresh prompts
        refresh_prompts()

        st.success(f"Database changed to {new_db_path}")

    # Export/Import
    st.header("Export/Import")

    # Export
    if st.button("Export All Prompts"):
        st.info("Export functionality would be implemented here")

    # Import
    uploaded_file = st.file_uploader("Import Prompts", type=["json"])
    if uploaded_file is not None:
        st.info("Import functionality would be implemented here")


def main():
    """Main function."""
    # Set page config
    st.set_page_config(
        page_title="EvolutePrompt UI",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Render sidebar and get selected page
    page = render_sidebar()

    # Render selected page (only if a page is actually selected)
    if page is not None:
        if page == "Prompt Management":
            render_prompt_management()
        elif page == "Prompt Testing":
            render_prompt_testing()
        elif page == "Settings":
            render_settings()
    else:
        # Welcome page
        st.title("Welcome to EvolutePrompt UI")
        st.write("Please initialize EvolutePrompt using the button in the sidebar.")


if __name__ == "__main__":
    main()
