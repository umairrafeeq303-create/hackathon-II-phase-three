---
id: 0002
title: Generate Phase III Implementation Plan
stage: plan
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-ai-chatbot
branch: 004-ai-chatbot
user: apple
command: /sp.plan
labels: ["planning", "ai-chatbot", "architecture", "mcp-tools", "phase-iii"]
links:
  spec: specs/004-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/004-ai-chatbot/plan.md
 - specs/004-ai-chatbot/research.md
 - specs/004-ai-chatbot/data-model.md
 - specs/004-ai-chatbot/quickstart.md
 - specs/004-ai-chatbot/contracts/chat-api.json
 - specs/004-ai-chatbot/contracts/mcp-tools.json
tests:
 - Constitution check: All 9 principles PASS
 - Specification completeness: 45 functional requirements validated
 - Research questions: 10/10 answered with decisions
 - Technical decisions: 15/15 documented
---

## Prompt

# /sp.plan Prompt for Phase III: Todo AI Chatbot

Generate a complete implementation plan for the Todo AI Chatbot feature (004-ai-chatbot) based on the specification in `specs/004-ai-chatbot/spec.md`.

## Plan Requirements

### 1. Constitution Check
Execute constitution check against ALL 9 principles in `.specify/memory/constitution.md` (version 1.1.0):
- Principle I: Explicit Defaults and Configuration Management
- Principle II: Defense-in-Depth Validation
- Principle III: Stateless Authentication with JWT
- Principle IV: Database Schema as Source of Truth
- Principle V: RESTful API Design Patterns
- Principle VI: Security-First Error Messages
- Principle VII: Stateless Conversational AI Architecture (NEW)
- Principle VIII: MCP Tool Design Principles (NEW)
- Principle IX: AI Agent Safety and Transparency (NEW)

For each principle, provide:
- Status: ✅ PASS or ❌ FAIL
- Validation: Evidence from spec.md requirements that demonstrate compliance
- Risk mitigation: If any principle is at risk, document mitigation strategy

**GATE**: Plan CANNOT proceed if any principle status is FAIL.

### 2. Technical Context Section
Fill EVERY field in the Technical Context section. If information is missing from spec.md, make informed architectural decisions and document them:

**Required Fields**:
- Existing Phase II stack: Python 3.11+, FastAPI, SQLModel, Neon PostgreSQL, JWT authentication, Next.js 14+, Better Auth, Tailwind CSS
- New Phase III stack: OpenAI Agents SDK 1.0+, Official MCP SDK, OpenAI API (GPT-3.5-turbo), OpenAI ChatKit
- Database: Extend existing Neon PostgreSQL with 2 new tables (Conversations, Messages)
- Authentication: Reuse Phase II JWT validation (get_current_user_id dependency)
- Frontend: Add `/chat` route with OpenAI ChatKit components

**NO [NEEDS CLARIFICATION] markers allowed** - make decisions based on:
- Industry best practices for conversational AI
- OpenAI Agents SDK documentation patterns
- MCP SDK stateless tool server examples
- Existing Phase II codebase architecture

### 3. Project Structure
Define complete directory structure showing:
- Backend additions: `backend/src/ai/` (agent orchestration), `backend/src/mcp/` (tool implementations)
- Frontend additions: `frontend/src/app/chat/` (chat UI), `frontend/src/components/chat/` (chat components)
- Database migrations: `backend/alembic/versions/` (new migration for Conversations and Messages tables)
- Configuration: Environment variable additions (OPENAI_API_KEY)

### 4. Phase 0: Research (REQUIRED)
Before implementation planning, answer these 10 research questions:

