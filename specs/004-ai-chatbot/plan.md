# Implementation Plan: Todo AI Chatbot - Natural Language Task Management

**Branch**: `004-ai-chatbot` | **Date**: 2026-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-ai-chatbot/spec.md`

## Summary

Implement an AI-powered chatbot interface that enables users to manage todo tasks through natural language conversations using OpenAI Agents SDK integrated with an MCP (Model Context Protocol) server. The system follows a completely stateless architecture where all conversation state and history are stored in the database, supporting horizontal scaling and server restarts without context loss.

**Technical Approach**:
- Backend: FastAPI + OpenAI Agents SDK + Official MCP SDK for stateless tool invocations
- Frontend: Next.js + OpenAI ChatKit for conversational UI
- Database: Extend existing Neon PostgreSQL with Conversation and Message tables
- Architecture: Fully stateless server loading conversation history from database on every request
- Integration: Reuse Phase II authentication (JWT), Task model, and frontend structure

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.3+ (frontend), Node.js 20+ (frontend runtime)
**Primary Dependencies**: OpenAI Agents SDK 1.0+, Official MCP SDK, OpenAI API (gpt-3.5-turbo), FastAPI, SQLModel, OpenAI ChatKit, React 19+
**Storage**: Neon Serverless PostgreSQL (extend existing Phase II database with 2 new tables)
**Testing**: pytest + pytest-asyncio (backend), Jest + React Testing Library (frontend)
**Target Platform**: Railway (backend), Vercel (frontend)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <3s response time (95th percentile), <500ms tool invocations, 100+ concurrent sessions, <50ms conversation history loading
**Constraints**: Stateless architecture (no in-memory state), conversation history limited to 50 messages, OpenAI API rate limits (3500 RPM for gpt-3.5-turbo), maximum message length 10,000 characters
**Scale/Scope**: 1 new API endpoint (chat), 5 MCP tools, 2 new database tables, 1 new frontend route, extend existing Phase II infrastructure

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development (Zero Manual Coding)
**Status**: ✅ PASS
**Validation**: All implementation will follow sp.specify → sp.plan → sp.tasks → sp.implement workflow. Specification complete at specs/004-ai-chatbot/spec.md with 8 user stories and 45 functional requirements.

### Principle II: Security-First Architecture
**Status**: ✅ PASS
**Validation**:
- FR-002: Chat endpoint requires JWT validation
- FR-009: User ownership enforced on conversations
- FR-011, FR-017, FR-019, FR-021: All MCP tools validate user_id matches resource ownership
- Principle VIII implementation: Defense-in-depth with tool-level validation
- FR-027, FR-028: Agent cannot access other users' data through natural language manipulation

### Principle III: Complete Separation of Concerns
**Status**: ✅ PASS
**Validation**:
- Backend (FastAPI) and Frontend (Next.js) remain independent services
- Frontend communicates via REST API only (POST /api/{user_id}/chat)
- Database access exclusively through backend SQLModel ORM
- MCP tools are independent, stateless functions
- Each service runnable independently

### Principle IV: User Data Isolation and Ownership
**Status**: ✅ PASS
**Validation**:
- FR-009: Conversations filtered by authenticated user_id
- FR-031: Foreign key from conversations.user_id enforces ownership
- FR-011, FR-017, FR-019, FR-021: Each MCP tool validates user owns the task
- Cross-user access attempts return 403 Forbidden
- Agent system prompt includes strict user isolation instructions

### Principle V: Production-Ready Code Quality
**Status**: ✅ PASS
**Validation**:
- Frontend: TypeScript with strict type checking
- Backend: Python type hints on all functions
- FR-037: Explicit error handling for all failure modes
- Environment variables for OPENAI_API_KEY and DATABASE_URL
- No hardcoded secrets in codebase

### Principle VI: RESTful API Design with JWT Authentication
**Status**: ✅ PASS
**Validation**:
- FR-001: POST /api/{user_id}/chat follows pattern
- FR-002: JWT token validation on every request
- FR-008: JSON request/response format
- User ID in token must match URL path
- CORS configured for frontend origin
- FastAPI Swagger UI auto-generated documentation

### Principle VII: Stateless Conversational AI Architecture
**Status**: ✅ PASS
**Validation**:
- FR-040: Server stores NO conversation state in memory
- FR-041: Every request loads conversation history from database independently
- FR-023: Agent loads full conversation history on every request
- FR-042: MCP tools are pure functions with no instance variables
- FR-043: Database session per request (no persistent connections)
- FR-045: Server restarts do not lose conversation context
- User Story 8 validates stateless architecture with restart test

### Principle VIII: MCP Tool Design Principles
**Status**: ✅ PASS
**Validation**:
- FR-011, FR-017, FR-019, FR-021: Each tool independently validates user_id
- FR-022: Standardized response format {task_id, status, title}
- FR-010-FR-021: All 5 tools are stateless
- FR-043: Tools use database session per invocation
- No shared state between tool invocations
- All parameters validated before database operations

### Principle IX: AI Agent Safety and Transparency
**Status**: ✅ PASS
**Validation**:
- FR-026: System prompts define personality and tool selection rules
- FR-027: Agent asks for clarification when ambiguous
- FR-028: Friendly, conversational responses (no technical jargon)
- FR-008: Tool calls included in API response for transparency
- Tool invocations logged with parameters and results
- FR-009: Agent cannot access other users' data
- Rate limiting via OpenAI API quota management

**GATE RESULT**: ✅ ALL PRINCIPLES PASS - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/004-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (complete)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── chat-api.json    # POST /api/{user_id}/chat contract
│   └── mcp-tools.json   # All 5 MCP tool definitions
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py              # Existing (Phase II)
│   │   ├── task.py              # Existing (Phase II)
│   │   ├── conversation.py      # NEW: Conversation model
│   │   └── message.py           # NEW: Message model
│   ├── api/
│   │   ├── auth.py              # Existing (Phase II)
│   │   ├── tasks.py             # Existing (Phase II)
│   │   └── chat.py              # NEW: Chat endpoint
│   ├── ai/                      # NEW: AI agent directory
│   │   ├── __init__.py
│   │   ├── agent.py             # Agent initialization and configuration
│   │   ├── runner.py            # Agent execution and conversation management
│   │   └── prompts.py           # System prompts and instructions
│   ├── mcp/                     # NEW: MCP server directory
│   │   ├── __init__.py
│   │   ├── server.py            # MCP server initialization
│   │   └── tools/               # MCP tool implementations
│   │       ├── __init__.py
│   │       ├── add_task.py      # Add task tool
│   │       ├── list_tasks.py    # List tasks tool
│   │       ├── complete_task.py # Complete task tool
│   │       ├── delete_task.py   # Delete task tool
│   │       └── update_task.py   # Update task tool
│   ├── schemas/
│   │   ├── task.py              # Existing (Phase II)
│   │   └── chat.py              # NEW: ChatRequest, ChatResponse schemas
│   ├── database.py              # Existing (Phase II - extend)
│   ├── dependencies.py          # Existing (Phase II - reuse JWT validation)
│   └── main.py                  # Existing (Phase II - add chat route)
├── tests/
│   ├── unit/
│   │   ├── test_mcp_tools.py    # NEW: MCP tool unit tests
│   │   └── test_agent.py        # NEW: Agent unit tests
│   ├── integration/
│   │   └── test_chat_api.py     # NEW: Chat endpoint integration tests
│   └── e2e/
│       └── test_conversations.py # NEW: End-to-end conversation tests
├── alembic/
│   └── versions/
│       └── xxx_add_conversation_tables.py # NEW: Migration for Conversation + Message
├── requirements.txt             # UPDATE: Add openai, openai-agents-sdk, mcp
└── .env.example                 # UPDATE: Add OPENAI_API_KEY

frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/              # Existing (Phase II)
│   │   ├── tasks/               # Existing (Phase II)
│   │   └── chat/                # NEW: Chat route
│   │       ├── page.tsx         # Chat page component
│   │       └── layout.tsx       # Chat layout (optional)
│   ├── components/
│   │   ├── auth/                # Existing (Phase II)
│   │   ├── tasks/               # Existing (Phase II)
│   │   └── chat/                # NEW: Chat components
│   │       ├── ChatInterface.tsx   # Main chat interface with ChatKit
│   │       ├── MessageList.tsx     # Message display component
│   │       ├── MessageInput.tsx    # Message input component
│   │       └── LoadingIndicator.tsx # Loading state component
│   ├── lib/
│   │   ├── api.ts               # Existing (Phase II - extend)
│   │   └── chatApi.ts           # NEW: Chat API client
│   ├── hooks/
│   │   └── useChat.ts           # NEW: Chat state management hook
│   └── context/
│       └── AuthContext.tsx      # Existing (Phase II - reuse)
├── package.json                 # UPDATE: Add @openai/chatkit
└── .env.local.example           # Existing (Phase II)

specs/
└── 004-ai-chatbot/              # This directory
```

