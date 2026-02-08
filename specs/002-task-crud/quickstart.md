# Quickstart Guide: Task CRUD API Backend Implementation

**Feature**: Task CRUD API Backend
**Branch**: `002-task-crud`
**Date**: 2026-01-09

## Overview

This guide provides step-by-step instructions for implementing the Task CRUD API Backend. It covers database setup, model creation, route implementation, and testing.

## Prerequisites

Before starting implementation, ensure:

✅ **Spec 1 (001-auth) is complete** and provides:
- User model with authentication
- JWT token validation (`get_current_user_id` dependency)
- Database connection setup
- BETTER_AUTH_SECRET environment variable

✅ **Development environment is ready**:
- Python 3.11+ installed
- FastAPI, SQLModel, python-jose, passlib installed
- Neon PostgreSQL database accessible
- DATABASE_URL environment variable configured

✅ **Branch is created**:
```bash
git checkout -b 002-task-crud
```

## Implementation Order

Follow this sequence to maximize value delivery and minimize integration issues:

### Phase 1: Database Model (Foundation)
1. Create Task model
2. Run database migration
3. Verify foreign key relationship

### Phase 2: Core CRUD Operations (High Value)
1. Create task (POST)
2. List tasks (GET all)
3. Get single task (GET by ID)

### Phase 3: Task Management (Medium Value)
1. Update task (PUT)
2. Delete task (DELETE)
3. Toggle completion (PATCH)

### Phase 4: Filtering & Sorting (Enhancement)
1. Add status filter (all/pending/completed)
2. Add sorting (created/title, asc/desc)

### Phase 5: Testing & Validation (Quality)
1. Unit tests for schemas
2. Integration tests for endpoints
3. Security tests for ownership validation

## Detailed Implementation Steps

### Step 1: Create Task Model

**File**: `backend/src/models/task.py`

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

**Validation**:
- Import in `backend/src/main.py`
- Run application to trigger SQLModel table creation
- Verify table exists in database

### Step 2: Create Pydantic Schemas

