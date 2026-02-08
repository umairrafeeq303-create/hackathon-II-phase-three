"""
MCP Server for Todo Task Management.

Provides 5 stateless tools for task operations:
- add_task: Create new task
- list_tasks: Retrieve user's tasks
- complete_task: Mark task as completed
- delete_task: Remove task
- update_task: Modify task

All tools validate user_id ownership before operations.
"""
from typing import Dict, Any, List
from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent


def success_response(task_id: int, status: str, title: str) -> Dict[str, Any]:
    """
    Generate standardized success response for MCP tools.

    Args:
        task_id: Task database ID
        status: Operation status (created, completed, deleted, updated)
        title: Task title

    Returns:
        Standardized success response dictionary
    """
    return {
        "task_id": task_id,
        "status": status,
        "title": title
    }


def error_response(error: str, code: str) -> Dict[str, Any]:
    """
    Generate standardized error response for MCP tools.

    Args:
        error: Human-readable error message
        code: Error code (NOT_FOUND, UNAUTHORIZED, VALIDATION_ERROR, DATABASE_ERROR)

    Returns:
        Standardized error response dictionary
    """
    return {
        "error": error,
        "code": code
    }


# MCP Server instance will be initialized with tools
def create_mcp_server() -> Server:
    """
    Create and configure MCP server with all task management tools.

    Returns:
        Configured MCP Server instance
    """
    from .tools import (
        add_task_tool,
        list_tasks_tool,
        complete_task_tool,
        delete_task_tool,
        update_task_tool,
    )

    server = Server("todo-task-manager")

    # Register all tools
    server.add_tool(add_task_tool)
    server.add_tool(list_tasks_tool)
    server.add_tool(complete_task_tool)
    server.add_tool(delete_task_tool)
    server.add_tool(update_task_tool)

    return server
