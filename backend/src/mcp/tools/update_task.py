"""
MCP Tool: update_task

Updates task title and/or description.
Validates user owns the task.
At least one of title or description must be provided.
Returns task_id, status, and updated title.
"""
from typing import Dict, Any, Optional
from uuid import UUID
from sqlmodel import Session, select
from mcp import Tool
from mcp.types import TextContent

from ...models.task import Task
from ...db.session import get_session
from ..server import success_response, error_response


def update_task_handler(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Handle update_task MCP tool invocation.

    Stateless handler that updates a task with ownership validation.

    Args:
        user_id: Authenticated user UUID (must match JWT claim)
        task_id: Task ID to update
        title: New task title (optional, 1-200 characters)
        description: New task description (optional, max 1000 characters)

    Returns:
        Success: {task_id: int, status: "updated", title: str}
        Error: {error: str, code: str}
    """
    # Validate at least one field is provided
    if title is None and description is None:
        return error_response(
            "Must provide at least one of: title, description",
            "VALIDATION_ERROR"
        )

    # Validate title if provided
    if title is not None:
        if len(title.strip()) == 0:
            return error_response(
                "Title cannot be empty",
                "VALIDATION_ERROR"
            )
        if len(title) > 200:
            return error_response(
                "Title too long (max 200 characters)",
                "VALIDATION_ERROR"
            )

    # Validate description if provided
    if description is not None and len(description) > 1000:
        return error_response(
            "Description too long (max 1000 characters)",
            "VALIDATION_ERROR"
        )

    # Get database session (stateless - new session per invocation)
    try:
        session = next(get_session())
    except Exception as e:
        return error_response(
            "Database connection error",
            "DATABASE_ERROR"
        )

    try:
        # Query task with ownership validation
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == UUID(user_id)
        )
        task = session.exec(query).first()

        # Task not found or ownership violation
        if not task:
            return error_response(
                "Task not found or access denied",
                "NOT_FOUND"
            )

        # Update fields if provided
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description else None

        session.add(task)
        session.commit()
        session.refresh(task)

        return success_response(
            task_id=task.id,
            status="updated",
            title=task.title
        )

    except ValueError as e:
        # Invalid UUID format
        return error_response(
            f"Invalid user_id format: {str(e)}",
            "VALIDATION_ERROR"
        )
    except Exception as e:
        # Database errors
        session.rollback()
        return error_response(
            "Failed to update task",
            "DATABASE_ERROR"
        )
    finally:
        session.close()


# MCP Tool definition
update_task_tool = Tool(
    name="update_task",
    description="Update task title and/or description (validates user owns the task)",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "format": "uuid",
                "description": "Authenticated user UUID"
            },
            "task_id": {
                "type": "integer",
                "description": "Task ID to update"
            },
            "title": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200,
                "description": "New task title (optional)"
            },
            "description": {
                "type": "string",
                "maxLength": 1000,
                "description": "New task description (optional)"
            }
        },
        "required": ["user_id", "task_id"]
    },
    fn=update_task_handler
)
