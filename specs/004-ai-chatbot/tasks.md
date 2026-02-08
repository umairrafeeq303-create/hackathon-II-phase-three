---
description: "Implementation tasks for Todo AI Chatbot with natural language task management"
---

# Tasks: Todo AI Chatbot - Natural Language Task Management

**Input**: Design documents from `/specs/004-ai-chatbot/`
**Prerequisites**: plan.md (✅), spec.md (✅), research.md (✅), data-model.md (✅), contracts/ (✅)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- All paths are relative to repository root

---

## Phase 1: Setup and Dependencies (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

**⚠️ CRITICAL**: Must complete before ANY implementation

- [ ] T001 Update backend/requirements.txt with openai>=1.0.0, mcp>=1.0.0, tenacity>=8.2.0
- [ ] T002 Install backend dependencies with pip install -r backend/requirements.txt
- [ ] T003 [P] Update frontend/package.json with @openai/chatkit dependency
- [ ] T004 [P] Install frontend dependencies with npm install in frontend/
- [ ] T005 [P] Add OPENAI_API_KEY to backend/.env.example with placeholder sk-...
- [ ] T006 [P] Add OPENAI_API_KEY to backend/.env with actual API key from OpenAI platform
- [ ] T007 [P] Verify DATABASE_URL is configured in backend/.env from Phase II
- [ ] T008 [P] Verify BETTER_AUTH_SECRET is configured in backend/.env from Phase II
- [ ] T009 [P] Update README.md with Phase III setup instructions referencing specs/004-ai-chatbot/quickstart.md

**Checkpoint**: Setup complete - foundational phase can now begin

---

## Phase 2: Database Models and Migrations (Blocking Prerequisites)

**Purpose**: Core database infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [ ] T010 [P] Create backend/src/models/conversation.py with Conversation SQLModel class
- [ ] T011 [P] Define Conversation fields: id (UUID, primary key), user_id (UUID, foreign key to users.id), created_at (TIMESTAMP), updated_at (TIMESTAMP)
- [ ] T012 [P] Add Conversation relationships: user (back_populates "conversations"), messages (back_populates "conversation", cascade_delete=True)
- [ ] T013 [P] Create backend/src/models/message.py with Message SQLModel class
- [ ] T014 [P] Define Message fields: id (UUID, primary key), conversation_id (UUID, foreign key to conversations.id), role (Literal["user", "assistant"]), content (str, max 10000), created_at (TIMESTAMP)
- [ ] T015 [P] Add Message relationship: conversation (back_populates "messages")
- [ ] T016 Update backend/src/models/__init__.py to export Conversation and Message models

### Database Migration

- [ ] T017 Generate Alembic migration with alembic revision --autogenerate -m "Add conversation and message tables"
- [ ] T018 Review generated migration file in backend/alembic/versions/ for correctness
- [ ] T019 Add index idx_conversations_user_id on conversations(user_id) in migration if not auto-generated
- [ ] T020 Add index idx_messages_conversation_id on messages(conversation_id) in migration if not auto-generated
- [ ] T021 Add index idx_messages_created_at on messages(created_at) in migration if not auto-generated
- [ ] T022 Add CHECK constraint on messages.role to enforce 'user' or 'assistant' values
- [ ] T023 Apply migration with alembic upgrade head
- [ ] T024 Verify conversations table created with psql $DATABASE_URL -c "\\d conversations"
- [ ] T025 Verify messages table created with psql $DATABASE_URL -c "\\d messages"

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: MCP Server and Tools (Core - Blocking)

**Purpose**: Implement stateless MCP server with 5 task operation tools

**⚠️ CRITICAL**: MCP tools must be complete before agent integration (Phase 4)

### MCP Server Infrastructure

- [ ] T026 Create backend/src/mcp/__init__.py for MCP module initialization
- [ ] T027 Create backend/src/mcp/server.py with MCP server initialization using Official MCP SDK
- [ ] T028 Configure MCP server with tool registry and stateless handler pattern
- [ ] T029 Create backend/src/mcp/tools/__init__.py for tool exports
- [ ] T030 Define standardized tool response format helper functions: success_response(task_id, status, title) and error_response(error, code)

### add_task MCP Tool (US1 - Create Tasks)

- [ ] T031 [P] [US1] Create backend/src/mcp/tools/add_task.py with tool definition and handler function
- [ ] T032 [P] [US1] Define tool schema: input parameters (user_id: UUID required, title: str required max 200, description: str optional max 1000)
- [ ] T033 [P] [US1] Define tool schema: output format {task_id: int, status: "created", title: str} or {error: str, code: str}
- [ ] T034 [P] [US1] Implement stateless handler function accepting user_id, title, description parameters
- [ ] T035 [P] [US1] Get database session from dependency injection (no persistent connection)
- [ ] T036 [P] [US1] Validate title not empty and length ≤ 200 chars, return error {"error": "Title required (max 200 chars)", "code": "VALIDATION_ERROR"} if invalid
- [ ] T037 [P] [US1] Validate description length ≤ 1000 chars if provided, return error {"error": "Description too long (max 1000 chars)", "code": "VALIDATION_ERROR"} if invalid
- [ ] T038 [P] [US1] Create Task instance with user_id=user_id, title=title, description=description, completed=False
- [ ] T039 [P] [US1] Save task to database using session.add() and session.commit()
- [ ] T040 [P] [US1] Return success response {"task_id": task.id, "status": "created", "title": task.title}
- [ ] T041 [P] [US1] Add database error handling: catch exceptions and return {"error": "Database error", "code": "DATABASE_ERROR"}
- [ ] T042 [P] [US1] Register add_task tool in MCP server registry in backend/src/mcp/server.py

