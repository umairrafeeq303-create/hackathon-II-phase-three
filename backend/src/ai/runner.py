"""
Agent execution runner with conversation history management.

Handles loading conversation history from database and executing agent
with retry logic for rate limits and failures.
"""
from typing import List, Dict, Any, Tuple
from uuid import UUID
from sqlmodel import Session, select
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import RateLimitError, APIConnectionError, APITimeoutError, OpenAIError

from ..models.message import Message
from ..db.session import get_session
from .agent import task_agent


def load_conversation_history(conversation_id: UUID, limit: int = 50) -> List[Dict[str, str]]:
    """
    Load conversation history from database.

    Retrieves last N messages for the conversation, ordered chronologically.
    Stateless function - creates new database session.

    Args:
        conversation_id: UUID of the conversation
        limit: Maximum number of messages to load (default: 50)

    Returns:
        List of message dicts in OpenAI format: [{"role": "user"|"assistant", "content": str}]
    """
    session = next(get_session())

    try:
        # Query messages ordered by created_at DESC, then reverse
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = session.exec(query).all()

        # Reverse to get chronological order (oldest first)
        messages.reverse()

        # Convert to OpenAI format
        history = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]

        return history

    finally:
        session.close()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(RateLimitError)
)
def call_openai_with_retry(
    messages: List[Dict[str, str]],
    tools: List[Dict[str, Any]],
    model: str
) -> Any:
    """
    Call OpenAI API with exponential backoff retry for rate limits.

    Retries up to 3 times with delays: 1s, 2s, 4s

    Args:
        messages: Conversation history + new message
        tools: Tool schemas for function calling
        model: Model name (e.g., gpt-3.5-turbo)

    Returns:
        OpenAI API response

    Raises:
        RateLimitError: After 3 failed retry attempts
    """
    return task_agent.client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )


def run_agent(
    user_message: str,
    conversation_history: List[Dict[str, str]],
    user_id: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Execute agent with conversation history and new user message.

    Handles tool calling and response generation with retry logic.
    Stateless function - receives all context as parameters.

    Args:
        user_message: New message from user
        conversation_history: Previous messages in conversation
        user_id: Authenticated user UUID (for tool calls)

    Returns:
        Tuple of (assistant_response: str, tool_calls: List[Dict])

    Raises:
        OpenAIError: If API call fails after retries
        Exception: For other errors (database, etc.)
    """
    # Build messages array: system prompt + history + new message
    messages = [
        {"role": "system", "content": task_agent.system_prompt}
    ] + conversation_history + [
        {"role": "user", "content": user_message}
    ]

    # Get tool schemas
    tools = task_agent.get_tool_schemas()

    try:
        # Call OpenAI API with retry logic
        response = call_openai_with_retry(
            messages=messages,
            tools=tools,
            model=task_agent.model
        )

        # Extract response
        message = response.choices[0].message
        assistant_response = message.content or ""

        # Track tool calls for transparency
        tool_calls_info = []

        # Handle tool calls if any
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Inject user_id into all tool calls
                tool_args["user_id"] = user_id

                # Execute tool
                tool_result = task_agent.execute_tool(tool_name, tool_args)

                # Record tool call for transparency
                tool_calls_info.append({
                    "tool": tool_name,
                    "parameters": tool_args,
                    "result": tool_result
                })

                # Add tool result to conversation for next API call
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call.model_dump()]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })

            # Get final response after tool execution
            final_response = call_openai_with_retry(
                messages=messages,
                tools=tools,
                model=task_agent.model
            )

            assistant_response = final_response.choices[0].message.content or assistant_response

        return (assistant_response, tool_calls_info)

    except RateLimitError as e:
        # Rate limit exceeded after retries
        raise Exception("I'm having trouble connecting right now. The service is experiencing high demand. Please try again in a moment.")

    except APIConnectionError as e:
        # Network connection error
        raise Exception("I'm having trouble connecting right now. Please check your internet connection and try again.")

    except APITimeoutError as e:
        # Request timeout
        raise Exception("That's taking longer than expected. Please try again.")

    except OpenAIError as e:
        # Other OpenAI API errors
        raise Exception(f"I encountered an error: {str(e)}. Please try again.")

    except Exception as e:
        # Unexpected errors
        raise Exception(f"Something went wrong: {str(e)}. Please try again.")