**Structure Decision**: Web application structure (Option 2). Extends existing Phase II backend and frontend with new AI/MCP modules and chat UI. Backend adds `ai/` and `mcp/` directories for agent and tool logic. Frontend adds `chat/` route and components for ChatKit integration. Database models extend existing schema with Conversation and Message tables. All Phase II code preserved and reused (auth, tasks, user).

## Complexity Tracking

> **No violations** - All constitution principles pass without exceptions.

# PHASE 0: RESEARCH & TECHNICAL DECISIONS

*Research phase to resolve technical unknowns and finalize architectural decisions*

## Research Questions

**RQ-001: Is the specification complete?**
- **Finding**: Yes - no [NEEDS CLARIFICATION] markers found in spec.md
- **Evidence**: All 45 functional requirements (FR-001 to FR-045) are testable and unambiguous
- **Action**: None required - proceed with planning

**RQ-002: Are OpenAI Agents SDK and MCP SDK available and suitable?**
- **Finding**: Yes - both SDKs are production-ready and officially supported
- **Evidence**: OpenAI Agents SDK 1.0+ provides agent orchestration with tool invocation; Official MCP SDK enables stateless tool servers
- **Suitability**: Perfect fit for stateless architecture requirement
- **Action**: Use openai Python package (includes Agents SDK) + mcp package