### list_tasks MCP Tool (US2 - View Tasks)

- [ ] T043 [P] [US2] Create backend/src/mcp/tools/list_tasks.py with tool definition and handler function
- [ ] T044 [P] [US2] Define tool schema: input parameters (user_id: UUID required, status: Literal["all", "pending", "completed"] default "all")
- [ ] T045 [P] [US2] Define tool schema: output format {tasks: List[{id: int, title: str, description: str|null, completed: bool, created_at: str}]}
- [ ] T046 [P] [US2] Implement stateless handler function accepting user_id, status parameters
- [ ] T047 [P] [US2] Get database session from dependency injection
- [ ] T048 [P] [US2] Query tasks filtered by user_id from database: session.query(Task).filter(Task.user_id == user_id)
- [ ] T049 [P] [US2] Apply status filter: if status=="pending" add .filter(Task.completed == False), if status=="completed" add .filter(Task.completed == True)
- [ ] T050 [P] [US2] Order results by created_at DESC for consistent ordering
- [ ] T051 [P] [US2] Convert tasks to dict format with id, title, description, completed, created_at (ISO 8601 string)
- [ ] T052 [P] [US2] Return success response {"tasks": [task_dicts]}
- [ ] T053 [P] [US2] Add error handling for database errors and return {"error": "Database error", "code": "DATABASE_ERROR"}
- [ ] T054 [P] [US2] Register list_tasks tool in MCP server registry in backend/src/mcp/server.py

### complete_task MCP Tool (US3 - Complete Tasks)

- [ ] T055 [P] [US3] Create backend/src/mcp/tools/complete_task.py with tool definition and handler function
- [ ] T056 [P] [US3] Define tool schema: input parameters (user_id: UUID required, task_id: int required)
- [ ] T057 [P] [US3] Define tool schema: output format {task_id: int, status: "completed", title: str} or {error: str, code: str}
- [ ] T058 [P] [US3] Implement stateless handler function accepting user_id, task_id parameters
- [ ] T059 [P] [US3] Get database session from dependency injection
- [ ] T060 [P] [US3] Query task with ownership validation: session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
- [ ] T061 [P] [US3] If task not found, return {"error": "Task not found or access denied", "code": "NOT_FOUND"}
- [ ] T062 [P] [US3] Update task: set task.completed = True
- [ ] T063 [P] [US3] Save changes with session.commit()
- [ ] T064 [P] [US3] Return success response {"task_id": task.id, "status": "completed", "title": task.title}
- [ ] T065 [P] [US3] Add error handling for database errors and return {"error": "Database error", "code": "DATABASE_ERROR"}
- [ ] T066 [P] [US3] Register complete_task tool in MCP server registry in backend/src/mcp/server.py

### delete_task MCP Tool (US4 - Delete Tasks)

- [ ] T067 [P] [US4] Create backend/src/mcp/tools/delete_task.py with tool definition and handler function
- [ ] T068 [P] [US4] Define tool schema: input parameters (user_id: UUID required, task_id: int required)
- [ ] T069 [P] [US4] Define tool schema: output format {task_id: int, status: "deleted", title: str} or {error: str, code: str}
- [ ] T070 [P] [US4] Implement stateless handler function accepting user_id, task_id parameters
- [ ] T071 [P] [US4] Get database session from dependency injection
- [ ] T072 [P] [US4] Query task with ownership validation: session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
- [ ] T073 [P] [US4] If task not found, return {"error": "Task not found or access denied", "code": "NOT_FOUND"}
- [ ] T074 [P] [US4] Store task title before deletion for response
- [ ] T075 [P] [US4] Delete task with session.delete(task) and session.commit()
- [ ] T076 [P] [US4] Return success response {"task_id": task_id, "status": "deleted", "title": stored_title}
- [ ] T077 [P] [US4] Add error handling for database errors and return {"error": "Database error", "code": "DATABASE_ERROR"}
- [ ] T078 [P] [US4] Register delete_task tool in MCP server registry in backend/src/mcp/server.py

### update_task MCP Tool (US5 - Update Tasks)

- [ ] T079 [P] [US5] Create backend/src/mcp/tools/update_task.py with tool definition and handler function
- [ ] T080 [P] [US5] Define tool schema: input parameters (user_id: UUID required, task_id: int required, title: str optional max 200, description: str optional max 1000)
- [ ] T081 [P] [US5] Define tool schema: output format {task_id: int, status: "updated", title: str} or {error: str, code: str}
- [ ] T082 [P] [US5] Implement stateless handler function accepting user_id, task_id, title, description parameters
- [ ] T083 [P] [US5] Validate at least one of title or description is provided, return {"error": "Must provide title or description", "code": "VALIDATION_ERROR"} if both None
- [ ] T084 [P] [US5] Validate title length ≤ 200 chars if provided, return error if invalid
- [ ] T085 [P] [US5] Validate description length ≤ 1000 chars if provided, return error if invalid
- [ ] T086 [P] [US5] Get database session from dependency injection
- [ ] T087 [P] [US5] Query task with ownership validation: session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
- [ ] T088 [P] [US5] If task not found, return {"error": "Task not found or access denied", "code": "NOT_FOUND"}
- [ ] T089 [P] [US5] Update task fields: if title provided set task.title = title, if description provided set task.description = description
- [ ] T090 [P] [US5] Save changes with session.commit()
- [ ] T091 [P] [US5] Return success response {"task_id": task.id, "status": "updated", "title": task.title}
- [ ] T092 [P] [US5] Add error handling for database errors and return {"error": "Database error", "code": "DATABASE_ERROR"}
- [ ] T093 [P] [US5] Register update_task tool in MCP server registry in backend/src/mcp/server.py

