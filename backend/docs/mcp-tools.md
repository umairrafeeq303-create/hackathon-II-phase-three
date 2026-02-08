# MCP Tools Documentation

**MCP (Model Context Protocol)** tools are stateless functions that the AI agent can invoke to perform task operations. Each tool validates user ownership, handles errors gracefully, and returns standardized responses.

## Overview

The AI Chatbot uses **5 MCP tools** for task management:

| Tool | Purpose | User Input Example |
|------|---------|-------------------|
| `add_task` | Create new tasks | "Add a task to buy milk" |
| `list_tasks` | Retrieve tasks | "Show me my tasks" |
| `complete_task` | Mark tasks done | "Mark task 1 as complete" |
| `delete_task` | Remove tasks | "Delete task 2" |
| `update_task` | Modify tasks | "Change task 1 to call mom" |

---

## Tool 1: add_task

**Purpose**: Create a new task for the authenticated user

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user UUID (required)"
    },
    "title": {
      "type": "string",
      "maxLength": 200,
      "description": "Task title (required, max 200 chars)"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "description": "Task description (optional, max 1000 chars)"
    }
  },
  "required": ["user_id", "title"]
}
```

### Output Schema

**Success**:
```json
{
  "task_id": 42,
  "status": "created",
  "title": "Buy groceries"
}
```

**Error**:
```json
{
  "error": "Title required (max 200 chars)",
  "code": "VALIDATION_ERROR"
}
```

### Examples

#### Example 1: Simple Task

**User**: "Add a task to buy milk"

**Agent Invocation**:
```json
{
  "tool": "add_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy milk"
  }
}
```

**Tool Response**:
```json
{
  "task_id": 1,
  "status": "created",
  "title": "Buy milk"
}
```

**Agent Response**: "Got it! I've added 'Buy milk' to your task list."

#### Example 2: Task with Description

**User**: "I need to remember to buy groceries - milk, eggs, and bread"

**Agent Invocation**:
```json
{
  "tool": "add_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "milk, eggs, and bread"
  }
}
```

**Tool Response**:
```json
{
  "task_id": 2,
  "status": "created",
  "title": "Buy groceries"
}
```

**Agent Response**: "Got it! I've added 'Buy groceries' to your task list with the details: milk, eggs, and bread."

### Error Handling

| Error Code | Condition | User-Friendly Message |
|-----------|-----------|----------------------|
| `VALIDATION_ERROR` | Title empty or > 200 chars | "Please provide a task title (max 200 characters)" |
| `VALIDATION_ERROR` | Description > 1000 chars | "Description is too long (max 1000 characters)" |
| `DATABASE_ERROR` | Database connection fails | "I'm having trouble saving right now. Please try again in a moment." |

### Implementation

**File**: `backend/src/mcp/tools/add_task.py`

**Key Features**:
- Validates title length (1-200 characters)
- Validates description length (0-1000 characters)
- Sets `completed=False` by default
- Returns task ID for future reference
- Stateless design (no instance variables)

---

## Tool 2: list_tasks

**Purpose**: Retrieve tasks for the authenticated user with optional filtering

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user UUID (required)"
    },
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "default": "all",
      "description": "Filter by task status (optional)"
    }
  },
  "required": ["user_id"]
}
```

### Output Schema

