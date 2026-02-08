"""
MCP Tool: list_tasks

Retrieves tasks for the authenticated user.
Supports filtering by status (all, pending, completed).
Returns array of tasks with full details.
"""
from typing import Dict, Any, List
from uuid import UUID
from sqlmodel import Session, select
from mcp import Tool
from mcp.types import TextContent

from ...models.task import Task
from ...db.session import get_session
from ..server import error_response


def list_tasks_handler(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    Handle list_tasks MCP tool invocation.

    Stateless handler that retrieves tasks for the specified user.

    Args:
        user_id: Authenticated user UUID (must match JWT claim)
        status: Filter by status - "all", "pending", or "completed" (default: "all")

    Returns:
        Success: {tasks: List[{id, title, description, completed, created_at}]}
        Error: {error: str, code: str}
    """
    # Validate status parameter
    if status not in ("all", "pending", "completed"):
        return error_response(
            f"Invalid status: {status}. Must be 'all', 'pending', or 'completed'",
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
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == UUID(user_id))

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Order by created_at DESC for consistent ordering
        query = query.order_by(Task.created_at.desc())

        # Execute query
        results = session.exec(query).all()

        # Convert to response format
        tasks = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
            for task in results
        ]

        return {"tasks": tasks}

    except ValueError as e:
        # Invalid UUID format
        return error_response(
            f"Invalid user_id format: {str(e)}",
            "VALIDATION_ERROR"
        )
    except Exception as e:
        # Database errors
        return error_response(
            "Failed to retrieve tasks",
            "DATABASE_ERROR"
        )
    finally:
        session.close()


# MCP Tool definition
list_tasks_tool = Tool(
    name="list_tasks",
    description="Retrieve tasks for the authenticated user, optionally filtered by status",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "format": "uuid",
                "description": "Authenticated user UUID"
            },
            "status": {
                "type": "string",
                "enum": ["all", "pending", "completed"],
                "default": "all",
                "description": "Filter by task status"
            }
        },
        "required": ["user_id"]
    },
    fn=list_tasks_handler
)
