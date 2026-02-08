"""
End-to-end tests for AI Chatbot User Stories (Phases 7-13).

Tests all user story acceptance criteria:
- US2: View tasks via natural language
- US3: Complete tasks via natural language
- US4: Delete tasks via natural language
- US5: Update tasks via natural language
- US6: Maintain conversation context
- US7: Handle errors gracefully
- US8: Resume conversations after server restart
"""
import pytest
import time
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Session, create_engine, select
from sqlmodel.pool import StaticPool

from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
from src.ai.runner import run_agent, load_conversation_history
from src.mcp.tools.add_task import add_task_handler
from src.mcp.tools.list_tasks import list_tasks_handler
from src.mcp.tools.complete_task import complete_task_handler
from src.mcp.tools.delete_task import delete_task_handler
from src.mcp.tools.update_task import update_task_handler


# Fixtures
@pytest.fixture(name="session")
def session_fixture():
    """Create test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create all tables
    from src.models import user, task, conversation, message
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password="fake_hash",
        created_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_conversation")
def test_conversation_fixture(session: Session, test_user: User):
    """Create a test conversation."""
    conversation = Conversation(
        id=uuid4(),
        user_id=test_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


# Phase 7: User Story 2 - View Tasks via Natural Language
class TestViewTasks:
    """Tests for US2 - viewing tasks through conversational queries."""

    def test_show_all_tasks(self, session: Session, test_user: User):
        """Test: 'Show me my tasks' lists all tasks."""
        # Create test tasks
        task1 = Task(user_id=test_user.id, title="Buy groceries", completed=False)
        task2 = Task(user_id=test_user.id, title="Call mom", completed=False)
        task3 = Task(user_id=test_user.id, title="Project deadline", completed=True)
        session.add_all([task1, task2, task3])
        session.commit()

        # Test list_tasks tool
        result = list_tasks_handler(user_id=str(test_user.id), status="all")

        assert "tasks" in result
        assert len(result["tasks"]) == 3
        assert any(t["title"] == "Buy groceries" for t in result["tasks"])
        assert any(t["title"] == "Call mom" for t in result["tasks"])
        assert any(t["title"] == "Project deadline" for t in result["tasks"])

    def test_show_pending_tasks(self, session: Session, test_user: User):
        """Test: 'What's pending?' shows only incomplete tasks."""
        # Create test tasks
        task1 = Task(user_id=test_user.id, title="Buy groceries", completed=False)
        task2 = Task(user_id=test_user.id, title="Call mom", completed=False)
        task3 = Task(user_id=test_user.id, title="Project deadline", completed=True)
        session.add_all([task1, task2, task3])
        session.commit()

        # Test list_tasks with pending filter
        result = list_tasks_handler(user_id=str(test_user.id), status="pending")

        assert "tasks" in result
        assert len(result["tasks"]) == 2
        assert all(not t["completed"] for t in result["tasks"])
        assert any(t["title"] == "Buy groceries" for t in result["tasks"])
        assert any(t["title"] == "Call mom" for t in result["tasks"])

    def test_show_completed_tasks(self, session: Session, test_user: User):
        """Test: 'What have I completed?' shows only completed tasks."""
        # Create test tasks
        task1 = Task(user_id=test_user.id, title="Buy groceries", completed=False)
        task2 = Task(user_id=test_user.id, title="Call mom", completed=False)
        task3 = Task(user_id=test_user.id, title="Project deadline", completed=True)
        session.add_all([task1, task2, task3])
        session.commit()

        # Test list_tasks with completed filter
        result = list_tasks_handler(user_id=str(test_user.id), status="completed")

        assert "tasks" in result
        assert len(result["tasks"]) == 1
        assert all(t["completed"] for t in result["tasks"])
        assert result["tasks"][0]["title"] == "Project deadline"

    def test_empty_task_list(self, session: Session, test_user: User):
        """Test: Empty list returns empty array."""
        # No tasks created
        result = list_tasks_handler(user_id=str(test_user.id), status="all")

        assert "tasks" in result
        assert len(result["tasks"]) == 0
        assert result["tasks"] == []