**Checkpoint**: MCP tools complete - agent integration can now begin

---

## Phase 4: OpenAI Agent Integration (Core - Blocking)

**Purpose**: Implement AI agent with conversation history loading and tool integration

**⚠️ CRITICAL**: Agent must be complete before Chat API endpoint (Phase 5)

### Agent Configuration

- [ ] T094 Create backend/src/ai/__init__.py for AI module initialization
- [ ] T095 Create backend/src/ai/prompts.py with system prompt constant
- [ ] T096 Define system prompt with personality: friendly, helpful todo assistant
- [ ] T097 Add system prompt rules: detect user intent, select appropriate tool, ask clarification when ambiguous
- [ ] T098 Add system prompt constraints: only access user's own data, provide conversational responses (no technical jargon), maintain context across turns
- [ ] T099 Add system prompt tool descriptions: add_task (create new tasks), list_tasks (show tasks), complete_task (mark done), delete_task (remove), update_task (modify)

### Agent Core Implementation

- [ ] T100 Create backend/src/ai/agent.py with Agent class
- [ ] T101 Initialize OpenAI client in Agent.__init__ with api_key from environment variable OPENAI_API_KEY
- [ ] T102 Configure agent to use gpt-3.5-turbo model (from research.md decision TD-004)
- [ ] T103 Import and register all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) in agent
- [ ] T104 Implement tool registration method that maps MCP tool names to handler functions
- [ ] T105 Add configuration for tool call transparency (include tool calls in response per FR-008)

### Conversation History Management

- [ ] T106 Create backend/src/ai/runner.py with ConversationRunner class
- [ ] T107 Implement load_conversation_history(conversation_id: UUID, session) function
- [ ] T108 Query messages: session.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.desc()).limit(50).all()
- [ ] T109 Reverse message list to get chronological order (oldest first) for agent context
- [ ] T110 Convert messages to OpenAI format: [{"role": msg.role, "content": msg.content} for msg in messages]
- [ ] T111 Return formatted message history list for agent execution

### Agent Execution

- [ ] T112 Implement run_agent(user_message: str, conversation_history: List[dict], user_id: UUID) function in backend/src/ai/runner.py
- [ ] T113 Append user message to conversation history: conversation_history.append({"role": "user", "content": user_message})
- [ ] T114 Execute agent with OpenAI Agents SDK: agent.run(messages=conversation_history, tools=registered_tools)
- [ ] T115 Capture agent response and tool calls from execution result
- [ ] T116 Extract assistant message content from agent response
- [ ] T117 Extract tool_calls list from agent response (tool name, parameters, result) for transparency
- [ ] T118 Return tuple: (assistant_message: str, tool_calls: List[dict])

### Error Handling and Retry Logic

- [ ] T119 Implement exponential backoff retry logic for OpenAI API rate limits (1s, 2s, 4s delays, max 3 retries) using tenacity library
- [ ] T120 Add retry decorator to agent execution: @retry(wait=wait_exponential(multiplier=1, min=1, max=4), stop=stop_after_attempt(3), retry=retry_if_exception_type(RateLimitError))
- [ ] T121 Handle OpenAI API connection errors: catch APIConnectionError and return friendly message "I'm having trouble connecting right now. Please try again in a moment."
- [ ] T122 Handle OpenAI API timeout errors: catch Timeout and retry once with extended timeout
- [ ] T123 Handle authentication errors: catch AuthenticationError and return "API key configuration error. Please contact support."
- [ ] T124 Add logging for all OpenAI API calls with request/response metadata for debugging

**Checkpoint**: Agent integration complete - Chat API endpoint can now be implemented

---

## Phase 5: Chat API Endpoint (Core - Blocking)

**Purpose**: Implement stateless chat endpoint with conversation management

**⚠️ CRITICAL**: Chat API must be complete before frontend integration (Phase 6)

### Pydantic Schemas

- [ ] T125 [P] Create backend/src/schemas/chat.py with Pydantic schemas
- [ ] T126 [P] Define ToolCall schema: tool (str), parameters (Dict[str, Any]), result (Dict[str, Any])
- [ ] T127 [P] Define ChatRequest schema: message (str, min_length=1, max_length=10000), conversation_id (Optional[UUID])
- [ ] T128 [P] Define ChatResponse schema: conversation_id (UUID), response (str), tool_calls (List[ToolCall], default=[])
- [ ] T129 [P] Add Pydantic examples to all schemas for API documentation

### Chat Router