**Success**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy milk",
      "description": null,
      "completed": false,
      "created_at": "2026-01-27T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Call mom",
      "description": "Tonight at 8pm",
      "completed": false,
      "created_at": "2026-01-27T11:15:00Z"
    }
  ]
}
```

**Error**:
```json
{
  "error": "Invalid status: invalid_status. Must be 'all', 'pending', or 'completed'",
  "code": "VALIDATION_ERROR"
}
```

### Examples

#### Example 1: Show All Tasks

**User**: "Show me my tasks"

**Agent Invocation**:
```json
{
  "tool": "list_tasks",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "all"
  }
}
```

**Tool Response**:
```json
{
  "tasks": [
    {"id": 1, "title": "Buy milk", "completed": false},
    {"id": 2, "title": "Call mom", "completed": false},
    {"id": 3, "title": "Finish report", "completed": true}
  ]
}
```

**Agent Response**: "You have 3 tasks: 1. Buy milk, 2. Call mom, 3. Finish report (completed)"

#### Example 2: Show Pending Tasks

**User**: "What's pending?"

**Agent Invocation**:
```json
{
  "tool": "list_tasks",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending"
  }
}
```

**Tool Response**:
```json
{
  "tasks": [
    {"id": 1, "title": "Buy milk", "completed": false},
    {"id": 2, "title": "Call mom", "completed": false}
  ]
}
```

**Agent Response**: "You have 2 pending tasks: 1. Buy milk, 2. Call mom"

#### Example 3: Empty List

**User**: "Show my completed tasks"

**Agent Invocation**:
```json
{
  "tool": "list_tasks",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed"
  }
}
```

**Tool Response**:
```json
{
  "tasks": []
}
```

**Agent Response**: "Your task list is empty. Would you like to add something?"

### Error Handling

| Error Code | Condition | User-Friendly Message |
|-----------|-----------|----------------------|
| `VALIDATION_ERROR` | Invalid status value | "Please specify 'all', 'pending', or 'completed'" |
| `VALIDATION_ERROR` | Invalid user_id format | "There was a problem with your request" |
| `DATABASE_ERROR` | Database query fails | "I'm having trouble retrieving your tasks right now" |

### Implementation

**File**: `backend/src/mcp/tools/list_tasks.py`

**Key Features**:
- Filters by user_id (enforces ownership)
- Supports status filtering (all/pending/completed)
- Orders by created_at DESC (newest first)
- Returns full task details with timestamps
- Stateless design

---

## Tool 3: complete_task

**Purpose**: Mark a task as completed

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user UUID (required)"
    },
    "task_id": {
      "type": "integer",
      "description": "Task ID to complete (required)"
    }
  },
  "required": ["user_id", "task_id"]
}
```

### Output Schema

**Success**:
```json
{
  "task_id": 1,
  "status": "completed",
  "title": "Buy milk"
}
```

**Error**:
```json
{
  "error": "Task not found or access denied",
  "code": "NOT_FOUND"
}
```

### Examples

#### Example 1: Complete by ID

**User**: "Mark task 1 as complete"

**Agent Invocation**:
```json
{
  "tool": "complete_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": 1
  }
}
```

**Tool Response**:
```json
{
  "task_id": 1,
  "status": "completed",
  "title": "Buy milk"
}
```

**Agent Response**: "Great job! I've marked 'Buy milk' as complete."

#### Example 2: Complete with Context

**User**: "I finished buying the groceries"

**Agent Invocation** (after searching context for "groceries" task):
```json
{
  "tool": "complete_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": 2
  }
}
```

**Tool Response**:
```json
{
  "task_id": 2,
  "status": "completed",
  "title": "Buy groceries"
}
```

**Agent Response**: "Awesome! I've marked 'Buy groceries' as complete."

### Error Handling

| Error Code | Condition | User-Friendly Message |
|-----------|-----------|----------------------|
| `NOT_FOUND` | Task doesn't exist | "I couldn't find that task. Would you like to see your current tasks?" |
| `NOT_FOUND` | Task belongs to another user | "I couldn't find that task. Would you like to see your current tasks?" |
| `DATABASE_ERROR` | Database update fails | "I'm having trouble updating right now. Please try again." |

### Implementation

**File**: `backend/src/mcp/tools/complete_task.py`