**RQ-001**: Are all requirements in spec.md complete and unambiguous, or are there [NEEDS CLARIFICATION] markers?
**RQ-002**: Which OpenAI SDK and MCP SDK versions are available and suitable for this use case?
**RQ-003**: What is the exact stateless architecture pattern for conversation management (database schema, request cycle)?
**RQ-004**: How many messages of conversation history should be loaded on each request (token limits, performance)?
**RQ-005**: Which OpenAI model to use (GPT-3.5-turbo vs GPT-4) based on cost, speed, and accuracy requirements?
**RQ-006**: What is the error handling strategy for OpenAI API failures (rate limits, timeouts, network errors)?
**RQ-007**: What database indexes are needed for conversation/message queries to meet <3s response time requirement?
**RQ-008**: How will MCP tools validate user_id ownership for security (FR-028, FR-029, FR-030)?
**RQ-009**: Can Phase II authentication (JWT, get_current_user_id) be reused without modification?
**RQ-010**: What are the performance estimates for database queries, OpenAI API calls, and total request latency?

### 5. Technical Decisions (REQUIRED)
Document 15 technical decisions with rationale:

**TD-001**: Stateless request cycle design (load history → store user msg → run agent → store assistant msg → return)
**TD-002**: Validation strategy (Pydantic request schema + tool-level user_id checks + database constraints)
**TD-003**: Conversation history limit (number of messages to load)
**TD-004**: Model selection (GPT-3.5-turbo vs GPT-4)
**TD-005**: Tool call transparency (include tool_calls array in response or omit)
**TD-006**: Error handling tiers (OpenAI API, database, validation)
**TD-007**: System prompt structure (explicit rules, examples, constraints)
**TD-008**: Conversation isolation strategy (database query filters, foreign keys)
**TD-009**: Retry logic for rate limits (exponential backoff, max retries)
**TD-010**: Database connection pooling (pool size, timeout, max overflow)
**TD-011**: Message content limits (max characters to prevent abuse)
**TD-012**: Conversation creation strategy (create on first message vs explicit endpoint)
**TD-013**: Tool response format standardization (success/error schemas)
**TD-014**: Frontend state management (React hooks, context, or library)
**TD-015**: Testing strategy (unit tests, integration tests, end-to-end tests)

### 6. Phase 1: Design and Contracts
Generate these deliverables automatically within this plan execution:

**Deliverable 1**: `specs/004-ai-chatbot/data-model.md`
- SQLModel definitions for Conversation and Message tables
- Alembic migration script with indexes
- Pydantic request/response schemas (ChatRequest, ChatResponse, ToolCall)
- Query patterns for loading history, storing messages, validating ownership

**Deliverable 2**: `specs/004-ai-chatbot/quickstart.md`
- Prerequisites: Phase II completion, OpenAI API key
- Backend setup: Install dependencies (openai, mcp), configure OPENAI_API_KEY, run migration
- Frontend setup: Install @openai/chatkit, configure chat route
- Testing steps: 5 test cases with expected results
- Troubleshooting: Common errors and solutions

**Deliverable 3**: `specs/004-ai-chatbot/contracts/chat-api.json`
- OpenAPI 3.1 specification for POST /api/{user_id}/chat endpoint
- Request schema: {message: string, conversation_id?: UUID}
- Response schema: {conversation_id: UUID, response: string, tool_calls?: ToolCall[]}
- Error schemas: 400, 401, 403, 404, 500 with examples

**Deliverable 4**: `specs/004-ai-chatbot/contracts/mcp-tools.json`
- JSON schema definitions for all 5 MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- Input schemas with validation rules (user_id, task_id, title, description, status)
- Output schemas for success and error responses
- Examples for each tool with realistic data

## Success Criteria

Plan is complete when:
1. ✅ All 9 constitution principles show PASS status with evidence
2. ✅ Technical Context section has ZERO [NEEDS CLARIFICATION] markers
3. ✅ All 10 research questions answered with actionable findings
4. ✅ All 15 technical decisions documented with clear rationale
5. ✅ Phase 1 deliverables generated: data-model.md, quickstart.md, contracts/chat-api.json, contracts/mcp-tools.json
6. ✅ Project structure shows all new directories and files
7. ✅ Plan references spec.md requirements explicitly (FR-001, FR-002, etc.)

