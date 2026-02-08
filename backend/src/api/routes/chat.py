"""
Chat API routes for AI task assistant.

Provides natural language conversation interface for task management.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.core.deps import get_current_user_id
from src.db.session import get_session
from src.models.conversation import Conversation
from src.models.message import Message
from src.schemas.chat import ChatRequest, ChatResponse, ToolCall
from src.ai.runner import run_agent, load_conversation_history


# Helper function (reused from tasks.py)
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


# Router setup
router = APIRouter(prefix="/api/{user_id}/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Send a message to the AI task assistant and get a response.

    Stateless chat endpoint that:
    1. Validates user authentication
    2. Loads or creates conversation
    3. Loads conversation history from database
    4. Stores user message
    5. Executes AI agent with tool calling
    6. Stores assistant response
    7. Returns response with tool call transparency

    Args:
        user_id: User ID from URL (must match JWT token)
        request: ChatRequest with message and optional conversation_id
        session: Database session
        current_user_id: User ID from JWT token

    Returns:
        ChatResponse with conversation_id, assistant response, and tool calls

    Raises:
        HTTPException:
            - 400 (invalid user_id or conversation_id)
            - 403 (user_id mismatch or conversation ownership violation)
            - 404 (conversation not found)
            - 500 (agent execution error)

    Security:
        - Validates JWT token
        - Validates URL user_id matches token user_id
        - Validates conversation ownership before access
        - Injects authenticated user_id into all tool calls
    """
    # Validate user_id matches JWT
    await verify_user_match(user_id, current_user_id)
    user_uuid = UUID(current_user_id)

    try:
        # Step 1: Load or create conversation
        conversation: Optional[Conversation] = None

        if request.conversation_id:
            # Load existing conversation and verify ownership
            conversation = session.get(Conversation, request.conversation_id)

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )

            if conversation.user_id != user_uuid:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden: conversation ownership violation",
                )
        else:
            # Create new conversation
            conversation = Conversation(
                id=uuid4(),
                user_id=user_uuid,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Step 2: Load conversation history (last 50 messages)
        history = load_conversation_history(conversation.id, limit=50)

        # Step 3: Store user message
        user_message = Message(
            id=uuid4(),
            conversation_id=conversation.id,
            role="user",
            content=request.message,
            created_at=datetime.utcnow(),
        )
        session.add(user_message)
        session.commit()

        # Step 4: Execute AI agent
        try:
            assistant_response, tool_calls_info = run_agent(
                user_message=request.message,
                conversation_history=history,
                user_id=current_user_id,
            )
        except Exception as e:
            # Agent execution failed - still store user message but return error
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

        # Step 5: Store assistant response
        assistant_message = Message(
            id=uuid4(),
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_response,
            created_at=datetime.utcnow(),
        )
        session.add(assistant_message)

        # Step 6: Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

        session.commit()
        session.refresh(assistant_message)

        # Step 7: Format tool calls for response
        tool_calls = [
            ToolCall(
                tool=tc["tool"],
                parameters=tc["parameters"],
                result=tc["result"],
            )
            for tc in tool_calls_info
        ]

        # Step 8: Return response
        return ChatResponse(
            conversation_id=conversation.id,
            response=assistant_response,
            tool_calls=tool_calls,
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, 404s, etc.)
        session.rollback()
        raise
    except ValueError as e:
        # Invalid UUID format
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid conversation_id format: {str(e)}",
        )
    except Exception as e:
        # Unexpected errors
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}",
        )
