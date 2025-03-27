"""
Utilities for hashing prompts and responses.
"""

import hashlib
import json
from typing import Any, Dict, Optional

from evoluteprompt.core.prompt import Prompt


def hash_prompt(prompt: Prompt, include_parameters: bool = True) -> str:
    """
    Create a hash of a prompt to use as a cache key.

    Args:
        prompt: The prompt to hash.
        include_parameters: Whether to include the prompt parameters in the hash.

    Returns:
        A hash string that uniquely identifies the prompt.
    """
    # Create a dictionary of the parts we want to hash
    to_hash = {
        "messages": [
            {
                "role": msg.role.value,
                "content": msg.content,
                **({"name": msg.name} if msg.name else {}),
            }
            for msg in prompt.messages
        ]
    }

    # Include parameters if requested
    if include_parameters and prompt.parameters:
        # Convert to dict and filter out None values
        params_dict = prompt.parameters.model_dump(exclude_none=True)

        # Special handling for functions, which may contain complex objects
        if "functions" in params_dict:
            functions = []
            for func in params_dict["functions"]:
                if isinstance(func, dict):
                    functions.append(func)
                else:
                    functions.append(func.model_dump(exclude_none=True))
            params_dict["functions"] = functions

        to_hash["parameters"] = params_dict

    # Convert to JSON and hash
    json_str = json.dumps(to_hash, sort_keys=True)
    hash_obj = hashlib.sha256(json_str.encode())

    return hash_obj.hexdigest()


def dict_hash(d: Dict[str, Any]) -> str:
    """
    Create a hash of a dictionary.

    Args:
        d: The dictionary to hash.

    Returns:
        A hash string that uniquely identifies the dictionary.
    """
    json_str = json.dumps(d, sort_keys=True)
    hash_obj = hashlib.sha256(json_str.encode())

    return hash_obj.hexdigest()
