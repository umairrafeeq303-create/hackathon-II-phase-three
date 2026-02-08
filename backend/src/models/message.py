"""Message model for AI chatbot conversation messages."""
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """
    Message table for storing individual messages in AI chatbot conversations.

    Each message has a role (user or assistant) and belongs to a conversation.
    Messages are ordered by created_at for conversation history.
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )
    role: str = Field(nullable=False, max_length=20)  # "user" or "assistant"
    content: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    def __init__(self, **data):
        """Initialize message with role validation."""
        super().__init__(**data)
        if self.role not in ("user", "assistant"):
            raise ValueError(f"Invalid role: {self.role}. Must be 'user' or 'assistant'")
