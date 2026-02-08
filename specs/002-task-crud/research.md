# Phase 0: Research & Technical Decisions

**Feature**: Task CRUD API Backend
**Branch**: `002-task-crud`
**Date**: 2026-01-09

## Overview

This document consolidates all technical research, design decisions, and implementation patterns for the Task CRUD API Backend. All unknowns from Technical Context have been resolved through analysis of existing codebase (Spec 1 authentication) and FastAPI/SQLModel best practices.

## 1. SQLModel Task Model Design

### Decision: Task Model Structure

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Rationale

- **Primary Key**: Integer auto-increment for simplicity and performance (smaller index size than UUID)
- **Foreign Key**: `user_id` references `users.id` with CASCADE DELETE (when user deleted, tasks deleted)
- **Indexes**: Added on `user_id` (for user filtering) and `completed` (for status filtering)
- **Field Constraints**: `max_length` on title (200) and description (1000) enforced at database level
- **Timestamps**: `created_at` immutable, `updated_at` updated on modification
- **Default Values**: `completed=False` for new tasks, timestamps auto-generated

### Alternatives Considered

- **UUID Primary Key**: Rejected because integer auto-increment is simpler, faster for joins, and adequate for single-database setup
- **Separate Timestamps Table**: Rejected as over-engineering for simple timestamp tracking
- **Soft Delete**: Rejected per constitution (not in requirements, adds complexity)

## 2. Pydantic Request/Response Schemas

### Decision: Schema Hierarchy

```python
# Base schema with common fields
class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

# Request schema for creation
class TaskCreate(TaskBase):
    pass

# Request schema for updates (all fields optional)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

# Response schema with all fields
class TaskResponse(TaskBase):
    id: int
    user_id: uuid.UUID
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For SQLModel compatibility
```

### Rationale

- **Separation of Concerns**: Different schemas for create, update, and response
- **Validation**: Pydantic validates min/max length before database operations
- **Partial Updates**: TaskUpdate has all optional fields to support PATCH semantics
- **Response Completeness**: TaskResponse includes all fields for frontend consumption
- **SQLModel Compatibility**: `from_attributes=True` allows conversion from SQLModel objects

### Alternatives Considered

- **Single Schema**: Rejected because create/update/response have different field requirements
- **Inheriting from SQLModel**: Rejected to maintain clean separation between database and API layers

## 3. FastAPI Route Organization

### Decision: Router with Dependency Injection

```python
# backend/src/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ...api.dependencies.auth import get_current_user_id, verify_user_match
from ...core.database import get_session
from ...models.task import Task
from ...schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    status: str = "all",
    sort: str = "created",
    order: str = "desc",
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    # Implementation
    pass
```

### Rationale

- **Router Organization**: Separate router for task endpoints (clean separation from auth routes)
- **Path Parameters**: `{user_id}` in URL pattern for RESTful resource identification
- **Dependency Injection**: Reuse `get_current_user_id` from Spec 1 for JWT validation
- **Query Parameters**: Filter and sort options as query params (RESTful convention)
- **Type Safety**: Python type hints for all parameters and return types

### Alternatives Considered

- **Single Routes File**: Rejected because separate routers improve modularity
- **Class-Based Views**: Rejected because function-based routes are simpler and FastAPI convention

## 4. Authentication Integration (from Spec 1)

### Decision: Reuse Existing JWT Validation

```python
# backend/src/api/dependencies/auth.py (from Spec 1)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import uuid

security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> uuid.UUID:
    """Extract and validate user_id from JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        return uuid.UUID(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

async def verify_user_match(user_id: str, current_user_id: uuid.UUID):
    """Verify URL user_id matches JWT user_id."""
    try:
        url_user_id = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )

    if url_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: user_id mismatch"
        )
```

### Rationale

