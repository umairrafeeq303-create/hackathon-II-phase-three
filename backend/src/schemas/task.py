"""
Pydantic schemas for Task CRUD operations.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):
    """Base schema with common task fields."""

    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)",
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace from title and description."""
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        """Ensure title is not empty after stripping."""
        if not v or v.strip() == "":
            raise ValueError("Title cannot be empty")
        return v


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating a task.
    All fields are optional to support partial updates.
    At least one field must be provided (validated in route handler).
    """

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)

    description: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace."""
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        """Ensure title is not empty if provided."""
        if v is not None and (not v or v.strip() == ""):
            raise ValueError("Title cannot be empty")
        return v


class TaskResponse(TaskBase):
    """Schema for task responses (includes all fields)."""

    id: int
    user_id: UUID
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,  # Allows conversion from SQLModel objects
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        },
    }