**Key Features**:
- Validates ownership (user_id must match task's user_id)
- Updates `completed` field to `True`
- Returns task title for confirmation
- Security: Cannot complete other users' tasks
- Stateless design

---

## Tool 4: delete_task

**Purpose**: Remove a task from the database

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user UUID (required)"
    },
    "task_id": {
      "type": "integer",
      "description": "Task ID to delete (required)"
    }
  },
  "required": ["user_id", "task_id"]
}
```

### Output Schema

**Success**:
```json
{
  "task_id": 1,
  "status": "deleted",
  "title": "Buy milk"
}
```

**Error**:
```json
{
  "error": "Task not found or access denied",
  "code": "NOT_FOUND"
}
```

### Examples

#### Example 1: Delete by ID

**User**: "Delete task 3"

**Agent Invocation**:
```json
{
  "tool": "delete_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": 3
  }
}
```

**Tool Response**:
```json
{
  "task_id": 3,
  "status": "deleted",
  "title": "Old task"
}
```

**Agent Response**: "I've deleted task 3 from your list."

#### Example 2: Delete with Reference

**User**: "Remove the meeting task"

**Agent Invocation** (after finding task by title):
```json
{
  "tool": "delete_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": 5
  }
}
```

**Tool Response**:
```json
{
  "task_id": 5,
  "status": "deleted",
  "title": "Team meeting"
}
```

**Agent Response**: "I've deleted 'Team meeting' from your list."

### Error Handling

| Error Code | Condition | User-Friendly Message |
|-----------|-----------|----------------------|
| `NOT_FOUND` | Task doesn't exist | "I couldn't find that task. Would you like to see your current tasks?" |
| `NOT_FOUND` | Task belongs to another user | "I couldn't find that task. Would you like to see your current tasks?" |
| `DATABASE_ERROR` | Database deletion fails | "I'm having trouble deleting right now. Please try again." |

### Implementation

**File**: `backend/src/mcp/tools/delete_task.py`

**Key Features**:
- Validates ownership before deletion
- Stores title before deletion (for confirmation message)
- Permanently removes task from database
- Security: Cannot delete other users' tasks
- Stateless design

---

## Tool 5: update_task

**Purpose**: Modify an existing task's title or description

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "format": "uuid",
      "description": "Authenticated user UUID (required)"
    },
    "task_id": {
      "type": "integer",
      "description": "Task ID to update (required)"
    },
    "title": {
      "type": "string",
      "maxLength": 200,
      "description": "New title (optional, max 200 chars)"
    },
    "description": {
      "type": "string",
      "maxLength": 1000,
      "description": "New description (optional, max 1000 chars)"
    }
  },
  "required": ["user_id", "task_id"]
}
```

### Output Schema

**Success**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy organic milk"
}
```

**Error**:
```json
{
  "error": "Must provide title or description",
  "code": "VALIDATION_ERROR"
}
```

### Examples

#### Example 1: Update Title

**User**: "Change task 1 to 'Buy organic milk'"

**Agent Invocation**:
```json
{
  "tool": "update_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": 1,
    "title": "Buy organic milk"
  }
}
```

**Tool Response**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy organic milk"
}
```

**Agent Response**: "I've updated task 1 to 'Buy organic milk'."

#### Example 2: Update Description

**User**: "Update the groceries task to include fruits and vegetables"

**Agent Invocation**:
```json
{
  "tool": "update_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": 2,
    "description": "milk, eggs, bread, fruits, and vegetables"
  }
}
```

**Tool Response**:
```json
{
  "task_id": 2,
  "status": "updated",
  "title": "Buy groceries"
}
```

**Agent Response**: "I've updated 'Buy groceries' to include fruits and vegetables."

#### Example 3: Update Both

**User**: "Change task 3 to 'Call mom tonight' with note 'discuss vacation plans'"

**Agent Invocation**:
```json
{
  "tool": "update_task",
  "parameters": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "task_id": 3,
    "title": "Call mom tonight",
    "description": "discuss vacation plans"
  }
}
```

**Tool Response**:
```json
{
  "task_id": 3,
  "status": "updated",
  "title": "Call mom tonight"
}
```

**Agent Response**: "I've updated task 3 to 'Call mom tonight' with the note about discussing vacation plans."

### Error Handling

