"""
MCP Tool: add_task

Creates a new task for the authenticated user.
Validates user_id, title length, and description length.
Returns standardized response with task_id, status, and title.
"""
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from mcp import Tool
from mcp.types import TextContent

from ...models.task import Task
from ...db.session import get_session
from ..server import success_response, error_response


def add_task_handler(user_id: str, title: str, description: str | None = None) -> Dict[str, Any]:
    """
    Handle add_task MCP tool invocation.

    Stateless handler that creates a new task for the specified user.

    Args:
        user_id: Authenticated user UUID (must match JWT claim)
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        Success: {task_id: int, status: "created", title: str}
        Error: {error: str, code: str}
    """
    # Validate title
    if not title or len(title.strip()) == 0:
        return error_response(
            "Title is required",
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
        # Create task
        task = Task(
            user_id=UUID(user_id),
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return success_response(
            task_id=task.id,
            status="created",
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
            "Failed to create task",
            "DATABASE_ERROR"
        )
    finally:
        session.close()


# MCP Tool definition
add_task_tool = Tool(
    name="add_task",
    description="Create a new task for the authenticated user",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "format": "uuid",
                "description": "Authenticated user UUID (must match JWT claim)"
            },
            "title": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200,
                "description": "Task title"
            },
            "description": {
                "type": "string",
                "maxLength": 1000,
                "description": "Optional task description"
            }
        },
        "required": ["user_id", "title"]
    },
    fn=add_task_handler
)
