"""
OpenAI Agent configuration for task management chatbot.

Initializes OpenAI client with API key and configures agent with MCP tools.
"""
from openai import OpenAI
from typing import List, Dict, Any
from ..core.config import settings
from ..mcp.tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool,
)
from .prompts import TASK_ASSISTANT_PROMPT


class TaskAgent:
    """
    AI Agent for natural language task management.

    Uses OpenAI's GPT-3.5-turbo model with MCP tools for task operations.
    Configured to be stateless - loads conversation history on each request.
    """

    def __init__(self):
        """Initialize OpenAI client and configure agent."""
        # Initialize OpenAI client with API key from settings
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Model configuration
        self.model = "gpt-3.5-turbo"  # Fast, cost-effective model
        self.system_prompt = TASK_ASSISTANT_PROMPT

        # MCP Tools - registered for agent to use
        self.tools = [
            add_task_tool,
            list_tasks_tool,
            complete_task_tool,
            delete_task_tool,
            update_task_tool,
        ]

        # Tool mapping for execution
        self.tool_map = {
            "add_task": add_task_tool.fn,
            "list_tasks": list_tasks_tool.fn,
            "complete_task": complete_task_tool.fn,
            "delete_task": delete_task_tool.fn,
            "update_task": update_task_tool.fn,
        }

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        Get tool schemas in OpenAI function calling format.

        Returns:
            List of tool schemas for OpenAI API
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            }
            for tool in self.tools
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool with given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool parameters

        Returns:
            Tool execution result
        """
        if tool_name not in self.tool_map:
            return {
                "error": f"Unknown tool: {tool_name}",
                "code": "INVALID_TOOL"
            }

        tool_fn = self.tool_map[tool_name]
        return tool_fn(**arguments)


# Global agent instance
task_agent = TaskAgent()