**File**: `backend/src/schemas/task.py`

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    @validator('title', 'description', pre=True)
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @validator('title')
    def title_not_empty(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Title cannot be empty')
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    @validator('title', 'description', pre=True)
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and (not v or v.strip() == ''):
            raise ValueError('Title cannot be empty')
        return v

class TaskResponse(TaskBase):
    id: int
    user_id: uuid.UUID
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**Validation**:
- Test schema validation with sample data
- Verify whitespace stripping works
- Confirm error messages are descriptive

### Step 3: Create Helper Functions

**File**: `backend/src/api/routes/tasks.py` (at top of file)

```python
from fastapi import HTTPException, status
from sqlmodel import Session, select
from ...models.task import Task
import uuid

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task
```

**Validation**:
- Test `verify_user_match` with valid and invalid UUIDs
- Test `get_user_task_or_404` with owned and non-owned tasks
- Verify 404 is returned (not 403) for non-owned tasks

### Step 4: Implement Create Task Endpoint

**File**: `backend/src/api/routes/tasks.py`

```python
from fastapi import APIRouter, Depends
from typing import List
from ...api.dependencies.auth import get_current_user_id
from ...core.database import get_session
from ...schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_create: TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """Create a new task for the authenticated user."""
    await verify_user_match(user_id, current_user_id)

    task = Task(
        user_id=current_user_id,
        title=task_create.title,
        description=task_create.description
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
```

**Validation**:
- Test with valid title and description
- Test with title only (no description)
- Test with empty title (should fail validation)
- Test with title >200 chars (should fail)
- Test with user_id mismatch (should return 403)

### Step 5: Implement List Tasks Endpoint

**File**: `backend/src/api/routes/tasks.py`

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

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    status: TaskStatus = TaskStatus.ALL,
    sort: SortField = SortField.CREATED,
    order: SortOrder = SortOrder.DESC,
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """List all tasks for the authenticated user with filtering and sorting."""
    await verify_user_match(user_id, current_user_id)

    # Build query
    statement = select(Task).where(Task.user_id == current_user_id)

    # Apply status filter
    if status == TaskStatus.PENDING:
        statement = statement.where(Task.completed == False)
    elif status == TaskStatus.COMPLETED:
        statement = statement.where(Task.completed == True)

    # Apply sorting
    if sort == SortField.TITLE:
        sort_column = Task.title.collate("NOCASE")
    else:
        sort_column = Task.created_at

    if order == SortOrder.ASC:
        statement = statement.order_by(sort_column)
    else:
        statement = statement.order_by(sort_column.desc())

    tasks = session.exec(statement).all()
    return tasks
```

**Validation**:
- Test with no tasks (should return empty array)
- Test with multiple tasks (should return all)
- Test status filter: all, pending, completed
- Test sorting: created asc/desc, title asc/desc
- Test user isolation (user A shouldn't see user B's tasks)

### Step 6: Implement Get Single Task Endpoint

```python
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """Get a specific task if it belongs to the authenticated user."""
    await verify_user_match(user_id, current_user_id)
    task = await get_user_task_or_404(task_id, current_user_id, session)
    return task
```

**Validation**:
- Test with owned task (should return task)
- Test with non-existent task ID (should return 404)
- Test with another user's task (should return 404, not 403)

### Step 7: Implement Update Task Endpoint

```python
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    user_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """Update a task's title and/or description."""
    await verify_user_match(user_id, current_user_id)
    task = await get_user_task_or_404(task_id, current_user_id, session)

    # Ensure at least one field is provided
    update_data = task_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one field must be provided for update"
        )

    # Apply updates
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
```

**Validation**:
- Test updating title only
- Test updating description only
- Test updating both fields
- Test with empty update (should return 422)
- Test with invalid validation (title too long, etc.)

### Step 8: Implement Delete Task Endpoint

```python
@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """Delete a task permanently."""
    await verify_user_match(user_id, current_user_id)
    task = await get_user_task_or_404(task_id, current_user_id, session)

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}
```

**Validation**:
- Test deleting owned task (should succeed)
- Test deleting non-existent task (should return 404)
- Test deleting another user's task (should return 404)
- Verify task is removed from database

### Step 9: Implement Toggle Completion Endpoint

```python
@router.patch("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    task_id: int,
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """Toggle the completion status of a task."""
    await verify_user_match(user_id, current_user_id)
    task = await get_user_task_or_404(task_id, current_user_id, session)

    # Toggle completed
    task.completed = not task.completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
```

**Validation**:
- Test toggling from false to true (complete task)
- Test toggling from true to false (reopen task)
- Test multiple toggles (should be idempotent)
- Verify updated_at changes on each toggle

### Step 10: Register Router in Main Application

**File**: `backend/src/main.py`

```python
from fastapi import FastAPI
from .api.routes import tasks

app = FastAPI(title="Todo API")

# Include task router
app.include_router(tasks.router)

# ... other routers (auth from Spec 1)
```

**Validation**:
- Start application: `uvicorn backend.src.main:app --reload`
- Visit `/docs` to see Swagger UI
- Verify all 6 task endpoints are listed
- Test each endpoint via Swagger UI

## Testing Strategy

### Integration Tests

**File**: `backend/tests/test_tasks.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from backend.src.main import app
from backend.src.core.database import get_session

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
    # Create test user and return JWT token headers
    # Implementation depends on Spec 1 auth system
    pass

def test_create_task(client, auth_headers):
    response = client.post(
        "/api/{user_id}/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] == False

def test_list_tasks(client, auth_headers):
    # Create multiple tasks
    # Test filtering and sorting
    pass

def test_user_isolation(client, auth_headers_user_a, auth_headers_user_b):
    # User A creates task
    # User B should not see User A's task
    pass

# ... more tests
```

### Security Tests

```python
def test_user_id_mismatch(client, auth_headers):
    """Test that user cannot access another user's endpoint."""
    response = client.get(
        "/api/{different_user_id}/tasks",
        headers=auth_headers
    )
    assert response.status_code == 403

def test_task_enumeration_prevention(client, auth_headers_user_a, auth_headers_user_b):
    """Test that 404 is returned (not 403) when accessing another user's task."""
    # User A creates task
    task_id = create_task_as_user_a()

    # User B tries to access task
    response = client.get(
        f"/api/{{user_b_id}}/tasks/{task_id}",
        headers=auth_headers_user_b
    )
    assert response.status_code == 404  # NOT 403
    assert "not found" in response.json()["detail"].lower()
```

## Common Issues and Solutions

### Issue: Foreign Key Constraint Violation

**Symptom**: Error when creating task: "foreign key constraint fails"

**Solution**: Ensure user exists in database before creating task. Verify `user_id` from JWT matches an actual user.

### Issue: User Can See Other Users' Tasks

**Symptom**: List endpoint returns tasks from multiple users

**Solution**: Verify `where(Task.user_id == current_user_id)` is applied in all queries.

### Issue: 403 Returned for Non-Existent Tasks

**Symptom**: Accessing non-existent task returns 403 instead of 404

**Solution**: Use combined query in `get_user_task_or_404` that returns 404 for both cases.

### Issue: Updated_at Not Changing

**Symptom**: updated_at timestamp doesn't update on modifications

**Solution**: Manually set `task.updated_at = datetime.utcnow()` in update and toggle operations.

## Performance Checklist

✅ **Indexes created**: `user_id` and `completed` columns
✅ **Queries filtered**: All queries include `user_id` filter
✅ **Batch operations**: Use `session.exec().all()` for list queries
✅ **Connection pooling**: Database connection pooled by SQLModel
✅ **Response time**: Test with 10,000+ tasks to verify <1s response

## Security Checklist

✅ **JWT validation**: All endpoints use `get_current_user_id` dependency
✅ **User ID matching**: All endpoints call `verify_user_match`
✅ **Ownership validation**: Update/delete/toggle use `get_user_task_or_404`
✅ **Enumeration prevention**: Return 404 (not 403) for non-owned tasks
✅ **Input validation**: Pydantic schemas validate all inputs
✅ **SQL injection prevention**: SQLModel parameterizes all queries

## Deployment Checklist

✅ **Environment variables**: DATABASE_URL, BETTER_AUTH_SECRET set
✅ **Database migration**: Task table created with indexes
✅ **CORS configuration**: Frontend origin allowed
✅ **API documentation**: `/docs` endpoint accessible
✅ **Health check**: Application starts without errors
✅ **Integration test**: All 6 endpoints functional

## Next Steps

After completing implementation:

1. Run `/sp.tasks` to generate detailed task list
2. Execute `/sp.implement` to perform implementation
3. Test all endpoints with real data
4. Deploy to Railway
5. Proceed to Spec 3 (frontend integration)

## References

- **Feature Specification**: [spec.md](./spec.md)
- **Data Model**: [data-model.md](./data-model.md)
- **API Contracts**: [contracts/task-api.yaml](./contracts/task-api.yaml)
- **Research**: [research.md](./research.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
