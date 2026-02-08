# Phase 1: Data Model

**Feature**: Task CRUD API Backend
**Branch**: `002-task-crud`
**Date**: 2026-01-09

## Overview

This document defines the complete data model for the Task CRUD API, including database models (SQLModel), request/response schemas (Pydantic), validation rules, and state transitions.

## 1. Database Models

### 1.1 Task Model (NEW)

**File**: `backend/src/models/task.py`

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

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
        description="Auto-incrementing task ID"
    )

    # Foreign key to User
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        index=True,
        description="ID of the user who owns this task"
    )

    # Task content
    title: str = Field(
        max_length=200,
        description="Task title (required, max 200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )

    # Task state
    completed: bool = Field(
        default=False,
        index=True,
        description="Whether the task is completed"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the task was created (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the task was last updated (UTC)"
    )
```

### 1.2 User Model (from Spec 1)

**File**: `backend/src/models/user.py`

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    """User model with authentication credentials."""
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    email: str = Field(
        unique=True,
        index=True,
        max_length=255
    )

    name: str = Field(max_length=255)

    hashed_password: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 1.3 Database Schema (SQL)

```sql
-- Users table (from Spec 1)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table (NEW - this feature)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Foreign Key Behavior**:
- `ON DELETE CASCADE`: When a user is deleted, all their tasks are automatically deleted
- This ensures no orphaned tasks remain in the database

## 2. Request/Response Schemas

### 2.1 Base Schemas

**File**: `backend/src/schemas/task.py`

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid

class TaskBase(BaseModel):
    """Base schema with common task fields."""

    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )

    @validator('title', 'description', pre=True)
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace from title and description."""
        if isinstance(v, str):
            return v.strip()
        return v

    @validator('title')
    def title_not_empty(cls, v):
        """Ensure title is not empty after stripping."""
        if not v or v.strip() == '':
            raise ValueError('Title cannot be empty')
        return v
```

### 2.2 Request Schemas

```python
class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating a task.
    All fields are optional to support partial updates.
    At least one field must be provided (validated in route handler).
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    @validator('title', 'description', pre=True)
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace."""
        if isinstance(v, str):
            return v.strip()
        return v

    @validator('title')
    def title_not_empty(cls, v):
        """Ensure title is not empty if provided."""
        if v is not None and (not v or v.strip() == ''):
            raise ValueError('Title cannot be empty')
        return v
```

### 2.3 Response Schemas

```python
class TaskResponse(TaskBase):
    """Schema for task responses (includes all fields)."""

    id: int
    user_id: uuid.UUID
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from SQLModel objects
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v)
        }


class TaskListResponse(BaseModel):
    """Schema for list of tasks."""

    tasks: list[TaskResponse]
    total: int

    class Config:
        from_attributes = True
```

## 3. Validation Rules

### 3.1 Field Constraints

| Field | Constraint | Error Message |
|-------|-----------|---------------|
| title | Required (min_length=1) | "field required" |
| title | Max length 200 | "ensure this value has at most 200 characters" |
| title | Not empty after strip | "Title cannot be empty" |
| description | Optional | - |
| description | Max length 1000 | "ensure this value has at most 1000 characters" |
| user_id | Valid UUID format | "value is not a valid uuid" |
| completed | Boolean | "value could not be parsed to a boolean" |

### 3.2 Update Validation

For `TaskUpdate`, at least one field must be provided:

```python
# In route handler:
update_data = task_update.dict(exclude_unset=True)
if not update_data:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="At least one field must be provided for update"
    )
```

### 3.3 Whitespace Handling

- **Title and Description**: Leading/trailing whitespace is automatically stripped
- **Empty After Strip**: If title becomes empty after stripping, validation fails
- **Normalization**: Ensures consistent data storage (no accidental whitespace)

## 4. State Transitions

### 4.1 Task Lifecycle

```
[User creates task]
         ↓
    ┌─────────┐
    │ Created │  (completed = false)
    └─────────┘
         ↓
    ┌─────────┐
    │ Updated │  (title/description changed, updated_at updated)
    └─────────┘
         ↓
    ┌───────────┐
    │ Completed │  (completed = true)
    └───────────┘
         ↓
    ┌────────────┐
    │ Reopened   │  (completed = false again)
    └────────────┘
         ↓
    [Can be deleted at any state]
```

### 4.2 Toggle Completion Logic

```python
# PATCH /api/{user_id}/tasks/{task_id}/toggle
# Toggles completed between true and false