**RQ-003: What is the optimal stateless architecture pattern?**
- **Finding**: Database-backed request-response cycle
- **Pattern**: Load history from DB → Store user message → Run agent with context → Store assistant message → Return response
- **Rationale**: Eliminates server memory dependency, enables horizontal scaling, survives restarts
- **Action**: Implement per-request conversation loading in chat endpoint

**RQ-004: How many messages should conversation history include?**
- **Finding**: 50 messages (25 user + 25 assistant exchanges)
- **Rationale**: Balances context richness with token limits (gpt-3.5-turbo has 4096 token context window)
- **Estimate**: 50 messages ≈ 2000-3000 tokens, leaving room for system prompt and response
- **Action**: Implement LIMIT 50 in conversation history query, ordered by created_at DESC

**RQ-005: Which OpenAI model to use?**
- **Decision**: GPT-3.5-turbo
- **Rationale**:
  - Cost-effective ($0.002/1K tokens vs $0.03/1K for GPT-4)
  - Fast response time (1-2 seconds vs 3-5 seconds)
  - Sufficient for task management natural language understanding
  - Meets <3s response time requirement (SC-004)
- **Alternative**: GPT-4 available as upgrade path if accuracy issues emerge
- **Action**: Configure agent with model="gpt-3.5-turbo"

**RQ-006: How to handle OpenAI API rate limits and errors?**
- **Finding**: Three-tier error handling strategy
- **Tier 1 - Rate Limits**: Exponential backoff (1s, 2s, 4s) with max 3 retries
- **Tier 2 - API Errors**: Catch RateLimitError, APIError, Timeout and return user-friendly messages
- **Tier 3 - Fallback**: Store partial state (user message saved even if agent fails)
- **Action**: Implement retry decorator and error translation layer

**RQ-007: What indexes are needed for conversation history queries?**
- **Finding**: Three indexes required for optimal performance
- **Index 1**: `conversations.user_id` (for user conversation lookup)
- **Index 2**: `messages.conversation_id` (for message retrieval)
- **Index 3**: `messages.created_at` (for chronological ordering)
- **Performance**: Should achieve <50ms query time for 50 messages
- **Action**: Include indexes in Alembic migration

**RQ-008: How to validate ownership at MCP tool level?**
- **Finding**: Two-step validation pattern
- **Step 1**: Validate user_id parameter matches authenticated user (from JWT)
- **Step 2**: For task operations, query task with user_id filter and verify existence
- **Implementation**: Pass user_id from JWT to each MCP tool invocation
- **Action**: Add user_id parameter to all 5 MCP tool functions

