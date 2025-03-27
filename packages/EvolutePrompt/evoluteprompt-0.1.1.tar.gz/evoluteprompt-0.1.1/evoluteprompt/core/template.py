"""
Template functionality for the EvolutePrompt library.
"""

import re
from typing import Any, Dict, List, Optional, Union

from jinja2 import Template as JinjaTemplate
from pydantic import BaseModel

from evoluteprompt.core.prompt import Prompt, PromptBuilder
from evoluteprompt.core.types import MessageRole


class PromptTemplate(BaseModel):
    """
    A template for a prompt that can be rendered with variables.
    """

    template: str
    variables: Dict[str, Any] = {}

    @classmethod
    def from_string(cls, template_str: str, variables: Dict[str, Any] = None):
        """
        Create a template from a string.

        Args:
            template_str: The template string.
            variables: Optional default variables for the template.

        Returns:
            A PromptTemplate object.
        """
        return cls(template=template_str, variables=variables or {})

    def render(self, **kwargs) -> str:
        """
        Render the template with the given variables.

        Args:
            **kwargs: Variables to render the template with.

        Returns:
            The rendered template.
        """
        # Merge provided variables with default variables
        variables = {**self.variables, **kwargs}

        # Create a Jinja template and render it
        jinja_template = JinjaTemplate(self.template)
        return jinja_template.render(**variables)

    def to_prompt(
        self,
        role: Union[str, MessageRole] = MessageRole.USER,
        require_user_message: bool = True,
        **kwargs,
    ) -> Prompt:
        """
        Convert the template to a prompt with a single message.

        Args:
            role: The role of the message (default: USER).
            require_user_message: If False, allows creating a prompt without any user message.
                                 If using a non-USER role, set this to False to avoid requiring a user message.
            **kwargs: Variables to render the template with.

        Returns:
            A Prompt object with a single message.
        """
        rendered = self.render(**kwargs)

        builder = PromptBuilder()
        builder.add_message(role, rendered)

        return builder.build(require_user_message=require_user_message)

    @classmethod
    def from_file(cls, file_path: str) -> "PromptTemplate":
        """
        Create a template from a file.

        Args:
            file_path: The path to the file.

        Returns:
            A PromptTemplate object.
        """
        with open(file_path, "r") as f:
            template_content = f.read()

        return cls(template=template_content)


class MultiMessageTemplate(BaseModel):
    """
    A template for a prompt with multiple messages.
    """

    system_template: Optional[str] = None
    user_templates: List[str] = []
    assistant_templates: List[str] = []
    variables: Dict[str, Any] = {}

    def render(self, **kwargs) -> List[Dict[str, str]]:
        """
        Render all templates with the given variables.

        Args:
            **kwargs: Variables to render the templates with.

        Returns:
            A list of rendered messages.
        """
        # Merge provided variables with default variables
        variables = {**self.variables, **kwargs}

        messages = []

        # Add system message if provided
        if self.system_template:
            system_template = JinjaTemplate(self.system_template)
            messages.append({"role": "system",
                             "content": system_template.render(**variables)})

        # Add user and assistant messages alternating
        max_len = max(len(self.user_templates), len(self.assistant_templates))

        for i in range(max_len):
            # Add user message if available
            if i < len(self.user_templates):
                user_template = JinjaTemplate(self.user_templates[i])
                messages.append({"role": "user",
                                 "content": user_template.render(**variables)})

            # Add assistant message if available
            if i < len(self.assistant_templates):
                assistant_template = JinjaTemplate(self.assistant_templates[i])
                messages.append(
                    {"role": "assistant", "content": assistant_template.render(**variables)}
                )

        return messages

    def to_prompt(self, require_user_message: bool = True, **kwargs) -> Prompt:
        """
        Convert the template to a prompt with multiple messages.

        Args:
            require_user_message: If False, allows creating a prompt without any user message.
            **kwargs: Variables to render the templates with.

        Returns:
            A Prompt object with multiple messages.
        """
        rendered_messages = self.render(**kwargs)

        builder = PromptBuilder()
        for message in rendered_messages:
            builder.add_message(message["role"], message["content"])

        return builder.build(require_user_message=require_user_message)

    @classmethod
    def from_file(
            cls,
            file_path: str,
            delimiter: str = "---") -> "MultiMessageTemplate":
        """
        Create a template from a file with multiple sections separated by a delimiter.

        The file format should be:

        system
        <system template>
        ---
        user
        <user template 1>
        ---
        assistant
        <assistant template 1>
        ---
        user
        <user template 2>
        ...

        Args:
            file_path: The path to the file.
            delimiter: The delimiter separating sections (default: "---").

        Returns:
            A MultiMessageTemplate object.
        """
        with open(file_path, "r") as f:
            content = f.read()

        sections = content.split(delimiter)

        system_template = None
        user_templates = []
        assistant_templates = []

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Get the role from the first line
            lines = section.split("\n")
            role = lines[0].strip().lower()

            # Get the content from the rest of the lines
            content = "\n".join(lines[1:]).strip()

            if role == "system":
                system_template = content
            elif role == "user":
                user_templates.append(content)
            elif role == "assistant":
                assistant_templates.append(content)

        return cls(
            system_template=system_template,
            user_templates=user_templates,
            assistant_templates=assistant_templates,
        )