- [ ] T130 Create backend/src/api/chat.py with FastAPI router
- [ ] T131 Define POST /api/{user_id}/chat endpoint with path parameter user_id: UUID
- [ ] T132 Add JWT authentication dependency: current_user_id = Depends(get_current_user_id) from Phase II
- [ ] T133 Validate path user_id matches JWT user_id, raise HTTPException(403, "Forbidden - user_id mismatch") if not
- [ ] T134 Add request body parameter: chat_request: ChatRequest
- [ ] T135 Add database session dependency: session = Depends(get_session) from Phase II

### Stateless Request Cycle Implementation

- [ ] T136 Implement conversation loading: if chat_request.conversation_id provided, query Conversation with user_id validation
- [ ] T137 If conversation_id provided but not found or owned by different user, raise HTTPException(404, "Conversation not found")
- [ ] T138 Implement conversation creation: if conversation_id is None, create new Conversation(user_id=user_id), add to session, commit
- [ ] T139 Store user message: create Message(conversation_id=conversation.id, role="user", content=chat_request.message), add to session, commit
- [ ] T140 Load conversation history using load_conversation_history(conversation.id, session) from backend/src/ai/runner.py
- [ ] T141 Execute agent: call run_agent(chat_request.message, conversation_history, user_id) from backend/src/ai/runner.py
- [ ] T142 Capture agent response: (assistant_message, tool_calls) = run_agent(...)
- [ ] T143 Store assistant message: create Message(conversation_id=conversation.id, role="assistant", content=assistant_message), add to session, commit
- [ ] T144 Update conversation timestamp: set conversation.updated_at = datetime.utcnow(), commit
- [ ] T145 Return ChatResponse(conversation_id=conversation.id, response=assistant_message, tool_calls=tool_calls)

### Error Handling

- [ ] T146 Add try-except for database errors: catch SQLAlchemyError and return HTTPException(500, "I'm having trouble saving your message. Please try again.")
- [ ] T147 Add try-except for OpenAI API errors: catch OpenAIError and return HTTPException(500, agent error message from error handling)
- [ ] T148 Add validation for message length: if len(message) > 10000, raise HTTPException(400, "Message too long (max 10,000 characters)")
- [ ] T149 Add CORS configuration to allow frontend origin in backend/src/main.py if not already configured from Phase II
- [ ] T150 Register chat router in backend/src/main.py: app.include_router(chat_router)

**Checkpoint**: Chat API complete - frontend integration can now begin

---

## Phase 6: User Story 1 - Create Tasks via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks through conversational interface

**Independent Test**: Send "Add a task to buy groceries" and verify task created in database

### Frontend Chat Components

- [ ] T151 [P] [US1] Create frontend/src/lib/api-chat.ts with sendChatMessage function
- [ ] T152 [P] [US1] Implement sendChatMessage(userId: string, message: string, conversationId?: string): Promise<ChatResponse>
- [ ] T153 [P] [US1] Configure API request: POST ${NEXT_PUBLIC_API_URL}/api/${userId}/chat with Authorization: Bearer ${token}
- [ ] T154 [P] [US1] Handle response parsing and error cases (400, 401, 403, 404, 500)
- [ ] T155 [P] [US1] Create frontend/src/hooks/useChat.ts custom React hook
- [ ] T156 [P] [US1] Implement useChat state: messages (array), isLoading (bool), error (string | null), conversationId (string | null)
- [ ] T157 [P] [US1] Implement sendMessage function in useChat that calls sendChatMessage and updates state
- [ ] T158 [P] [US1] Add optimistic UI update: append user message immediately before API call
- [ ] T159 [P] [US1] Handle API response: append assistant message to messages array, update conversationId
- [ ] T160 [P] [US1] Handle errors: set error state with user-friendly message

### Chat UI Components

- [ ] T161 [P] [US1] Create frontend/src/components/chat/MessageList.tsx component
- [ ] T162 [P] [US1] Display messages array in chronological order with user/assistant styling differentiation
- [ ] T163 [P] [US1] Style user messages aligned right with blue background
- [ ] T164 [P] [US1] Style assistant messages aligned left with gray background
- [ ] T165 [P] [US1] Add auto-scroll to bottom when new messages arrive
- [ ] T166 [P] [US1] Create frontend/src/components/chat/ChatInput.tsx component
- [ ] T167 [P] [US1] Implement textarea input with placeholder "Type your message..."
- [ ] T168 [P] [US1] Add send button with disabled state when loading or input empty
- [ ] T169 [P] [US1] Handle Enter key to send message (Shift+Enter for new line)
- [ ] T170 [P] [US1] Clear input after sending message

### Chat Page

- [ ] T171 [US1] Create frontend/src/app/chat/page.tsx with chat interface
- [ ] T172 [US1] Import and use useChat hook for state management
- [ ] T173 [US1] Add authentication check: redirect to login if not authenticated (reuse Phase II auth)
- [ ] T174 [US1] Get authenticated user ID from auth context
- [ ] T175 [US1] Render MessageList component with messages from useChat
- [ ] T176 [US1] Render ChatInput component with sendMessage handler from useChat
- [ ] T177 [US1] Add loading indicator when isLoading is true
- [ ] T178 [US1] Add error display when error is not null with dismiss button
- [ ] T179 [US1] Add conversation persistence: store conversationId in URL query parameter
- [ ] T180 [US1] Load conversationId from URL on mount if present