if task.completed:
    task.completed = False  # Reopen task
else:
    task.completed = True   # Complete task

task.updated_at = datetime.utcnow()
```

**Behavior**:
- Idempotent: Can be called multiple times safely
- Updates `updated_at` timestamp on every toggle
- Does not modify `title` or `description`

## 5. Entity Relationships

```
┌────────────┐
│   User     │
│ (Spec 1)   │
└────────────┘
       │
       │ 1
       │
       │ has many
       │
       │ N
       ▼
┌────────────┐
│   Task     │
│ (This spec)│
└────────────┘
```

**Cardinality**: One User has many Tasks (1:N)

**Cascade Behavior**:
- Delete User → Delete all associated Tasks (CASCADE DELETE)
- Delete Task → No effect on User

**Referential Integrity**:
- `tasks.user_id` MUST reference valid `users.id`
- PostgreSQL enforces foreign key constraint

## 6. Query Patterns

### 6.1 Common Queries

```python
# Get all tasks for a user (with filter and sort)
select(Task).where(
    Task.user_id == user_id,
    Task.completed == False  # if status=pending
).order_by(Task.created_at.desc())

# Get single task (with ownership check)
select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id
)

# Count tasks by user
select(func.count(Task.id)).where(Task.user_id == user_id)

# Get recently updated tasks
select(Task).where(
    Task.user_id == user_id
).order_by(Task.updated_at.desc()).limit(10)
```

### 6.2 Index Utilization

| Query | Index Used | Performance |
|-------|-----------|-------------|
| Filter by user_id | idx_tasks_user_id | Fast (indexed) |
| Filter by completed | idx_tasks_completed | Fast (indexed) |
| Filter by user_id + completed | Both indexes | Fast (combined) |
| Sort by created_at | Sequential scan after filter | Acceptable (filtered set is small) |
| Sort by title | Sequential scan after filter | Acceptable (filtered set is small) |

## 7. Data Integrity Rules

### 7.1 Database Constraints

- **Primary Key**: `tasks.id` is unique and auto-incrementing
- **Foreign Key**: `tasks.user_id` MUST reference `users.id`
- **Not Null**: `user_id`, `title`, `completed`, `created_at`, `updated_at` cannot be null
- **Max Length**: `title` max 200, `description` max 1000 (enforced at database level)

### 7.2 Application-Level Rules

- **User Isolation**: Tasks can only be accessed by their owner
- **Timestamp Immutability**: `created_at` never changes after creation
- **Timestamp Updates**: `updated_at` MUST be updated on every modification
- **Whitespace Normalization**: Title/description stripped before storage

## 8. Performance Considerations

### 8.1 Expected Data Volume

- **Per User**: Up to 10,000+ tasks (per success criteria)
- **Total System**: Scales with number of users
- **Typical Queries**: Filter + sort operations on user's tasks (already filtered set)

### 8.2 Optimization Strategy

- **Indexes**: On `user_id` and `completed` for fast filtering
- **No Composite Index**: Single-column indexes sufficient for most queries
- **Pagination**: Not required for MVP (success criteria: 10k tasks loads <1s)
- **Database**: PostgreSQL query optimizer handles index combination efficiently

### 8.3 Performance Targets

| Operation | Target | Strategy |
|-----------|--------|----------|
| Create task | <5 seconds | Indexed insert |
| List tasks (10k+) | <1 second | Indexed query + sorting |
| Filter/sort | <1 second | Indexed WHERE + ORDER BY |
| Update task | <1 second | Primary key lookup |
| Delete task | <1 second | Primary key lookup |
| Toggle completion | <1 second | Primary key lookup + update |

## Summary

**Database Models**:
- Task model with 7 fields (id, user_id, title, description, completed, created_at, updated_at)
- Foreign key to User with CASCADE DELETE
- Indexes on user_id and completed

**Schemas**:
- TaskCreate (for POST requests)
- TaskUpdate (for PUT requests, partial updates)
- TaskResponse (for all responses)
- Validation with automatic whitespace stripping

**Relationships**:
- User 1:N Task (one user has many tasks)
- Foreign key enforces referential integrity

**State Transitions**:
- Created → Updated → Completed → Reopened → Deleted
- Toggle operation for completion status

**Performance**:
- Indexes support sub-second queries with 10,000+ tasks
- Meets all success criteria from specification

**Next**: Proceed to generate API contracts in `contracts/` directory.