## Response snapshot

### Constitution Check Results
**Status**: ✅ ALL 9 PRINCIPLES PASS

**Principle VII: Stateless Conversational AI Architecture** - ✅ PASS
- FR-040: Server stores NO conversation state in memory
- FR-041: Every request loads conversation history from database independently
- FR-023: Agent loads full conversation history on every request
- FR-042: MCP tools are pure functions with no instance variables

**Principle VIII: MCP Tool Design Principles** - ✅ PASS
- FR-024: All 5 MCP tools implemented (add_task, list_tasks, complete_task, delete_task, update_task)
- FR-025: Tool responses standardized with {task_id, status, title} or {error, code}
- FR-026: Each tool invocation uses fresh database session
- FR-027: Tools are pure functions with no shared state

**Principle IX: AI Agent Safety and Transparency** - ✅ PASS
- FR-031: User-friendly error messages without exposing internals
- FR-032: Tool calls optionally returned in response for transparency
- FR-033: System prompt guides safe, helpful responses
- FR-034: Agent validates intent before invoking tools

### Phase 0: Research Findings Summary

**All 10 Research Questions Answered**:
- RQ-001: Specification is complete with 45 testable requirements, no clarification needed
- RQ-002: OpenAI SDK 1.0+ and Official MCP SDK confirmed suitable for stateless architecture
- RQ-003: Stateless pattern: load conversation → load 50 messages → store user msg → run agent → store assistant msg
- RQ-004: 50 message history limit (balances context vs token constraints)
- RQ-005: GPT-3.5-turbo selected (15x cheaper than GPT-4, 1-2s response time, sufficient accuracy)
- RQ-006: Three-tier error handling: OpenAI API (retry with backoff) → Database (rollback) → Validation (400/422)
- RQ-007: 3 indexes required: conversations.user_id, messages.conversation_id, messages.created_at
- RQ-008: Two-step validation: JWT user_id → tool parameter user_id → database filter by user_id
- RQ-009: Phase II auth fully reusable (get_current_user_id dependency, JWT validation unchanged)
- RQ-010: Total latency estimate: 1030-2090ms (database 55ms + OpenAI 1000-2000ms + overhead 5-10ms)

**All 15 Technical Decisions Documented**:
- TD-001: Stateless request cycle with database-backed history
- TD-002: Defense-in-depth validation (Pydantic + tool-level + DB)
- TD-003: 50 message history limit
- TD-004: GPT-3.5-turbo model selection
- TD-005: Tool call transparency in API response
- TD-006: Three-tier error handling strategy
- TD-007: Structured system prompt with explicit rules
- TD-008: Multi-layer conversation isolation security
- TD-009: Exponential backoff retry logic (1s, 2s, 4s)
- TD-010: Connection pool configuration (pool_size=20, max_overflow=10)
- TD-011: Message content limit (10,000 characters)
- TD-012: Conversation creation on first message
- TD-013: Standardized tool response format
- TD-014: React useChat hook for frontend state
- TD-015: Multi-layer testing strategy (unit, integration, e2e, restart, load)

### Phase 1: Design Deliverables Generated

**✅ data-model.md** (392 lines):
- SQLModel Conversation model with user_id FK, timestamps, message relationship
- SQLModel Message model with conversation_id FK, role (user/assistant), content
- Alembic migration script with 3 indexes for query optimization
- Pydantic ChatRequest schema (message, conversation_id)
- Pydantic ChatResponse schema (conversation_id, response, tool_calls)
- Query patterns: load conversation, load 50 messages, store user/assistant messages
- Storage estimates: 50KB per conversation, 500MB for 1000 users (10 conversations each)

