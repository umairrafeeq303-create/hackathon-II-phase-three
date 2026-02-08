"""
Task CRUD API routes.
"""
from datetime import datetime
from typing import List, Literal, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from src.core.deps import get_current_user_id
from src.db.session import get_session
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse


# Helper functions
async def verify_user_match(user_id: str, current_user_id: str):
    """
    Verify URL user_id matches JWT user_id.

    Args:
        user_id: User ID from URL path parameter
        current_user_id: User ID from JWT token

    Raises:
        HTTPException: 400 if user_id format invalid, 403 if mismatch
    """
    try:
        url_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format",
        )

    token_user_id = UUID(current_user_id)

    if url_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: user_id mismatch",
        )


async def get_user_task_or_404(
    task_id: int, user_id: UUID, session: Session
) -> Task:
    """
    Get task by ID and verify ownership.

    Returns 404 if task not found OR not owned by user (enumeration prevention).

    Args:
        task_id: Task ID to retrieve
        user_id: User ID from JWT token
        session: Database session

    Returns:
        Task object if found and owned

    Raises:
        HTTPException: 404 if not found or not owned
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


# Router setup
router = APIRouter(prefix="/api/{user_id}/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_create: TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Create a new task for the authenticated user.

    Args:
        user_id: User ID from URL (must match JWT token)
        task_create: Task data (title required, description optional)
        session: Database session
        current_user_id: User ID from JWT token

    Returns:
        Created task with all fields

    Raises:
        HTTPException: 400 (invalid user_id), 403 (mismatch), 422 (validation error)
    """
    await verify_user_match(user_id, current_user_id)

    task = Task(
        user_id=UUID(current_user_id),
        title=task_create.title,
        description=task_create.description,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    status: Literal["all", "pending", "completed"] = Query(default="all"),
    sort: Literal["created_at", "updated_at", "title", "created", "updated"] = Query(default="created_at"),
    order: Literal["asc", "desc"] = Query(default="desc"),
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    List all tasks for the authenticated user with filtering and sorting.

    Args:
        user_id: User ID from URL (must match JWT token)
        status: Filter by completion status (all/pending/completed)
        sort: Sort by field (created/title)
        order: Sort order (asc/desc)
        session: Database session
        current_user_id: User ID from JWT token

    Returns:
        List of tasks matching filter criteria

    Raises:
        HTTPException: 400 (invalid user_id), 403 (mismatch)
    """
    await verify_user_match(user_id, current_user_id)

    # Build query
    statement = select(Task).where(Task.user_id == UUID(current_user_id))

    # Apply status filter
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)
    # "all" means no filter

    # Apply sorting
    if sort == "title":
        # Case-insensitive sorting for title
        from sqlalchemy import func
        sort_column = func.lower(Task.title).asc() if order == "asc" else func.lower(Task.title).desc()
    elif sort in ["updated_at", "updated"]:
        sort_column = Task.updated_at.asc() if order == "asc" else Task.updated_at.desc()
    else:  # sort in ["created_at", "created"] - default
        sort_column = Task.created_at.asc() if order == "asc" else Task.created_at.desc()

    statement = statement.order_by(sort_column)

    # Execute query
    tasks = session.exec(statement).all()

    return tasks


@router.get("/{id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Get a single task by ID.

    Args:
        user_id: User ID from URL (must match JWT token)
        id: Task ID to retrieve
        session: Database session
        current_user_id: User ID from JWT token

    Returns:
        Complete task object

    Raises:
        HTTPException: 400 (invalid user_id), 403 (mismatch or not owned), 404 (not found)
    """
    await verify_user_match(user_id, current_user_id)

    task = await get_user_task_or_404(id, UUID(current_user_id), session)

    return task


@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Update a task's title and/or description.

    Args:
        user_id: User ID from URL (must match JWT token)
        id: Task ID to update
        task_update: Update data (at least one field required)
        session: Database session
        current_user_id: User ID from JWT token

    Returns:
        Updated task object

    Raises:
        HTTPException: 400 (invalid user_id or no fields), 403 (mismatch or not owned), 404 (not found), 422 (validation error)
    """
    await verify_user_match(user_id, current_user_id)

    # Validate at least one field provided
    if task_update.title is None and task_update.description is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (title or description) must be provided",
        )

    task = await get_user_task_or_404(id, UUID(current_user_id), session)

    # Update provided fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{id}")
async def delete_task(
    user_id: str,
    id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Delete a task permanently.

    Args:
        user_id: User ID from URL (must match JWT token)
        id: Task ID to delete
        session: Database session
        current_user_id: User ID from JWT token

    Returns:
        Success message

    Raises:
        HTTPException: 400 (invalid user_id), 403 (mismatch or not owned), 404 (not found)
    """
    await verify_user_match(user_id, current_user_id)

    task = await get_user_task_or_404(id, UUID(current_user_id), session)

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/{id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Toggle a task's completion status (true ↔ false).

    Args:
        user_id: User ID from URL (must match JWT token)
        id: Task ID to toggle
        session: Database session
        current_user_id: User ID from JWT token

    Returns:
        Updated task with toggled completion status

    Raises:
        HTTPException: 400 (invalid user_id), 403 (mismatch or not owned), 404 (not found)
    """
    await verify_user_match(user_id, current_user_id)

    task = await get_user_task_or_404(id, UUID(current_user_id), session)

    # Toggle completion status
    task.completed = not task.completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
