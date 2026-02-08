"""
MCP Tool: complete_task

Marks a task as completed.
Validates user owns the task before updating.
Returns task_id, status, and title.
"""
from typing import Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from mcp import Tool
from mcp.types import TextContent

from ...models.task import Task
from ...db.session import get_session
from ..server import success_response, error_response


def complete_task_handler(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Handle complete_task MCP tool invocation.

    Stateless handler that marks a task as completed with ownership validation.

    Args:
        user_id: Authenticated user UUID (must match JWT claim)
        task_id: Task ID to mark as complete

    Returns:
        Success: {task_id: int, status: "completed", title: str}
        Error: {error: str, code: str}
    """
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

        # Update task to completed
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        return success_response(
            task_id=task.id,
            status="completed",
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
            "Failed to complete task",
            "DATABASE_ERROR"
        )
    finally:
        session.close()


# MCP Tool definition
complete_task_tool = Tool(
    name="complete_task",
    description="Mark a task as completed (validates user owns the task)",
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
                "description": "Task ID to mark as complete"
            }
        },
        "required": ["user_id", "task_id"]
    },
    fn=complete_task_handler
)