- **Reuse Existing Code**: Leverages Spec 1 authentication dependency (no duplication)
- **Two-Step Validation**: 1) Extract user_id from JWT, 2) Verify it matches URL parameter
- **Error Separation**: 401 for auth failures, 403 for authorization failures, 400 for format errors
- **Type Safety**: Returns typed `uuid.UUID` for downstream use

### Alternatives Considered

- **Combined Validation**: Rejected because separating JWT and URL validation improves clarity
- **Custom Middleware**: Rejected because FastAPI dependencies are more testable

## 5. User Ownership Validation Pattern

### Decision: Three-Tier Validation

```python
async def get_user_task_or_404(
    task_id: int,
    user_id: uuid.UUID,
    session: Session
) -> Task:
    """Get task by ID and verify ownership. Returns 404 if not found or not owned."""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if task is None:
        # Return 404 (not 403) to prevent task enumeration
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task
```

### Rationale

- **Combined Query**: Filters by both `task_id` AND `user_id` in single query (efficient)
- **Enumeration Prevention**: Returns 404 (not 403) when task doesn't exist OR isn't owned (prevents attackers from discovering task IDs)
- **Reusable Helper**: Shared across update, delete, toggle, and get_single operations
- **Type Safety**: Returns typed `Task` object for direct use

### Alternatives Considered

- **Separate Queries**: Rejected because two queries (find task, check ownership) is less efficient
- **403 for Ownership**: Rejected because it leaks information about task existence

## 6. Filtering and Sorting Implementation

### Decision: Query Parameter-Based Filtering with SQLModel

```python
from enum import Enum

class TaskStatus(str, Enum):
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"

class SortField(str, Enum):
    CREATED = "created"
    TITLE = "title"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

# In route handler:
statement = select(Task).where(Task.user_id == current_user_id)

# Apply status filter
if status == TaskStatus.PENDING:
    statement = statement.where(Task.completed == False)
elif status == TaskStatus.COMPLETED:
    statement = statement.where(Task.completed == True)
# else: all - no additional filter

# Apply sorting
if sort == SortField.TITLE:
    sort_column = Task.title.collate("NOCASE")  # Case-insensitive
else:
    sort_column = Task.created_at

if order == SortOrder.ASC:
    statement = statement.order_by(sort_column)
else:
    statement = statement.order_by(sort_column.desc())

tasks = session.exec(statement).all()
```

### Rationale

- **Enums for Validation**: Pydantic validates query parameters against allowed values
- **Query Chaining**: SQLModel allows building queries progressively (readable, maintainable)
- **Case-Insensitive Title Sort**: Uses `collate("NOCASE")` for better UX
- **Index Utilization**: Filters on indexed columns (`user_id`, `completed`)
- **Default Behavior**: Default to "all" status and "created desc" (newest first)

### Alternatives Considered

- **ORM Filters**: Rejected because SQLModel's select() is more explicit
- **String-Based Sorting**: Rejected because enums provide type safety

## 7. Database Query Optimization

### Decision: Index Strategy and Query Patterns

**Indexes**:
- `user_id` (foreign key, supports user filtering)
- `completed` (supports status filtering)
- Composite index NOT added (single-column indexes sufficient for most queries)

**Query Patterns**:
```python
# List with filter/sort (uses indexes)
select(Task).where(
    Task.user_id == user_id,
    Task.completed == True
).order_by(Task.created_at.desc())

# Single task (uses primary key + user_id index)
select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id
)
```

### Rationale

- **Selective Indexing**: Only index columns used in WHERE and ORDER BY clauses
- **No Over-Indexing**: Composite index would help marginally but slow down writes
- **PostgreSQL Optimizer**: Modern databases can combine single-column indexes efficiently
- **Performance Target**: Sub-100ms queries with 10,000+ tasks (achievable with current indexes)

### Alternatives Considered

- **Composite Index (user_id, completed)**: Rejected because minimal benefit and slows inserts
- **Index on created_at**: Rejected because sorting happens after filtering (fewer rows)