### Navigation Integration

- [ ] T181 [US1] Add /chat navigation link to frontend navigation component (existing from Phase II)
- [ ] T182 [US1] Style /chat link consistently with existing navigation
- [ ] T183 [US1] Add chat icon or label "AI Assistant" to navigation

**Checkpoint**: User Story 1 complete and independently testable - basic task creation via chat works end-to-end

---

## Phase 7: User Story 2 - View Tasks via Natural Language (Priority: P1)

**Goal**: Users can view their tasks through conversational queries

**Independent Test**: Create test tasks, send "Show me my tasks", verify AI lists all tasks

### Agent Enhancement for Viewing

- [ ] T184 [US2] Verify agent system prompt includes list_tasks tool description (already in T099)
- [ ] T185 [US2] Test agent intent detection: "Show me my tasks" should trigger list_tasks tool
- [ ] T186 [US2] Test agent intent detection: "What's pending?" should trigger list_tasks with status="pending"
- [ ] T187 [US2] Test agent intent detection: "What have I completed?" should trigger list_tasks with status="completed"
- [ ] T188 [US2] Enhance agent response formatting: format task list as numbered list "You have 3 tasks: 1. Task A, 2. Task B, 3. Task C"
- [ ] T189 [US2] Add empty list handling: when tasks array is empty, respond "Your task list is empty. Would you like to add something?"

**Checkpoint**: User Story 2 complete - task viewing via natural language works end-to-end

---

## Phase 8: User Story 3 - Complete Tasks via Natural Language (Priority: P1)

**Goal**: Users can mark tasks complete through conversation

**Independent Test**: Create task, send "Mark task 1 as complete", verify task.completed = true

### Agent Enhancement for Completion

- [ ] T190 [US3] Verify agent system prompt includes complete_task tool description (already in T099)
- [ ] T191 [US3] Test agent intent detection: "Mark task 3 as complete" should extract task_id=3 and trigger complete_task
- [ ] T192 [US3] Test agent intent detection: "I finished buying groceries" should search task by title and trigger complete_task
- [ ] T193 [US3] Add disambiguation handling: when multiple tasks match, ask "I found 2 tasks matching 'groceries'. Which one? 1. Buy groceries, 2. Put away groceries"
- [ ] T194 [US3] Enhance agent response: "Great job! I've marked 'Task Title' as complete." with encouraging tone
- [ ] T195 [US3] Handle task not found: "I couldn't find task 999. Would you like to see your current tasks?"

**Checkpoint**: User Story 3 complete - core workflow (create, view, complete) works end-to-end - MVP READY

---

## Phase 9: User Story 6 - Maintain Conversation Context (Priority: P1)

**Goal**: AI understands references to previous messages using database-backed history

**Independent Test**: Send "Add a task to buy milk" then "Mark that task as complete", verify AI identifies "that task" correctly

### Context Management Implementation

- [ ] T196 [US6] Verify conversation history loading retrieves last 50 messages (already in T108)
- [ ] T197 [US6] Test context preservation: create task in message 1, reference "that task" in message 2, verify agent resolves reference
- [ ] T198 [US6] Test context preservation: list tasks in message 1, reference "the first one" in message 2, verify agent identifies correct task
- [ ] T199 [US6] Test multi-turn context: verify agent maintains context across 5+ message exchanges
- [ ] T200 [US6] Test pronoun resolution: "Delete it" should resolve "it" to last mentioned task from conversation history

**Checkpoint**: User Story 6 complete - conversational context works naturally

---

## Phase 10: User Story 4 - Delete Tasks via Natural Language (Priority: P2)

**Goal**: Users can remove tasks through conversation

**Independent Test**: Create task, send "Delete task 1", verify task removed from database

### Agent Enhancement for Deletion

- [ ] T201 [US4] Verify agent system prompt includes delete_task tool description (already in T099)
- [ ] T202 [US4] Test agent intent detection: "Delete task 2" should extract task_id=2 and trigger delete_task
- [ ] T203 [US4] Test agent intent detection: "Remove the meeting task" should search by title and trigger delete_task
- [ ] T204 [US4] Add bulk deletion confirmation: "Delete all my tasks" should ask "Are you sure? You have 5 tasks. Reply 'yes' to confirm."
- [ ] T205 [US4] Implement confirmation handling: track pending confirmation in conversation context, execute on "yes" response
- [ ] T206 [US4] Enhance agent response: "I've deleted task 2 from your list." with simple confirmation

**Checkpoint**: User Story 4 complete - task deletion works via natural language

---

## Phase 11: User Story 5 - Update Tasks via Natural Language (Priority: P2)

**Goal**: Users can modify existing tasks through conversation

**Independent Test**: Create task, send "Change task 1 to 'New title'", verify task.title updated

### Agent Enhancement for Updates

- [ ] T207 [US5] Verify agent system prompt includes update_task tool description (already in T099)
- [ ] T208 [US5] Test agent intent detection: "Change task 1 to 'Call mom tonight'" should extract task_id=1, title='Call mom tonight', trigger update_task
- [ ] T209 [US5] Test agent intent detection: "Update the groceries task to include fruits" should search by title and update description
- [ ] T210 [US5] Add missing information prompt: "Rename the first task" should ask "What would you like to rename it to?"
- [ ] T211 [US5] Handle partial updates: support updating only title OR only description, not requiring both
- [ ] T212 [US5] Enhance agent response: "I've updated task 1 to 'New Title'." with clear confirmation

