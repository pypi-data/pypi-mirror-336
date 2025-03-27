"""
Prompt repository for version control of prompts.
"""

import json
import os
import re
import shutil
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import semver

from promptflow.core.prompt import Prompt
from promptflow.core.types import PromptMetadata


class PromptRepo:
    """
    A repository for managing and versioning prompts.
    """

    def __init__(self, repo_path: str):
        """
        Initialize a prompt repository.

        Args:
            repo_path: Path to the repository.
        """
        self.repo_path = os.path.abspath(repo_path)
        self._ensure_repo_exists()

    def _ensure_repo_exists(self) -> None:
        """Ensure the repository directory exists."""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        # Create a .promptflow directory for metadata
        meta_dir = os.path.join(self.repo_path, ".promptflow")
        if not os.path.exists(meta_dir):
            os.makedirs(meta_dir)

    def _get_prompt_dir(self, prompt_name: str) -> str:
        """Get the directory for a prompt."""
        return os.path.join(self.repo_path, prompt_name)

    def _get_version_dir(self, prompt_name: str, version: str) -> str:
        """Get the directory for a specific version of a prompt."""
        return os.path.join(self._get_prompt_dir(prompt_name), version)

    def _get_prompt_file(self, prompt_name: str, version: str) -> str:
        """Get the file path for a specific version of a prompt."""
        return os.path.join(
            self._get_version_dir(
                prompt_name,
                version),
            "prompt.json")

    def _get_meta_file(self, prompt_name: str) -> str:
        """Get the metadata file for a prompt."""
        return os.path.join(self._get_prompt_dir(prompt_name), "meta.json")

    def create_prompt(self, prompt_name: str) -> Prompt:
        """
        Create a new prompt.

        Args:
            prompt_name: Name of the prompt.

        Returns:
            A new Prompt object.
        """
        # Create a new empty prompt
        prompt = Prompt(messages=[])

        # Add metadata
        prompt.metadata = PromptMetadata(
            version="0.1.0",
            description=f"Prompt: {prompt_name}",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        return prompt

    def save_prompt(
        self,
        prompt_name: str,
        prompt: Prompt,
        version: Optional[str] = None,
        message: Optional[str] = None,
    ) -> str:
        """
        Save a prompt to the repository.

        Args:
            prompt_name: Name of the prompt.
            prompt: The prompt to save.
            version: Version of the prompt (default: auto-increment).
            message: Commit message.

        Returns:
            The version of the saved prompt.
        """
        # Make sure the prompt directory exists
        prompt_dir = self._get_prompt_dir(prompt_name)
        if not os.path.exists(prompt_dir):
            os.makedirs(prompt_dir)

        # Determine the version
        if version is None:
            version = self._get_next_version(prompt_name)

        # Update the prompt metadata
        if prompt.metadata is None:
            prompt.metadata = PromptMetadata(
                version=version,
                description=f"Prompt: {prompt_name}",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
            )
        else:
            prompt.metadata.version = version
            prompt.metadata.updated_at = datetime.now().isoformat()

        # Create the version directory
        version_dir = self._get_version_dir(prompt_name, version)
        if not os.path.exists(version_dir):
            os.makedirs(version_dir)

        # Save the prompt file
        prompt_file = self._get_prompt_file(prompt_name, version)
        with open(prompt_file, "w") as f:
            f.write(prompt.to_json())

        # Save metadata
        meta_file = self._get_meta_file(prompt_name)
        meta = {
            "name": prompt_name,
            "latest_version": version,
            "versions": self.list_versions(prompt_name),
            "updated_at": datetime.now().isoformat(),
        }

        if message:
            meta["message"] = message

        # Append this version
        if "versions" not in meta:
            meta["versions"] = []

        if version not in meta["versions"]:
            meta["versions"].append(version)

        with open(meta_file, "w") as f:
            json.dump(meta, f, indent=2)

        return version

    def get_prompt(
            self,
            prompt_name: str,
            version: Optional[str] = None) -> Prompt:
        """
        Get a prompt from the repository.

        Args:
            prompt_name: Name of the prompt.
            version: Version of the prompt (default: latest).

        Returns:
            The prompt.

        Raises:
            FileNotFoundError: If the prompt or version does not exist.
        """
        # If no version is specified, get the latest version
        if version is None:
            version = self.get_latest_version(prompt_name)

        # Make sure the prompt exists
        prompt_file = self._get_prompt_file(prompt_name, version)
        if not os.path.exists(prompt_file):
            raise FileNotFoundError(
                f"Prompt '{prompt_name}' version '{version}' not found")

        # Load the prompt
        with open(prompt_file, "r") as f:
            prompt_data = json.load(f)

        return Prompt.from_dict(prompt_data)

    def list_prompts(self) -> List[str]:
        """
        List all prompts in the repository.

        Returns:
            A list of prompt names.
        """
        prompts = []

        # Iterate through all directories in the repository
        for item in os.listdir(self.repo_path):
            item_path = os.path.join(self.repo_path, item)

            # Skip files and hidden directories
            if os.path.isfile(item_path) or item.startswith("."):
                continue

            # Check if the directory contains any versions
            versions_exist = False
            for subitem in os.listdir(item_path):
                if re.match(r"^\d+\.\d+\.\d+$", subitem):
                    versions_exist = True
                    break

            if versions_exist:
                prompts.append(item)

        return prompts

    def list_versions(self, prompt_name: str) -> List[str]:
        """
        List all versions of a prompt.

        Args:
            prompt_name: Name of the prompt.

        Returns:
            A list of version strings.
        """
        versions = []

        # Get the prompt directory
        prompt_dir = self._get_prompt_dir(prompt_name)
        if not os.path.exists(prompt_dir):
            return versions

        # Iterate through all directories in the prompt directory
        for item in os.listdir(prompt_dir):
            item_path = os.path.join(prompt_dir, item)

            # Skip files and directories that don't match version format
            if os.path.isfile(item_path) or not re.match(
                    r"^\d+\.\d+\.\d+$", item):
                continue

            versions.append(item)

        # Sort versions
        versions.sort(key=lambda v: semver.VersionInfo.parse(v))

        return versions

    def get_latest_version(self, prompt_name: str) -> str:
        """
        Get the latest version of a prompt.

        Args:
            prompt_name: Name of the prompt.

        Returns:
            The latest version.

        Raises:
            FileNotFoundError: If the prompt does not exist or has no versions.
        """
        versions = self.list_versions(prompt_name)

        if not versions:
            raise FileNotFoundError(f"Prompt '{prompt_name}' has no versions")

        return versions[-1]

    def _get_next_version(self, prompt_name: str) -> str:
        """
        Get the next version for a prompt.

        Args:
            prompt_name: Name of the prompt.

        Returns:
            The next version.
        """
        try:
            latest = self.get_latest_version(prompt_name)
            version_info = semver.VersionInfo.parse(latest)
            return str(version_info.bump_patch())
        except FileNotFoundError:
            return "0.1.0"

    def delete_prompt(self, prompt_name: str) -> None:
        """
        Delete a prompt and all its versions.

        Args:
            prompt_name: Name of the prompt.

        Raises:
            FileNotFoundError: If the prompt does not exist.
        """
        prompt_dir = self._get_prompt_dir(prompt_name)

        if not os.path.exists(prompt_dir):
            raise FileNotFoundError(f"Prompt '{prompt_name}' not found")

        shutil.rmtree(prompt_dir)

    def delete_version(self, prompt_name: str, version: str) -> None:
        """
        Delete a specific version of a prompt.

        Args:
            prompt_name: Name of the prompt.
            version: Version to delete.

        Raises:
            FileNotFoundError: If the prompt or version does not exist.
        """
        version_dir = self._get_version_dir(prompt_name, version)

        if not os.path.exists(version_dir):
            raise FileNotFoundError(
                f"Prompt '{prompt_name}' version '{version}' not found")

        shutil.rmtree(version_dir)

        # Update metadata
        meta_file = self._get_meta_file(prompt_name)
        if os.path.exists(meta_file):
            with open(meta_file, "r") as f:
                meta = json.load(f)

            if "versions" in meta and version in meta["versions"]:
                meta["versions"].remove(version)

            # If this was the latest version, update it
            if meta.get("latest_version") == version:
                versions = self.list_versions(prompt_name)
                if versions:
                    meta["latest_version"] = versions[-1]
                else:
                    meta.pop("latest_version", None)

            with open(meta_file, "w") as f:
                json.dump(meta, f, indent=2)

    def compare_versions(self, prompt_name: str,
                         version1: str, version2: str) -> Dict[str, Any]:
        """
        Compare two versions of a prompt.

        Args:
            prompt_name: Name of the prompt.
            version1: First version.
            version2: Second version.

        Returns:
            A dictionary with differences between the versions.

        Raises:
            FileNotFoundError: If either version does not exist.
        """
        prompt1 = self.get_prompt(prompt_name, version1)
        prompt2 = self.get_prompt(prompt_name, version2)

        # Compare messages
        messages1 = [m.model_dump() for m in prompt1.messages]
        messages2 = [m.model_dump() for m in prompt2.messages]

        return {
            "message_count_diff": len(messages2) - len(messages1),
            "messages_added": len(messages2) > len(messages1),
            "messages_removed": len(messages2) < len(messages1),
            "metadata_diff": prompt2.metadata != prompt1.metadata,
            "parameters_diff": prompt2.parameters != prompt1.parameters,
        }