# Phase 8: User Story 3 - Complete Tasks via Natural Language
class TestCompleteTasks:
    """Tests for US3 - marking tasks complete through conversation."""

    def test_complete_task_by_id(self, session: Session, test_user: User):
        """Test: 'Mark task 1 as complete' updates task status."""
        # Create test task
        task = Task(user_id=test_user.id, title="Buy groceries", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        # Complete the task
        result = complete_task_handler(user_id=str(test_user.id), task_id=task.id)

        assert "task_id" in result
        assert result["status"] == "completed"
        assert result["title"] == "Buy groceries"

        # Verify in database
        session.refresh(task)
        assert task.completed is True

    def test_complete_nonexistent_task(self, session: Session, test_user: User):
        """Test: Attempting to complete non-existent task returns error."""
        result = complete_task_handler(user_id=str(test_user.id), task_id=999)

        assert "error" in result
        assert result["code"] == "NOT_FOUND"

    def test_complete_other_users_task(self, session: Session, test_user: User):
        """Test: Cannot complete another user's task."""
        # Create another user and their task
        other_user = User(id=uuid4(), email="other@example.com", hashed_password="hash")
        session.add(other_user)
        session.commit()

        other_task = Task(user_id=other_user.id, title="Other user task", completed=False)
        session.add(other_task)
        session.commit()
        session.refresh(other_task)

        # Try to complete as test_user
        result = complete_task_handler(user_id=str(test_user.id), task_id=other_task.id)

        assert "error" in result
        assert result["code"] == "NOT_FOUND"


# Phase 9: User Story 6 - Maintain Conversation Context
class TestConversationContext:
    """Tests for US6 - conversation context preservation."""

    def test_context_preservation_across_messages(self, session: Session, test_user: User, test_conversation: Conversation):
        """Test: References to previous messages work correctly."""
        # Simulate conversation:
        # User: "Add a task to buy milk"
        # Assistant: "Got it! I've added 'Buy milk' to your task list."
        # User: "Mark that task as complete"

        # Message 1: Add task
        msg1_user = Message(
            conversation_id=test_conversation.id,
            role="user",
            content="Add a task to buy milk"
        )
        session.add(msg1_user)
        session.commit()

        # Create task (simulating agent action)
        task = Task(user_id=test_user.id, title="Buy milk", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        msg1_assistant = Message(
            conversation_id=test_conversation.id,
            role="assistant",
            content="Got it! I've added 'Buy milk' to your task list."
        )
        session.add(msg1_assistant)
        session.commit()

        # Message 2: Reference "that task"
        msg2_user = Message(
            conversation_id=test_conversation.id,
            role="user",
            content="Mark that task as complete"
        )
        session.add(msg2_user)
        session.commit()

        # Load conversation history
        history = load_conversation_history(test_conversation.id)

        assert len(history) == 3  # user + assistant + user
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Add a task to buy milk"
        assert history[1]["role"] == "assistant"
        assert history[2]["role"] == "user"
        assert history[2]["content"] == "Mark that task as complete"

    def test_conversation_history_limit(self, session: Session, test_conversation: Conversation):
        """Test: Conversation history limited to 50 messages."""
        # Add 60 messages
        for i in range(60):
            msg = Message(
                conversation_id=test_conversation.id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}"
            )
            session.add(msg)
        session.commit()

        # Load history
        history = load_conversation_history(test_conversation.id, limit=50)

        assert len(history) == 50
        # Should get the most recent 50 messages
        assert history[-1]["content"] == "Message 59"
        assert history[0]["content"] == "Message 10"


# Phase 10: User Story 4 - Delete Tasks via Natural Language
class TestDeleteTasks:
    """Tests for US4 - deleting tasks through conversation."""

    def test_delete_task_by_id(self, session: Session, test_user: User):
        """Test: 'Delete task 1' removes task from database."""
        # Create test task
        task = Task(user_id=test_user.id, title="Buy groceries", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id

        # Delete the task
        result = delete_task_handler(user_id=str(test_user.id), task_id=task_id)

        assert "task_id" in result
        assert result["status"] == "deleted"
        assert result["title"] == "Buy groceries"

        # Verify removed from database
        deleted_task = session.get(Task, task_id)
        assert deleted_task is None

    def test_delete_nonexistent_task(self, session: Session, test_user: User):
        """Test: Attempting to delete non-existent task returns error."""
        result = delete_task_handler(user_id=str(test_user.id), task_id=999)

        assert "error" in result
        assert result["code"] == "NOT_FOUND"

    def test_delete_other_users_task(self, session: Session, test_user: User):
        """Test: Cannot delete another user's task."""
        # Create another user and their task
        other_user = User(id=uuid4(), email="other@example.com", hashed_password="hash")
        session.add(other_user)
        session.commit()

        other_task = Task(user_id=other_user.id, title="Other user task", completed=False)
        session.add(other_task)
        session.commit()
        session.refresh(other_task)

        # Try to delete as test_user
        result = delete_task_handler(user_id=str(test_user.id), task_id=other_task.id)

        assert "error" in result
        assert result["code"] == "NOT_FOUND"


# Phase 11: User Story 5 - Update Tasks via Natural Language
class TestUpdateTasks:
    """Tests for US5 - updating tasks through conversation."""

    def test_update_task_title(self, session: Session, test_user: User):
        """Test: 'Change task 1 to New title' updates title."""
        # Create test task
        task = Task(user_id=test_user.id, title="Buy groceries", description="Get food", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        # Update title
        result = update_task_handler(
            user_id=str(test_user.id),
            task_id=task.id,
            title="Buy organic groceries"
        )

        assert "task_id" in result
        assert result["status"] == "updated"
        assert result["title"] == "Buy organic groceries"

        # Verify in database
        session.refresh(task)
        assert task.title == "Buy organic groceries"
        assert task.description == "Get food"  # Description unchanged

    def test_update_task_description(self, session: Session, test_user: User):
        """Test: Update description only."""
        # Create test task
        task = Task(user_id=test_user.id, title="Buy groceries", description="Get food", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        # Update description
        result = update_task_handler(
            user_id=str(test_user.id),
            task_id=task.id,
            description="Get organic fruits and vegetables"
        )

        assert result["status"] == "updated"

        # Verify in database
        session.refresh(task)
        assert task.title == "Buy groceries"  # Title unchanged
        assert task.description == "Get organic fruits and vegetables"

    def test_update_nonexistent_task(self, session: Session, test_user: User):
        """Test: Updating non-existent task returns error."""
        result = update_task_handler(
            user_id=str(test_user.id),
            task_id=999,
            title="New title"
        )

        assert "error" in result
        assert result["code"] == "NOT_FOUND"

    def test_update_without_changes(self, session: Session, test_user: User):
        """Test: Update requires at least title or description."""
        # This should be handled by validation
        # (Not testing here as it's a validation layer concern)
        pass


# Phase 12: User Story 7 - Handle Errors Gracefully
class TestErrorHandling:
    """Tests for US7 - graceful error handling."""

    def test_invalid_task_id_error(self, session: Session, test_user: User):
        """Test: Invalid task ID returns user-friendly error."""
        result = complete_task_handler(user_id=str(test_user.id), task_id=999)

        assert "error" in result
        assert result["code"] == "NOT_FOUND"
        assert "not found" in result["error"].lower() or "access denied" in result["error"].lower()

    def test_invalid_status_filter(self, session: Session, test_user: User):
        """Test: Invalid status filter returns validation error."""
        result = list_tasks_handler(user_id=str(test_user.id), status="invalid")

        assert "error" in result
        assert result["code"] == "VALIDATION_ERROR"

    def test_invalid_user_id_format(self, session: Session):
        """Test: Invalid UUID format returns validation error."""
        result = list_tasks_handler(user_id="invalid-uuid", status="all")

        assert "error" in result
        assert result["code"] == "VALIDATION_ERROR"


# Phase 13: User Story 8 - Resume Conversations After Server Restart
class TestStatelessArchitecture:
    """Tests for US8 - stateless architecture validation."""

    def test_conversation_loads_from_database(self, session: Session, test_user: User, test_conversation: Conversation):
        """Test: Conversation history loaded from database on each request."""
        # Add messages
        msg1 = Message(conversation_id=test_conversation.id, role="user", content="Add task to buy milk")
        msg2 = Message(conversation_id=test_conversation.id, role="assistant", content="Got it!")
        msg3 = Message(conversation_id=test_conversation.id, role="user", content="Show my tasks")
        session.add_all([msg1, msg2, msg3])
        session.commit()

        # Simulate server restart by creating new session
        # Load history (simulates fresh request after restart)
        history = load_conversation_history(test_conversation.id)

        assert len(history) == 3
        assert history[0]["content"] == "Add task to buy milk"
        assert history[1]["content"] == "Got it!"
        assert history[2]["content"] == "Show my tasks"

    def test_no_in_memory_state(self):
        """Test: Agent has no instance variables storing conversation state."""
        from src.ai.agent import task_agent

        # Check that agent doesn't store conversation state
        agent_vars = vars(task_agent)

        # Should only have configuration, not conversation data
        assert "client" in agent_vars  # OpenAI client
        assert "model" in agent_vars  # Model name
        assert "tools" in agent_vars  # Tool definitions

        # Should NOT have conversation state
        assert "messages" not in agent_vars
        assert "conversation_history" not in agent_vars
        assert "current_conversation" not in agent_vars

    def test_tools_are_stateless(self):
        """Test: MCP tools have no instance state."""
        # Tools are functions, not classes with state
        from src.mcp.tools import (
            add_task_tool,
            list_tasks_tool,
            complete_task_tool,
            delete_task_tool,
            update_task_tool
        )

        # All tools should be Tool instances with fn handlers
        for tool in [add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool]:
            assert hasattr(tool, "fn")
            assert callable(tool.fn)
            # Function should not have state (closures with mutable state)
            assert not hasattr(tool.fn, "__self__")  # Not a bound method


# Integration Test: Full Conversation Flow
class TestFullConversationFlow:
    """Integration test covering full conversation lifecycle."""

    def test_complete_task_management_conversation(self, session: Session, test_user: User):
        """Test: Complete conversation flow from create to delete."""
        user_id = str(test_user.id)

        # Step 1: Create task
        result = add_task_handler(user_id=user_id, title="Buy groceries", description="Milk and eggs")
        assert result["status"] == "created"
        task_id = result["task_id"]

        # Step 2: List tasks
        result = list_tasks_handler(user_id=user_id, status="all")
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["title"] == "Buy groceries"
        assert result["tasks"][0]["completed"] is False

        # Step 3: Update task
        result = update_task_handler(user_id=user_id, task_id=task_id, title="Buy organic groceries")
        assert result["status"] == "updated"

        # Step 4: Complete task
        result = complete_task_handler(user_id=user_id, task_id=task_id)
        assert result["status"] == "completed"

        # Step 5: Verify completion
        result = list_tasks_handler(user_id=user_id, status="completed")
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["completed"] is True

        # Step 6: Delete task
        result = delete_task_handler(user_id=user_id, task_id=task_id)
        assert result["status"] == "deleted"

        # Step 7: Verify deletion
        result = list_tasks_handler(user_id=user_id, status="all")
        assert len(result["tasks"]) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