**✅ quickstart.md** (375 lines):
- Prerequisites: Phase II completion verification commands
- Backend setup: pip install openai mcp tenacity, OPENAI_API_KEY configuration, alembic migration
- Frontend setup: npm install @openai/chatkit, environment variables
- 5 test cases: create task, view tasks, complete task, conversation context, server restart
- Troubleshooting: OpenAI API key not found, rate limit errors, conversation not found, database query slow, CORS errors
- Production deployment: Railway environment variables, Vercel deployment

**✅ contracts/chat-api.json** (292 lines):
- OpenAPI 3.1 specification for POST /api/{user_id}/chat endpoint
- Security: Bearer JWT authentication with user_id validation
- Request schema: ChatRequest with message (1-10000 chars) and optional conversation_id
- Response schema: ChatResponse with conversation_id, response, tool_calls array
- Error responses: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (conversation not found), 500 (internal error)
- Examples: newConversation, continueConversation, taskCreated, tasksListed

**✅ contracts/mcp-tools.json** (340 lines):
- 5 MCP tool schemas: add_task, list_tasks, complete_task, delete_task, update_task
- Input schemas with user_id (UUID), task_id (integer), title (1-200 chars), description (max 1000 chars), status (all/pending/completed)
- Output schemas: success {task_id, status, title} or error {error, code}
- Constraints: stateless functions, ownership validation, standardized responses, database sessions per invocation
- Error codes: NOT_FOUND, UNAUTHORIZED, VALIDATION_ERROR
- Examples for each tool with realistic inputs and outputs

### Project Structure
```
backend/
├── src/
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── agent.py          # OpenAI agent orchestration
│   │   └── prompts.py        # System prompts and templates
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py         # MCP server initialization
│   │   └── tools.py          # 5 MCP tool implementations
│   ├── models/
│   │   ├── conversation.py   # Conversation SQLModel
│   │   └── message.py        # Message SQLModel
│   ├── schemas/
│   │   ├── chat.py           # ChatRequest, ChatResponse, ToolCall
│   └── routers/
│       └── chat.py           # POST /api/{user_id}/chat endpoint
├── alembic/versions/
│   └── xxx_add_conversation_tables.py  # Migration script
└── requirements.txt          # +openai, +mcp, +tenacity

frontend/
├── src/
│   ├── app/
│   │   └── chat/
│   │       ├── page.tsx      # Chat UI route
│   │       └── layout.tsx
│   ├── components/
│   │   └── chat/
│   │       ├── ChatInterface.tsx  # Main chat component
│   │       └── MessageList.tsx
│   └── lib/
│       └── api-chat.ts       # Chat API client
└── package.json              # +@openai/chatkit
```

## Outcome

- ✅ Impact: Complete implementation plan with constitution validation, research, and design deliverables for Phase III AI Chatbot feature
- 🧪 Tests: Constitution check (9/9 PASS), Research questions (10/10 answered), Technical decisions (15/15 documented)
- 📁 Files: Created plan.md (447 lines), research.md (193 lines), data-model.md (392 lines), quickstart.md (375 lines), chat-api.json (292 lines), mcp-tools.json (340 lines)
- 🔁 Next prompts: Update CLAUDE.md agent context, run /sp.tasks to generate implementation task breakdown
- 🧠 Reflection: Successfully completed Phase 0 (Research) and Phase 1 (Design & Contracts). All constitution principles validated. Ready for task generation and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - all deliverables generated successfully with complete information
- Graders run and results (PASS/FAIL): Constitution check PASS (9/9), Specification completeness PASS (45 FRs), Research completeness PASS (10/10 RQs), Technical decisions PASS (15/15 TDs), Contract generation PASS (2/2 files)
- Prompt variant (if applicable): Standard /sp.plan workflow with enhanced Phase 0 research requirements
- Next experiment (smallest change to try): Consider generating ADR for stateless architecture decision (TD-001) if significant enough by three-part test (impact, alternatives, scope)
