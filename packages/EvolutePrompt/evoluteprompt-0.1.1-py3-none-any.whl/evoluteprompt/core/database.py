"""
Database storage for prompts using Tortoise ORM.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union

from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from evoluteprompt.core.prompt import Prompt
from evoluteprompt.core.types import PromptCategory, PromptMetadata, PromptParameters, PromptStats


class BaseModel(models.Model):
    """Base model with common fields."""

    id = fields.IntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Prompt(BaseModel):
    """Model for storing prompts."""

    name = fields.CharField(max_length=255)
    version = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
    template = fields.TextField()
    variables = fields.JSONField(default=dict)
    metadata = fields.JSONField(default=dict)
    tags = fields.JSONField(default=list)

    class Meta:
        table = "prompts"
        unique_together = [("name", "version")]


class PromptStats(BaseModel):
    """Model for storing prompt usage statistics."""

    prompt = fields.ForeignKeyField(
        "models.Prompt",
        related_name="stats",
        on_delete=fields.CASCADE)
    total_uses = fields.IntField(default=0)
    successful_uses = fields.IntField(default=0)
    failed_uses = fields.IntField(default=0)
    last_used = fields.DatetimeField(null=True)

    class Meta:
        table = "prompt_stats"


# Create Pydantic models
PromptInDB = pydantic_model_creator(
    Prompt, name="PromptInDB", exclude=(
        "created_at", "updated_at"))


class PromptModel(models.Model):
    """Database model for storing prompts."""

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, db_index=True)
    version = fields.CharField(max_length=50, db_index=True)

    # JSON encoded data
    messages = fields.JSONField()
    metadata_json = fields.JSONField(default={})
    parameters_json = fields.JSONField(default={})
    stats_json = fields.JSONField(default={})

    # Searchable fields extracted from metadata
    category = fields.CharField(max_length=50, null=True, db_index=True)
    is_active = fields.BooleanField(default=False, db_index=True)
    is_fallback = fields.BooleanField(default=False, db_index=True)
    fallback_for = fields.CharField(max_length=255, null=True, db_index=True)
    priority = fields.IntField(default=0)

    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "prompts"
        unique_together = (("name", "version"),)

    @property
    def metadata(self) -> PromptMetadata:
        """Get the prompt metadata as a Pydantic model."""
        data = self.metadata_json or {}
        return PromptMetadata(**data)

    @property
    def parameters(self) -> Optional[PromptParameters]:
        """Get the prompt parameters as a Pydantic model."""
        if not self.parameters_json:
            return None
        return PromptParameters(**self.parameters_json)

    @property
    def stats(self) -> Optional[PromptStats]:
        """Get the prompt stats as a Pydantic model."""
        if not self.stats_json:
            return None
        return PromptStats(**self.stats_json)

    def to_prompt(self) -> Prompt:
        """Convert the database model to a Prompt object."""
        return Prompt(
            messages=self.messages,
            metadata=self.metadata,
            parameters=self.parameters,
            stats=self.stats,
        )

    @classmethod
    def from_prompt(
            cls,
            name: str,
            version: str,
            prompt: Prompt) -> "PromptModel":
        """Convert a Prompt object to a database model."""
        # Extract metadata fields for indexing
        metadata_dict = prompt.metadata.dict() if prompt.metadata else {}
        category = metadata_dict.get("category")
        is_active = metadata_dict.get("is_active", False)
        is_fallback = metadata_dict.get("is_fallback", False)
        fallback_for = metadata_dict.get("fallback_for")
        priority = metadata_dict.get("priority", 0)

        return cls(
            name=name,
            version=version,
            messages=json.loads(json.dumps([m.dict() for m in prompt.messages])),
            metadata_json=json.loads(json.dumps(metadata_dict)) if prompt.metadata else {},
            parameters_json=(
                json.loads(json.dumps(prompt.parameters.dict())) if prompt.parameters else {}
            ),
            stats_json=json.loads(json.dumps(prompt.stats.dict())) if prompt.stats else {},
            category=category,
            is_active=is_active,
            is_fallback=is_fallback,
            fallback_for=fallback_for,
            priority=priority,
        )


class DBPromptRepo:
    """
    A repository for managing and versioning prompts using a database.
    """

    def __init__(self, db_url: str = "sqlite://db.sqlite3"):
        """
        Initialize a database prompt repository.

        Args:
            db_url: Database URL. Defaults to SQLite.
        """
        self.db_url = db_url
        self._is_initialized = False

    async def init(self):
        """Initialize the database connection."""
        if not self._is_initialized:
            await Tortoise.init(
                db_url=self.db_url, modules={"models": ["evoluteprompt.core.database"]}
            )
            await Tortoise.generate_schemas()
            self._is_initialized = True

    async def close(self):
        """Close the database connection."""
        await Tortoise.close_connections()
        self._is_initialized = False

    async def save_prompt(
        self,
        prompt_name: str,
        prompt: Prompt,
        version: Optional[str] = None,
        message: Optional[str] = None,
    ) -> str:
        """
        Save a prompt to the database.

        Args:
            prompt_name: The name of the prompt.
            prompt: The prompt to save.
            version: The version to save. If None, a new version will be created.
            message: A message describing the changes.

        Returns:
            The version of the saved prompt.
        """
        await self.init()

        # If no version specified, get the next version
        if version is None:
            version = await self._get_next_version(prompt_name)

        # Update the prompt metadata
        if prompt.metadata is None:
            prompt.metadata = PromptMetadata(version=version)
        else:
            prompt.metadata.version = version

        if prompt.metadata.created_at is None:
            prompt.metadata.created_at = datetime.now().isoformat()

        prompt.metadata.updated_at = datetime.now().isoformat()

        # Create or update the prompt in the database
        prompt_model = await PromptModel.filter(name=prompt_name, version=version).first()
        if prompt_model:
            # Update existing prompt
            prompt_model.messages = json.loads(
                json.dumps([m.dict() for m in prompt.messages]))
            prompt_model.metadata_json = (
                json.loads(
                    json.dumps(
                        prompt.metadata.dict())) if prompt.metadata else {})
            prompt_model.parameters_json = (
                json.loads(
                    json.dumps(
                        prompt.parameters.dict())) if prompt.parameters else {})
            prompt_model.stats_json = (
                json.loads(
                    json.dumps(
                        prompt.stats.dict())) if prompt.stats else {})

            # Update indexable fields
            metadata_dict = prompt.metadata.dict() if prompt.metadata else {}
            prompt_model.category = metadata_dict.get("category")
            prompt_model.is_active = metadata_dict.get("is_active", False)
            prompt_model.is_fallback = metadata_dict.get("is_fallback", False)
            prompt_model.fallback_for = metadata_dict.get("fallback_for")
            prompt_model.priority = metadata_dict.get("priority", 0)

            await prompt_model.save()
        else:
            # Create new prompt
            prompt_model = PromptModel.from_prompt(
                prompt_name, version, prompt)
            await prompt_model.save()

        return version

    async def get_prompt(
            self,
            prompt_name: str,
            version: Optional[str] = None) -> Optional[Prompt]:
        """
        Get a prompt from the database.

        Args:
            prompt_name: The name of the prompt.
            version: The version to get. If None, the latest version will be used.

        Returns:
            The prompt, or None if not found.
        """
        await self.init()

        # If no version specified, get the latest version
        if version is None:
            version = await self.get_latest_version(prompt_name)
            if version is None:
                return None

        # Get the prompt from the database
        prompt_model = await PromptModel.filter(name=prompt_name, version=version).first()
        if prompt_model is None:
            return None

        return prompt_model.to_prompt()

    async def get_active_prompt(self, prompt_name: str) -> Optional[Prompt]:
        """
        Get the active prompt for the given name.

        Args:
            prompt_name: The name of the prompt.

        Returns:
            The active prompt, or None if not found.
        """
        await self.init()

        prompt_model = (
            await PromptModel.filter(name=prompt_name, is_active=True).order_by("-priority").first()
        )

        if prompt_model is None:
            return None

        return prompt_model.to_prompt()

    async def get_fallback_prompt(self, prompt_name: str) -> Optional[Prompt]:
        """
        Get the fallback prompt for the given name.

        Args:
            prompt_name: The name of the prompt.

        Returns:
            The fallback prompt, or None if not found.
        """
        await self.init()

        prompt_model = (
            await PromptModel.filter(fallback_for=prompt_name, is_fallback=True)
            .order_by("-priority")
            .first()
        )

        if prompt_model is None:
            return None

        return prompt_model.to_prompt()

    async def list_prompts(
            self,
            category: Optional[PromptCategory] = None) -> List[str]:
        """
        List all prompts in the database.

        Args:
            category: Optional category to filter by.

        Returns:
            A list of prompt names.
        """
        await self.init()

        query = PromptModel.all()
        if category:
            query = query.filter(category=category)

        prompt_models = await query.distinct().values("name")
        return [p["name"] for p in prompt_models]

    async def list_versions(self, prompt_name: str) -> List[str]:
        """
        List all versions of a prompt.

        Args:
            prompt_name: The name of the prompt.

        Returns:
            A list of versions.
        """
        await self.init()

        prompt_models = (
            await PromptModel.filter(name=prompt_name).order_by("version").values("version")
        )
        return [p["version"] for p in prompt_models]

    async def get_latest_version(self, prompt_name: str) -> Optional[str]:
        """
        Get the latest version of a prompt.

        Args:
            prompt_name: The name of the prompt.

        Returns:
            The latest version, or None if not found.
        """
        await self.init()

        prompt_model = await PromptModel.filter(name=prompt_name).order_by("-version").first()
        if prompt_model is None:
            return None

        return prompt_model.version

    async def _get_next_version(self, prompt_name: str) -> str:
        """
        Get the next version for a prompt.

        Args:
            prompt_name: The name of the prompt.

        Returns:
            The next version.
        """
        latest_version = await self.get_latest_version(prompt_name)

        if latest_version is None:
            # First version
            return "0.1.0"

        # Parse the version
        parts = latest_version.split(".")
        if len(parts) != 3:
            # Invalid version format, start from scratch
            return "0.1.0"

        # Increment the patch version
        major, minor, patch = map(int, parts)
        return f"{major}.{minor}.{patch + 1}"

    async def set_active(
            self,
            prompt_name: str,
            version: str,
            active: bool = True) -> None:
        """
        Set a prompt version as active or inactive.

        Args:
            prompt_name: The name of the prompt.
            version: The version to update.
            active: Whether the prompt should be active.
        """
        await self.init()

        prompt_model = await PromptModel.filter(name=prompt_name, version=version).first()
        if prompt_model is None:
            return

        prompt_model.is_active = active
        await prompt_model.save()

        # If setting this prompt as active, deactivate all other versions
        if active:
            await PromptModel.filter(name=prompt_name).exclude(version=version).update(
                is_active=False
            )

    async def set_fallback(
            self,
            prompt_name: str,
            version: str,
            fallback_for: str) -> None:
        """
        Set a prompt version as a fallback for another prompt.

        Args:
            prompt_name: The name of the prompt.
            version: The version to update.
            fallback_for: The name of the prompt this is a fallback for.
        """
        await self.init()

        prompt_model = await PromptModel.filter(name=prompt_name, version=version).first()
        if prompt_model is None:
            return

        prompt_model.is_fallback = True
        prompt_model.fallback_for = fallback_for
        await prompt_model.save()

    async def update_stats(
            self,
            prompt_name: str,
            version: str,
            success: bool = True) -> None:
        """
        Update the stats for a prompt.

        Args:
            prompt_name: The name of the prompt.
            version: The version to update.
            success: Whether the prompt was used successfully.
        """
        await self.init()

        prompt_model = await PromptModel.filter(name=prompt_name, version=version).first()
        if prompt_model is None:
            return

        stats = prompt_model.stats or PromptStats()

        if success:
            stats.successful_uses += 1
        else:
            stats.failed_uses += 1

        stats.last_used = datetime.now().isoformat()

        prompt_model.stats_json = json.loads(json.dumps(stats.dict()))
        await prompt_model.save()