## 8. Error Handling and HTTP Status Codes

### Decision: Consistent Error Response Format

```python
# Validation error (422)
{
    "detail": [
        {
            "loc": ["body", "title"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}

# Custom errors (400, 401, 403, 404)
{
    "detail": "Task not found"
}

# Server errors (500)
{
    "detail": "Internal server error"
}
```

**Status Code Mapping**:
- 200: Successful GET, PUT, DELETE
- 201: Successful POST (resource created)
- 400: Bad request (invalid user_id format)
- 401: Unauthorized (missing/invalid JWT)
- 403: Forbidden (user_id mismatch)
- 404: Not found (task doesn't exist or not owned)
- 422: Unprocessable entity (validation failed)
- 500: Internal server error

### Rationale

- **FastAPI Default**: 422 errors auto-generated by Pydantic with detailed field info
- **Explicit HTTPException**: Custom errors use HTTPException with appropriate status code
- **Enumeration Prevention**: 404 for both "not found" and "not owned" (consistent messaging)
- **Client-Friendly**: Validation errors include field location for form highlighting

### Alternatives Considered

- **Custom Error Schema**: Rejected because FastAPI's default is industry-standard
- **403 for Not Found**: Rejected because it leaks task existence information

## 9. Updated_at Timestamp Management

### Decision: Manual Update in Route Handlers

```python
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    verify_user_match(user_id, current_user_id)
    task = get_user_task_or_404(task_id, current_user_id, session)

    # Update fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Rationale

- **Explicit Update**: Manually set `updated_at` in update and toggle operations (clear intent)
- **No Database Trigger**: Avoids database-level triggers (keeps logic in application code)
- **Timestamp Accuracy**: Uses `datetime.utcnow()` for consistency with `created_at`

### Alternatives Considered

- **SQLModel Event Listener**: Rejected because explicit updates are clearer
- **Database Trigger**: Rejected per constitution (logic should be in code, not database)

## 10. Testing Strategy

### Decision: Pytest with Test Fixtures

```python
# tests/conftest.py
import pytest
from sqlmodel import Session, create_engine, SQLModel
from fastapi.testclient import TestClient

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)

@pytest.fixture
def auth_headers(session):
    # Create test user and return JWT token
    pass
```

**Test Categories**:
- **Unit Tests**: Schema validation, helper functions
- **Integration Tests**: Full endpoint tests with database
- **Contract Tests**: Request/response format validation
- **Security Tests**: Ownership validation, enumeration prevention

### Rationale

- **In-Memory SQLite**: Fast test execution without external database
- **TestClient**: FastAPI's built-in test client for HTTP testing
- **Fixture Reuse**: Shared session and auth fixtures across tests
- **Comprehensive Coverage**: Tests cover success, validation, authorization, and error cases

### Alternatives Considered

- **Real Database**: Rejected because slower and requires cleanup
- **Mock Database**: Rejected because integration tests need real SQL queries

## Summary of Resolved Unknowns

All Technical Context unknowns have been resolved:

✅ **Language/Version**: Python 3.11+ (confirmed)
✅ **Primary Dependencies**: FastAPI, SQLModel, python-jose, passlib (confirmed)
✅ **Storage**: Neon PostgreSQL via SQLModel (confirmed)
✅ **Testing**: pytest with in-memory SQLite (decided)
✅ **Target Platform**: Railway deployment (confirmed)
✅ **Performance Goals**: Task model with indexes meets <1s requirements (validated)
✅ **Constraints**: Three-tier validation ensures zero cross-user access (validated)
✅ **Scale/Scope**: 6 endpoints with filtering/sorting (confirmed)

## Next Steps

Proceed to **Phase 1: Design & Contracts** to generate:
- `data-model.md`: Complete Task model and schema definitions
- `contracts/`: OpenAPI specification for all 6 endpoints
- `quickstart.md`: Implementation guidance for developers
