# Data Model: Todo AI Chatbot

**Feature**: 004-ai-chatbot
**Date**: 2026-01-27
**Database**: Neon Serverless PostgreSQL (extend existing Phase II schema)

## Overview

Extends existing Phase II database with 2 new tables to support stateless AI conversations. All conversation state and message history stored in database to enable horizontal scaling and server restarts without context loss.

## Entity Relationship Diagram

```
User (existing)
  ├─ 1:N → Conversation (new)
  │          ├─ 1:N → Message (new)
  └─ 1:N → Task (existing)
```

## Database Tables

### Conversation Table (NEW)

Represents a chat session between a user and the AI assistant.

**Table**: `conversations`

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| id | UUID | PRIMARY KEY | Unique conversation identifier |
| user_id | UUID | FOREIGN KEY → users(id) ON DELETE CASCADE, NOT NULL | Owner of conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Conversation creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
```sql
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
```

**Rationale**: User owns multiple conversations. Cascade delete ensures cleanup when user deleted. updated_at tracks conversation activity.

### Message Table (NEW)

Represents individual messages in a conversation (both user and assistant messages).

**Table**: `messages`

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| id | UUID | PRIMARY KEY | Unique message identifier |
| conversation_id | UUID | FOREIGN KEY → conversations(id) ON DELETE CASCADE, NOT NULL | Parent conversation |
| role | VARCHAR(20) | NOT NULL, CHECK (role IN ('user', 'assistant')) | Message sender |
| content | TEXT | NOT NULL | Message text content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

**Indexes**:
```sql
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

**Rationale**: Conversation has many messages. role distinguishes user input from AI response. Cascade delete removes messages when conversation deleted. Indexes optimize conversation history queries.

### Existing Tables (Phase II - NO CHANGES)

**User Table** (existing):
- id: UUID (PK)
- email: String (unique)
- name: String
- hashed_password: String
- created_at: TIMESTAMP

**Task Table** (existing):
- id: Integer (PK, auto-increment)
- user_id: UUID (FK → users.id)
- title: String (max 200)
- description: String (max 1000, nullable)
- completed: Boolean
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)
```

### Message Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Literal

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: Literal["user", "assistant"] = Field(nullable=False)
    content: str = Field(nullable=False, max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
```

## Pydantic Schemas

### Request Schema

```python
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000, description="User message content")
    conversation_id: Optional[UUID] = Field(None, description="Existing conversation ID (null for new conversation)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add a task to buy groceries",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
```

### Response Schema

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID

class ToolCall(BaseModel):
    tool: str = Field(..., description="MCP tool name (add_task, list_tasks, etc.)")
    parameters: Dict[str, Any] = Field(..., description="Tool input parameters")
    result: Dict[str, Any] = Field(..., description="Tool execution result")

class ChatResponse(BaseModel):
    conversation_id: UUID = Field(..., description="Conversation ID for subsequent messages")
    response: str = Field(..., description="AI assistant response")
    tool_calls: List[ToolCall] = Field(default=[], description="Optional list of tool invocations for transparency")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "response": "Got it! I've added 'Buy groceries' to your task list.",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "parameters": {"user_id": "...", "title": "Buy groceries"},
                        "result": {"task_id": 5, "status": "created", "title": "Buy groceries"}
                    }
                ]
            }
        }
```

### Message Response Schema (for history)

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class MessageResponse(BaseModel):
    id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime
```

## Alembic Migration Script

**Filename**: `alembic/versions/xxx_add_conversation_tables.py`

```python
"""Add conversation and message tables for AI chatbot

Revision ID: xxx
Revises: yyy
Create Date: 2026-01-27
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'xxx'
down_revision = 'yyy'  # Previous migration ID
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('NOW()')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role'),
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    # Drop tables in reverse order (respect foreign keys)
    op.drop_index('idx_messages_created_at', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    op.drop_index('idx_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
```

## Query Patterns

### Create New Conversation

```python
conversation = Conversation(user_id=authenticated_user_id)
session.add(conversation)
session.commit()
session.refresh(conversation)
return conversation.id
```

### Load Conversation with Validation

```python
conversation = session.query(Conversation).filter(
    Conversation.id == conversation_id,
    Conversation.user_id == authenticated_user_id  # Ownership validation
).first()
if not conversation:
    raise HTTPException(status_code=404, detail="Conversation not found")
```

### Load Last 50 Messages

```python
messages = session.query(Message).filter(
    Message.conversation_id == conversation_id
).order_by(Message.created_at.desc()).limit(50).all()
messages.reverse()  # Oldest first for agent context
```

**Performance**: <50ms with indexes

### Store User Message

```python
user_message = Message(
    conversation_id=conversation_id,
    role="user",
    content=request.message
)
session.add(user_message)
session.commit()
```

### Store Assistant Message

```python
assistant_message = Message(
    conversation_id=conversation_id,
    role="assistant",
    content=agent_response
)
session.add(assistant_message)

# Update conversation timestamp
conversation.updated_at = datetime.utcnow()
session.commit()
```

## Storage Estimates

**Per conversation** (50 messages average):
- Conversation row: ~100 bytes
- Message rows (50): ~50KB (assuming 1KB per message)
- Total: ~50.1KB per conversation

**1000 active users**, 10 conversations each:
- Total: 10,000 conversations × 50KB = 500MB
- Neon free tier: 512MB (sufficient for MVP)
- Neon Pro tier: 10GB (supports 200K conversations)

## Validation Rules

**Message content**:
- Minimum length: 1 character
- Maximum length: 10,000 characters
- Non-empty after trimming

**Role values**:
- Must be "user" or "assistant"
- Enforced by database CHECK constraint and Pydantic Literal

**Conversation ownership**:
- Every query filters by user_id from JWT
- Foreign keys enforce referential integrity
- Cascade delete cleans up orphaned records

## Performance Optimizations

**Indexes**:
1. `conversations.user_id` - Fast user conversation lookup
2. `messages.conversation_id` - Fast message retrieval
3. `messages.created_at` - Fast chronological ordering

**Query optimization**:
- LIMIT 50 prevents unbounded result sets
- ORDER BY created_at DESC with reverse in Python (faster than ASC)
- Index-only scans where possible

**Connection pooling**:
- pool_size=20
- max_overflow=10
- pool_recycle=3600 (1 hour)

**Expected query times**:
- Conversation lookup: <5ms
- Message retrieval (50 rows): <50ms
- Message insert: <5ms
- Total per request: <60ms (database only)

## Migration Execution

```bash
# Generate migration (auto-detect changes)
alembic revision --autogenerate -m "Add conversation and message tables"

# Review generated migration in alembic/versions/

# Apply migration
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"
psql $DATABASE_URL -c "\d conversations"
psql $DATABASE_URL -c "\d messages"
```

## Rollback Strategy

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

**Data loss warning**: Downgrade drops conversations and messages tables. Backup data before rollback if needed.
