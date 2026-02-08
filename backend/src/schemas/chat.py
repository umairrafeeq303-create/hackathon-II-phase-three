"""
Pydantic schemas for AI chatbot API.

Request/response models for chat endpoint with validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from uuid import UUID


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="User message (1-10000 characters)"
    )
    conversation_id: Optional[UUID] = Field(
        None,
        description="Optional conversation ID to continue existing conversation"
    )

    @validator('message')
    def validate_message(cls, v):
        """Ensure message is not just whitespace."""
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace")
        return v.strip()


class ToolCall(BaseModel):
    """Tool call information for transparency."""
    tool: str = Field(..., description="Tool name that was executed")
    parameters: Dict[str, Any] = Field(..., description="Parameters passed to tool")
    result: Dict[str, Any] = Field(..., description="Tool execution result")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    conversation_id: UUID = Field(..., description="Conversation ID for this exchange")
    response: str = Field(..., description="AI assistant response")
    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="List of tool calls made during this interaction"
    )

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "response": "Got it! I've added 'Buy groceries' to your task list.",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "parameters": {
                            "user_id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "Buy groceries"
                        },
                        "result": {
                            "task_id": 1,
                            "status": "created",
                            "title": "Buy groceries"
                        }
                    }
                ]
            }
        }