**Checkpoint**: User Story 5 complete - all CRUD operations work via natural language

---

## Phase 12: User Story 7 - Handle Errors Gracefully (Priority: P2)

**Goal**: Provide friendly error messages and recovery suggestions

**Independent Test**: Simulate database failure, verify AI responds with helpful message instead of error code

### Error Message Enhancement

- [ ] T213 [US7] Test database connection failure scenario: verify agent responds "I'm having trouble saving your task right now. Please try again in a moment."
- [ ] T214 [US7] Test OpenAI API rate limit scenario: verify retry logic triggers and user sees "I'm thinking... (this is taking a bit longer)"
- [ ] T215 [US7] Test ambiguous request: "Do that thing" should trigger "I'm not sure what you'd like me to do. Could you be more specific?"
- [ ] T216 [US7] Test invalid task ID: "Mark task 999 as complete" should respond "I couldn't find task 999. Would you like to see your current tasks?"
- [ ] T217 [US7] Add agent prompt enhancement: include error recovery suggestions in system prompt
- [ ] T218 [US7] Test edge case: message exceeding 10,000 characters should return clear validation error

**Checkpoint**: User Story 7 complete - error handling is user-friendly

---

## Phase 13: User Story 8 - Resume Conversations After Server Restart (Priority: P3)

**Goal**: Validate stateless architecture - conversations survive server restarts

**Independent Test**: Start conversation, restart backend server, send another message, verify context maintained

### Stateless Architecture Validation

- [ ] T219 [US8] Verify server stores NO conversation state in memory (architectural review of all code)
- [ ] T220 [US8] Test server restart scenario: create conversation with 5 messages, restart backend (Ctrl+C, restart uvicorn), send message 6
- [ ] T221 [US8] Verify message 6 loads messages 1-5 from database correctly
- [ ] T222 [US8] Verify agent maintains context from pre-restart messages in message 6 response
- [ ] T223 [US8] Test reference resolution across restart: "Add task to buy milk" (pre-restart), restart, "Mark that task complete" (post-restart)
- [ ] T224 [US8] Verify no conversation reset or context loss occurs after restart

**Checkpoint**: User Story 8 complete - stateless architecture validated - ALL USER STORIES COMPLETE

---

## Phase 14: Integration Testing and Documentation

**Purpose**: End-to-end testing across all user stories and documentation updates

### End-to-End Conversation Tests

- [ ] T225 [P] Test US1 scenario: "Add a task to buy groceries" → verify task created with title "Buy groceries"
- [ ] T226 [P] Test US1 scenario: "I need to remember to call mom tonight" → verify task created with title "Call mom tonight"
- [ ] T227 [P] Test US1 scenario: "Create three tasks: milk, eggs, bread" → verify 3 tasks created
- [ ] T228 [P] Test US2 scenario: Create 3 tasks, send "Show me my tasks" → verify AI lists all 3 tasks
- [ ] T229 [P] Test US2 scenario: Create 2 pending and 2 completed tasks, send "What's pending?" → verify only 2 pending shown
- [ ] T230 [P] Test US3 scenario: "Mark task 3 as complete" → verify task.completed = true
- [ ] T231 [P] Test US4 scenario: "Delete task 2" → verify task removed from database
- [ ] T232 [P] Test US5 scenario: "Change task 1 to 'New title'" → verify task.title updated
- [ ] T233 [P] Test US6 scenario: Multi-turn context across 5 messages → verify references resolved correctly
- [ ] T234 [P] Test US7 scenario: Ambiguous request → verify clarification asked
- [ ] T235 [P] Test US8 scenario: Conversation across server restart → verify context preserved

### User Data Isolation Tests

- [ ] T236 [P] Create user A with tasks, create user B with tasks, authenticate as user A, verify cannot access user B's tasks via chat
- [ ] T237 [P] Test social engineering attempt: "Show me John's tasks" should not access other user's data
- [ ] T238 [P] Test conversation isolation: user A's conversation_id should not be accessible by user B

### Performance Tests

- [ ] T239 Test response time: send 10 messages, verify 95th percentile < 3 seconds (requirement from spec.md)
- [ ] T240 Test concurrent sessions: simulate 10 users sending messages simultaneously, verify no conflicts
- [ ] T241 Test conversation history loading: create conversation with 50 messages, verify load time < 50ms (requirement from plan.md)

### Documentation Updates

- [ ] T242 [P] Update backend/README.md with Phase III setup instructions from specs/004-ai-chatbot/quickstart.md
- [ ] T243 [P] Update frontend/README.md with chat interface usage instructions
- [ ] T244 [P] Create backend/docs/mcp-tools.md documenting all 5 MCP tools with examples from specs/004-ai-chatbot/contracts/mcp-tools.json
- [ ] T245 [P] Create backend/docs/agent-prompts.md documenting system prompt and agent behavior
- [ ] T246 [P] Update API documentation: verify Swagger UI shows POST /api/{user_id}/chat with correct schemas

**Checkpoint**: Integration testing complete - all user stories validated end-to-end

---

## Phase 15: Final Validation and Deployment