**RQ-009: How to integrate with existing Phase II authentication?**
- **Finding**: Reuse existing JWT validation dependency
- **Integration**: Import `get_current_user_id` dependency from Phase II auth module
- **Endpoint**: `@app.post("/api/{user_id}/chat", dependencies=[Depends(get_current_user_id)])`
- **Validation**: JWT user_id must match URL {user_id} parameter
- **Action**: Import and reuse existing auth dependencies

**RQ-010: What are performance estimates for database + OpenAI API?**
- **Database query** (load 50 messages): 10-50ms (with indexes)
- **OpenAI API call** (gpt-3.5-turbo): 1000-2000ms (1-2 seconds)
- **MCP tool invocation** (database operation): 5-10ms
- **Message storage** (2 INSERTs): 5-10ms
- **Total end-to-end**: 1020-2070ms (worst case ~2.1 seconds)
- **95th percentile estimate**: <3 seconds ✅ (meets SC-004)
- **Action**: Monitor and optimize if performance degrades

## Technical Decisions

**TD-001: Stateless Request Cycle Design**
- **Decision**: Implement fully stateless request-response cycle with database-backed history
- **Approach**:
  1. Load conversation by ID or create new
  2. Load last 50 messages from database
  3. Store user message with role="user"
  4. Execute agent with loaded conversation history
  5. Store assistant message with role="assistant"
  6. Return conversation_id + response + tool_calls
- **Rationale**: Eliminates server memory dependency, enables horizontal scaling, meets Principle VII
- **Trade-off**: Slightly higher latency (DB queries) vs stateful approach, but worth it for scalability

**TD-002: MCP Tool Parameter Validation Strategy**
- **Decision**: Defense-in-depth with multi-layer validation
- **Layer 1**: Pydantic schema validation (type checking, required fields)
- **Layer 2**: Tool-level user_id ownership validation
- **Layer 3**: Database constraint validation (foreign keys, unique constraints)
- **Rationale**: Prevents privilege escalation even if agent misbehaves (Principle VIII)
- **Implementation**: Each tool validates user_id before any database operation