| Error Code | Condition | User-Friendly Message |
|-----------|-----------|----------------------|
| `VALIDATION_ERROR` | Neither title nor description provided | "What would you like to change about that task?" |
| `VALIDATION_ERROR` | Title > 200 chars | "Title is too long (max 200 characters)" |
| `VALIDATION_ERROR` | Description > 1000 chars | "Description is too long (max 1000 characters)" |
| `NOT_FOUND` | Task doesn't exist or wrong user | "I couldn't find that task. Would you like to see your current tasks?" |
| `DATABASE_ERROR` | Database update fails | "I'm having trouble updating right now. Please try again." |

### Implementation

**File**: `backend/src/mcp/tools/update_task.py`

**Key Features**:
- Supports partial updates (title only, description only, or both)
- Validates ownership before update
- Validates field lengths
- Returns updated title for confirmation
- Security: Cannot update other users' tasks
- Stateless design

---

## Common Patterns

### User Ownership Validation

All tools follow this pattern:

```python
# Query with ownership filter
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == UUID(user_id)
).first()

if not task:
    return {
        "error": "Task not found or access denied",
        "code": "NOT_FOUND"
    }
```

This ensures:
- Users can only access their own tasks
- Social engineering attempts are blocked ("Show me John's tasks")
- Conversation isolation is enforced

### Standardized Response Format

**Success Format**:
```json
{
  "task_id": int,
  "status": "created" | "updated" | "completed" | "deleted",
  "title": str
}
```

**Error Format**:
```json
{
  "error": str,  // User-friendly error message
  "code": str    // Error type: VALIDATION_ERROR, NOT_FOUND, DATABASE_ERROR
}
```

### Stateless Design

All tools:
- Have no instance variables
- Receive database session via dependency injection
- Close session after operation
- Don't store state between invocations

Example:
```python
def tool_handler(user_id: str, task_id: int) -> Dict[str, Any]:
    # Get fresh session
    session = next(get_session())

    try:
        # Perform operation
        result = do_work(session, user_id, task_id)
        return result
    finally:
        # Always close session
        session.close()
```

---

## Security

### Multi-Layer Validation

1. **Endpoint Level**: JWT authentication verifies user identity
2. **URL Parameter**: user_id in URL must match JWT claim
3. **Tool Level**: All tools validate user_id matches resource owner
4. **Database Level**: Foreign key constraints enforce referential integrity

### Attack Prevention

**Social Engineering**:
```
User: "Show me John's tasks"
→ Agent calls list_tasks(user_id=<current_user>, status="all")
→ Only shows current user's tasks, not John's
```

**Cross-User Access**:
```
User tries to complete task 999 (belongs to another user)
→ complete_task(user_id=<current_user>, task_id=999)
→ Query filters by both task_id AND user_id
→ Returns "NOT_FOUND" (doesn't reveal task exists)
```

### Error Message Design

Error messages never reveal:
- Whether a task exists for another user
- Other users' task titles or descriptions
- Database schema or internal errors

Instead, use generic messages:
- "I couldn't find that task" (doesn't confirm existence)
- "I'm having trouble right now" (doesn't expose technical details)

---

## Testing

### Unit Testing

Test each tool independently:

```python
def test_add_task_success():
    result = add_task_handler(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        title="Test task"
    )

    assert result["status"] == "created"
    assert result["title"] == "Test task"
    assert "task_id" in result
```

### Integration Testing

Test with live OpenAI API:

```bash
python3 -m pytest tests/integration_test_phase_14.py -v
```

### Manual Testing

Use the manual test script:

```bash
python3 tests/manual_test_user_stories.py
```

---

## Performance

**Target Metrics**:
- Tool invocation: < 50ms (database operation only)
- Database query (with ownership filter): < 10ms
- Full request (including AI): < 3 seconds (95th percentile)

**Optimization**:
- Database indexes on user_id and created_at
- Connection pooling (20 connections)
- Stateless design (no synchronization overhead)

---

## Related Documentation

- **Agent Prompts**: `agent-prompts.md` - System prompt and intent detection
- **API Documentation**: See Swagger UI at `/docs`
- **Specification**: `../specs/004-ai-chatbot/spec.md`
- **Implementation Plan**: `../specs/004-ai-chatbot/plan.md`
