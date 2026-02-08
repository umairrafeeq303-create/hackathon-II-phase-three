"""
Task SQLModel for task management.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task model representing a user's todo item.

    Relationships:
    - Belongs to User (foreign key: user_id)

    Indexes:
    - user_id (for filtering tasks by user)
    - completed (for filtering by status)
    """

    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing task ID",
    )

    # Foreign key to User (CASCADE DELETE handled at database level via migration)
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        sa_column_kwargs={"nullable": False},
        description="ID of the user who owns this task",
    )

    # Task content
    title: str = Field(
        max_length=200,
        sa_column_kwargs={"nullable": False},
        description="Task title (required, max 200 characters)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)",
    )

    # Task state
    completed: bool = Field(
        default=False,
        index=True,
        sa_column_kwargs={"nullable": False},
        description="Whether the task is completed",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False},
        description="When the task was created (UTC)",
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"nullable": False},
        description="When the task was last updated (UTC)",
    )

    class Config:
        """SQLModel configuration."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-01-09T10:30:00",
                "updated_at": "2026-01-09T10:30:00",
            }
        }
