"""
User SQLModel for database table definition.
"""
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .conversation import Conversation


class User(SQLModel, table=True):
    """
    User model for storing user account information.

    Fields:
        id: UUID primary key
        email: Unique email address (lowercase, max 255 chars)
        name: User's full name (max 100 chars)
        hashed_password: Bcrypt hashed password (60 chars)
        created_at: Timestamp of account creation
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, sa_column_kwargs={"nullable": False})
    name: str = Field(max_length=100, sa_column_kwargs={"nullable": False})
    hashed_password: str = Field(max_length=60, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})

    # Relationships (Phase III)
    conversations: List["Conversation"] = Relationship(back_populates="user")

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "name": "John Doe",
                "hashed_password": "$2b$10$...",
                "created_at": "2026-01-09T10:30:00",
            }
        }