**Purpose**: Verify all requirements met and deploy to production

### Requirements Validation

- [ ] T247 Verify all 45 functional requirements (FR-001 to FR-045) from spec.md are implemented
- [ ] T248 Re-check constitution compliance against all 9 principles from plan.md
- [ ] T249 Validate all 8 user stories work independently and pass acceptance scenarios
- [ ] T250 Run definition of done checklist from spec.md - verify all items pass

### Production Deployment - Backend (Railway)

- [ ] T251 [P] Add OPENAI_API_KEY to Railway environment variables
- [ ] T252 [P] Verify DATABASE_URL is configured in Railway (from Phase II)
- [ ] T253 [P] Verify BETTER_AUTH_SECRET is configured in Railway (from Phase II)
- [ ] T254 [P] Verify CORS_ORIGINS includes Vercel frontend URL in Railway
- [ ] T255 Push Phase III code to main branch: git add ., git commit -m "Add Phase III AI Chatbot", git push origin main
- [ ] T256 Verify Railway auto-deploys from main branch
- [ ] T257 Run database migration on Railway: railway run alembic upgrade head
- [ ] T258 Verify production backend health: curl https://todo-backend.railway.app/docs
- [ ] T259 Verify POST /api/{user_id}/chat endpoint appears in production Swagger UI

### Production Deployment - Frontend (Vercel)

- [ ] T260 [P] Verify NEXT_PUBLIC_API_URL points to Railway backend URL in Vercel environment variables
- [ ] T261 [P] Verify BETTER_AUTH_SECRET matches backend value in Vercel (from Phase II)
- [ ] T262 Push Phase III frontend code to main branch (already done in T255 if monorepo)
- [ ] T263 Verify Vercel auto-deploys from main branch
- [ ] T264 Verify production frontend loads: visit https://your-app.vercel.app/chat
- [ ] T265 Test authentication flow: verify login works and redirects to chat interface

### Production End-to-End Testing

- [ ] T266 Test production US1: Send "Add a task to buy groceries" on production chat interface
- [ ] T267 Verify production task created: check tasks visible in production task list view (Phase II UI)
- [ ] T268 Test production US2: Send "Show me my tasks" and verify response includes task from T266
- [ ] T269 Test production US3: Send "Mark task 1 as complete" and verify task marked complete
- [ ] T270 Test production conversation persistence: refresh page, verify conversation_id preserved in URL
- [ ] T271 Test production authentication: logout, verify /chat redirects to login
- [ ] T272 Test production error handling: send invalid request, verify friendly error message

**Checkpoint**: ALL PHASES COMPLETE - Feature ready for production use

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately - BLOCKS all implementation
- **Phase 2 (Database)**: Depends on Phase 1 - BLOCKS all user stories and agent work
- **Phase 3 (MCP Tools)**: Depends on Phase 2 - BLOCKS Phase 4, 5
- **Phase 4 (Agent)**: Depends on Phase 2, 3 - BLOCKS Phase 5
- **Phase 5 (Chat API)**: Depends on Phase 2, 3, 4 - BLOCKS Phase 6+
- **Phases 6-13 (User Stories)**: All depend on Phases 1-5 completing
  - User stories CAN be implemented in parallel if team capacity allows
  - OR sequentially in priority order: US1 (P1) → US2 (P1) → US3 (P1) → US6 (P1) → US4 (P2) → US5 (P2) → US7 (P2) → US8 (P3)
- **Phase 14 (Testing)**: Depends on desired user stories being complete
- **Phase 15 (Deployment)**: Depends on all phases complete

### Critical Path (Sequential Dependencies)

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 (US1 MVP)
```

Minimum viable product (MVP) ready after Phase 6 completion - enables task creation via chat.

### User Story Independence

Once Phases 1-5 are complete, user stories can proceed independently:

- **US1 (Phase 6)**: No dependencies on other stories - MVP candidate
- **US2 (Phase 7)**: No dependencies on other stories
- **US3 (Phase 8)**: No dependencies on other stories
- **US6 (Phase 9)**: No dependencies on other stories
- **US4 (Phase 10)**: No dependencies on other stories
- **US5 (Phase 11)**: No dependencies on other stories
- **US7 (Phase 12)**: No dependencies on other stories
- **US8 (Phase 13)**: No dependencies on other stories

All user stories are independently testable once foundation is ready.

### Parallel Opportunities

**Within Phase 1 (Setup)**: Tasks T001-T009 all marked [P] can run in parallel

**Within Phase 2 (Database)**: Tasks T010-T016 all marked [P] can run in parallel

**Within Phase 3 (MCP Tools)**:
- Infrastructure tasks T026-T030 sequential
- All 5 tool implementations can run in parallel:
  - add_task (T031-T042) [P]
  - list_tasks (T043-T054) [P]
  - complete_task (T055-T066) [P]
  - delete_task (T067-T078) [P]
  - update_task (T079-T093) [P]

**Within Phase 6 (US1 Frontend)**:
- T151-T160 (API client and hook) [P]
- T161-T170 (UI components) [P]

**Across User Story Phases**:
- Once Phase 5 complete, Phases 6-13 can ALL run in parallel if team has capacity
- Different developers can work on different user stories simultaneously

**Within Phase 14 (Testing)**: Tasks T225-T238 all marked [P] can run in parallel

**Within Phase 15 (Deployment)**: Tasks T251-T254 and T260-T261 marked [P] can run in parallel

### Parallel Example: Phase 3 (MCP Tools)

```bash
# After completing T026-T030 (infrastructure), launch all 5 tools together:
Task T031-T042: Implement add_task tool in backend/src/mcp/tools/add_task.py
Task T043-T054: Implement list_tasks tool in backend/src/mcp/tools/list_tasks.py
Task T055-T066: Implement complete_task tool in backend/src/mcp/tools/complete_task.py
Task T067-T078: Implement delete_task tool in backend/src/mcp/tools/delete_task.py
Task T079-T093: Implement update_task tool in backend/src/mcp/tools/update_task.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