**TD-003: Conversation History Limit**
- **Decision**: 50 messages maximum (LIMIT 50 in query, ORDER BY created_at DESC)
- **Rationale**: Balances context richness with token limits and performance
- **Token estimate**: 50 messages ≈ 2000-3000 tokens (safe for gpt-3.5-turbo's 4096 limit)
- **Performance**: <50ms query time with proper indexing
- **Alternative considered**: 100 messages (rejected due to token limit risk)

**TD-004: Agent Model Selection**
- **Decision**: Use gpt-3.5-turbo as primary model
- **Rationale**: Cost-effective, fast, sufficient accuracy for task management
- **Cost**: $0.002/1K tokens (vs $0.03/1K for GPT-4)
- **Response time**: 1-2 seconds (vs 3-5 seconds for GPT-4)
- **Upgrade path**: GPT-4 available if accuracy issues emerge
- **Configuration**: `model="gpt-3.5-turbo"` in agent initialization

**TD-005: Tool Call Transparency**
- **Decision**: Include tool calls in API response for optional display to users
- **Format**: `tool_calls: [{tool: "list_tasks", parameters: {...}, result: {...}}]`
- **Rationale**: Builds user trust through transparency (Principle IX)
- **Usage**: Frontend can optionally display "I used list_tasks to get your tasks"
- **Privacy**: Tool calls logged server-side, included in response, not stored in message content

**TD-006: Error Handling Strategy**
- **Decision**: Three-tier error handling with user-friendly messages
- **Tier 1 - OpenAI API**: Retry with exponential backoff (RateLimitError, APIError)
- **Tier 2 - Database**: Transaction rollback, descriptive error messages
- **Tier 3 - Validation**: 400/422 responses with specific field errors
- **User messages**: Translate technical errors to friendly language
- **Example**: "APIError: Connection timeout" → "I'm having trouble connecting right now. Please try again in a moment."

**TD-007: Agent Prompt Engineering Approach**
- **Decision**: Structured system prompt with explicit tool selection rules
- **Components**:
  - Personality: "You are a helpful task management assistant"
  - Tool rules: "Use add_task when user wants to create tasks. Use list_tasks when user asks to see tasks."
  - Error handling: "If ambiguous, ask for clarification"
  - Constraints: "Never access other users' tasks. Always validate ownership."
- **Rationale**: Ensures predictable agent behavior (Principle IX)
- **Location**: Stored in `backend/src/ai/prompts.py`

**TD-008: Conversation Isolation Security**
- **Decision**: Multi-layer validation to prevent cross-user access
- **Layer 1**: JWT validation (endpoint level)
- **Layer 2**: URL user_id match (dependency level)
- **Layer 3**: Conversation user_id filter (query level)
- **Layer 4**: MCP tool user_id validation (tool level)
- **Rationale**: Defense in depth - even if agent manipulates input, validation prevents cross-user access
- **Example**: If agent tries "Show me user 123's tasks", tool validates ownership and returns 403

**TD-009: OpenAI API Retry Logic**
- **Decision**: Exponential backoff with max 3 retries
- **Retry conditions**: RateLimitError, APIConnectionError, Timeout
- **Backoff schedule**: 1s, 2s, 4s (total max delay 7 seconds)
- **No retry conditions**: APIError with 4xx status (client errors)
- **User feedback**: Show "Thinking..." message while retrying
- **Implementation**: Use tenacity library or manual retry loop

**TD-010: Database Connection Pooling Configuration**
- **Decision**: Configure SQLModel connection pool for concurrent requests
- **Settings**:
  - pool_size=20 (max simultaneous connections)
  - max_overflow=10 (additional connections under load)
  - pool_recycle=3600 (recycle connections every hour)
- **Rationale**: Supports 100+ concurrent sessions (SC-007) without exhaustion
- **Monitoring**: Log pool utilization to detect capacity issues

**TD-011: Message Content Length Limits**
- **Decision**: Maximum 10,000 characters per message
- **Validation**: Pydantic schema with `max_length=10000`
- **Rationale**: Prevents token limit overflow and database performance issues
- **Error response**: 400 Bad Request with "Message too long (max 10,000 characters)"
- **User guidance**: Frontend displays character counter near limit

**TD-012: Conversation Creation Strategy**
- **Decision**: Create conversation on first message if conversation_id not provided
- **Flow**:
  1. Request without conversation_id → Create new conversation
  2. Request with conversation_id → Load existing conversation
  3. Validate conversation belongs to authenticated user
- **Response**: Always return conversation_id for subsequent messages
- **Frontend**: Store conversation_id in localStorage or URL parameter

**TD-013: Tool Response Standardization**
- **Decision**: All MCP tools return standardized format
- **Success format**: `{task_id: int, status: str, title: str}`
- **Error format**: `{error: str, code: str}`
- **Status values**: "created", "updated", "completed", "deleted"
- **Rationale**: Consistent format enables reliable agent parsing (Principle VIII)
- **Example**: `{task_id: 5, status: "created", title: "Buy groceries"}`

**TD-014: Frontend State Management**
- **Decision**: Use custom useChat hook with React state
- **State**: `{messages: [], loading: boolean, error: string | null, conversationId: string | null}`
- **Actions**: `sendMessage(text)`, `retryMessage()`, `clearError()`
- **Persistence**: Store conversationId in localStorage
- **Rationale**: Simple, avoids Redux complexity for single-feature state

**TD-015: Testing Strategy for Stateless Architecture**
- **Decision**: Multi-layer testing approach
- **Unit tests**: Individual MCP tools (ownership validation, response format)
- **Integration tests**: Chat endpoint (request-response cycle)
- **E2E tests**: Full conversation flow (multi-turn with context)
- **Restart test**: Start conversation → restart server → continue conversation (validates statelessness)
- **Load test**: 100 concurrent sessions (validates SC-007)
- **Framework**: pytest + pytest-asyncio for backend, Jest + RTL for frontend

# PHASE 1: DESIGN & API CONTRACTS

*Design documentation, data models, and API contracts - to be generated by /sp.plan*

**Status**: Ready for generation

**Deliverables**:
1. `data-model.md` - Database schema for Conversation and Message models
2. `quickstart.md` - Setup guide with prerequisites and testing instructions
3. `contracts/chat-api.json` - OpenAPI spec for POST /api/{user_id}/chat
4. `contracts/mcp-tools.json` - JSON schema definitions for all 5 MCP tools

**Next Steps**:
1. Generate data-model.md with SQLModel definitions and Alembic migration
2. Generate quickstart.md with installation and testing steps
3. Generate API contracts in contracts/ directory
4. Update agent context file (CLAUDE.md) with new technologies

---

*Note: Phase 1 deliverables will be generated automatically by continuing this /sp.plan execution*