Fastest path to working chatbot:

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Database (T010-T025)
3. Complete Phase 3: MCP Tools (T026-T093) - focus on add_task first for MVP
4. Complete Phase 4: Agent (T094-T124)
5. Complete Phase 5: Chat API (T125-T150)
6. Complete Phase 6: User Story 1 (T151-T183)
7. **STOP and VALIDATE**: Test task creation via chat works end-to-end
8. Deploy to production and demo

**MVP Scope**: Users can chat with AI to create tasks. This validates the entire technical stack and provides immediate value.

### Incremental Delivery (Recommended)

Build and deliver incrementally:

1. **Iteration 1 - Foundation**: Phases 1-5 (T001-T150) → Infrastructure ready
2. **Iteration 2 - Create Tasks**: Phase 6 US1 (T151-T183) → Deploy MVP ✅
3. **Iteration 3 - View Tasks**: Phase 7 US2 (T184-T189) → Deploy update
4. **Iteration 4 - Complete Tasks**: Phase 8 US3 (T190-T195) → Deploy core workflow ✅
5. **Iteration 5 - Context**: Phase 9 US6 (T196-T200) → Deploy enhanced UX
6. **Iteration 6 - Delete/Update**: Phases 10-11 US4-US5 (T201-T212) → Deploy full CRUD
7. **Iteration 7 - Polish**: Phases 12-13 US7-US8 (T213-T224) → Deploy production-ready
8. **Iteration 8 - Validate**: Phases 14-15 (T225-T272) → Full testing and production deployment

Each iteration adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers working simultaneously:

**Week 1**: Everyone on Phases 1-5 (foundation)
- Developer A: Phase 1-2 (Setup, Database)
- Developer B: Phase 3 (MCP Tools add_task, list_tasks)
- Developer C: Phase 3 (MCP Tools complete_task, delete_task, update_task)

**Week 2**: Parallel user story development (after Phase 5 complete)
- Developer A: Phase 6 (US1 - Create)
- Developer B: Phase 7-8 (US2-US3 - View, Complete)
- Developer C: Phase 9 (US6 - Context)

**Week 3**: Remaining user stories and testing
- Developer A: Phase 10-11 (US4-US5 - Delete, Update)
- Developer B: Phase 12-13 (US7-US8 - Errors, Restart)
- Developer C: Phase 14 (Testing)

**Week 4**: Final validation and deployment
- All: Phase 15 (Deployment)

---

## Summary Statistics

- **Total Tasks**: 272
- **Phases**: 15
- **User Stories**: 8
- **Blocking Phases**: 5 (Setup, Database, MCP Tools, Agent, Chat API)
- **Independent User Story Phases**: 8 (all user stories after foundation)
- **Parallel Tasks**: 94 tasks marked [P]
- **MVP Tasks**: T001-T183 (183 tasks for basic chat with task creation)
- **Full Feature Tasks**: All 272 tasks for complete functionality

**Task Distribution by Phase**:
- Phase 1 (Setup): 9 tasks
- Phase 2 (Database): 16 tasks
- Phase 3 (MCP Tools): 68 tasks
- Phase 4 (Agent): 31 tasks
- Phase 5 (Chat API): 26 tasks
- Phase 6 (US1): 33 tasks
- Phase 7 (US2): 6 tasks
- Phase 8 (US3): 6 tasks
- Phase 9 (US6): 5 tasks
- Phase 10 (US4): 6 tasks
- Phase 11 (US5): 6 tasks
- Phase 12 (US7): 6 tasks
- Phase 13 (US8): 6 tasks
- Phase 14 (Testing): 22 tasks
- Phase 15 (Deployment): 26 tasks

**Estimated Completion Order** (if working sequentially):
1. Setup → Database → MCP Tools → Agent → Chat API → US1 (MVP ready: ~183 tasks)
2. US2 → US3 → US6 (Core workflow + context: +17 tasks)
3. US4 → US5 → US7 → US8 (Full features: +24 tasks)
4. Testing → Deployment (Production ready: +48 tasks)

---

## Notes

- All tasks include exact file paths for clarity
- [P] tasks operate on different files and can run in parallel
- [Story] labels map tasks to user stories for traceability
- Each user story phase is independently completable and testable
- Foundation phases (1-5) MUST complete before user story work begins
- User stories can be implemented in any order after foundation is ready
- Recommended: Start with US1 (create) → US2 (view) → US3 (complete) for MVP
- Tests are NOT included as they were not explicitly requested in the specification
- Commit after each logical task group or phase checkpoint
- Stop at any checkpoint to validate independently before proceeding
