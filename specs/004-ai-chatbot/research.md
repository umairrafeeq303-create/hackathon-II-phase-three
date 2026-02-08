# Research: Todo AI Chatbot - Natural Language Task Management

**Feature**: 004-ai-chatbot
**Date**: 2026-01-27
**Status**: Complete

## Executive Summary

Research phase confirms feasibility of building a stateless AI chatbot for task management using OpenAI Agents SDK + MCP SDK. All technical decisions finalized with no blocking issues. Architecture pattern selected: database-backed stateless request-response cycle.

## Research Questions & Findings

### RQ-001: Specification Completeness
**Status**: ✅ Complete
**Finding**: All 45 functional requirements testable and un ambiguous. No [NEEDS CLARIFICATION] markers.
**Action**: Proceed with implementation

### RQ-002: SDK Availability and Suitability
**Status**: ✅ Confirmed
**SDKs**: OpenAI Agents SDK 1.0+ (included in openai package), Official MCP SDK (mcp package)
**Suitability**: Perfect fit for stateless architecture - both support pure function tool invocations
**Installation**: `pip install openai mcp` (backend), `npm install @openai/chatkit` (frontend)

### RQ-003: Stateless Architecture Pattern
**Pattern**: Database-backed request-response cycle
**Flow**:
1. Load conversation from database (or create new)
2. Load last 50 messages ordered by created_at DESC
3. Store user message (role="user", content=request)
4. Execute OpenAI agent with conversation history as context
5. Store assistant message (role="assistant", content=response)
6. Return conversation_id + response + tool_calls

**Benefits**:
- No server memory dependency
- Horizontal scaling without session affinity
- Survives server restarts with zero context loss
- Meets Principle VII requirements

**Trade-offs**: +20-50ms latency for database queries (acceptable within <3s budget)

### RQ-004: Conversation History Limit
**Decision**: 50 messages (25 user + 25 assistant exchanges)
**Rationale**:
- GPT-3.5-turbo context window: 4096 tokens
- 50 messages ≈ 2000-3000 tokens
- Leaves ~1000 tokens for system prompt + response generation
- Query performance: <50ms with proper indexing

**Query**: `SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at DESC LIMIT 50`

### RQ-005: Model Selection
**Decision**: GPT-3.5-turbo
**Comparison**:

| Factor | GPT-3.5-turbo | GPT-4 |
| --- | --- | --- |
| Cost | $0.002/1K tokens | $0.03/1K tokens |
| Response time | 1-2 seconds | 3-5 seconds |
| Accuracy | Sufficient for tasks | Excellent |
| Context window | 4096 tokens | 8192 tokens |

**Conclusion**: GPT-3.5-turbo meets requirements at 15x lower cost. GPT-4 available as upgrade if needed.

### RQ-006: Error Handling Strategy
**Three-tier approach**:

**Tier 1 - OpenAI API**:
- RateLimitError: Exponential backoff (1s, 2s, 4s), max 3 retries
- APIConnectionError: Retry once, then fail gracefully
- Timeout: Retry once with extended timeout

**Tier 2 - Database**:
- Transaction rollback on failures
- Partial state preservation (user message saved even if agent fails)
- Descriptive error messages

**Tier 3 - Validation**:
- 400 Bad Request: Invalid input format
- 422 Unprocessable Entity: Validation failed (Pydantic)
- 403 Forbidden: Ownership violation

**User-facing translation**:
- "RateLimitError" → "I'm thinking... (taking a bit longer)"
- "DatabaseError" → "I'm having trouble saving your message. Please try again."
- "ValidationError" → "That message is too long (max 10,000 characters)"

### RQ-007: Database Indexing Strategy
**Required indexes**:

```sql
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

**Performance estimates**:
- Conversation lookup by user_id: <5ms
- Message retrieval (50 rows): <50ms
- Total query time: <55ms (well within budget)

### RQ-008: MCP Tool Ownership Validation
**Two-step validation pattern**:

**Step 1 - User ID validation**:
```python
def validate_user_id(user_id: str, authenticated_user_id: str):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
```

**Step 2 - Resource ownership validation**:
```python
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id  # Enforces ownership
).first()
if not task:
    return {"error": "Task not found", "code": "NOT_FOUND"}
```

**Implementation**: Every MCP tool accepts `user_id` parameter from JWT and validates against task ownership.

### RQ-009: Phase II Authentication Integration
**Reuse strategy**:
- Import `get_current_user_id` dependency from existing auth module
- Import `User` model from existing models
- Endpoint decorator: `@app.post("/api/{user_id}/chat", dependencies=[Depends(get_current_user_id)])`
- JWT validation logic unchanged from Phase II

**No code duplication** - authentication layer fully reused.

### RQ-010: Performance Estimates
**End-to-end latency breakdown**:

| Component | Time (ms) |
| --- | --- |
| Load conversation | 5-10 |
| Load 50 messages | 10-50 |
| Store user message | 5-10 |
| Execute OpenAI agent | 1000-2000 |
| MCP tool invocation | 5-10 |
| Store assistant message | 5-10 |
| **Total** | **1030-2090** |

**95th percentile estimate**: 2.1 seconds (well under <3s requirement ✅)

**Worst case** (with 3 retries): 2.1s + 7s backoff = 9.1s (rare, handled with user feedback)

## Technical Decisions Summary

**15 Key Decisions Finalized**:

1. **TD-001**: Stateless request cycle with database-backed history
2. **TD-002**: Defense-in-depth validation (Pydantic + tool-level + DB constraints)
3. **TD-003**: 50 message history limit
4. **TD-004**: GPT-3.5-turbo model selection
5. **TD-005**: Tool call transparency in API response
6. **TD-006**: Three-tier error handling strategy
7. **TD-007**: Structured system prompt with explicit rules
8. **TD-008**: Multi-layer conversation isolation security
9. **TD-009**: Exponential backoff retry logic (1s, 2s, 4s)
10. **TD-010**: Connection pool configuration (pool_size=20, max_overflow=10)
11. **TD-011**: Message content limit (10,000 characters)
12. **TD-012**: Conversation creation on first message
13. **TD-013**: Standardized tool response format
14. **TD-014**: React useChat hook for frontend state
15. **TD-015**: Multi-layer testing strategy (unit, integration, e2e, restart, load)

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
| --- | --- | --- | --- |
| OpenAI API rate limits | High | Medium | Exponential backoff, usage monitoring |
| Token limit exceeded | Medium | Low | 50 message limit, use GPT-3.5-turbo |
| DB connection pool exhaustion | High | Low | Pool size=20, max_overflow=10, monitoring |
| AI misunderstands intent | Medium | Medium | Prompt engineering, clarification prompts |
| Security bypass via manipulation | High | Low | Multi-layer validation, tool-level ownership checks |

## Next Steps

1. ✅ Research complete - all questions answered
2. → Generate data-model.md with database schema
3. → Generate quickstart.md with setup instructions
4. → Generate API contracts (chat-api.json, mcp-tools.json)
5. → Proceed to /sp.tasks for implementation task breakdown

## Approval

**Research Status**: ✅ APPROVED
**Gate Status**: ✅ ALL CONSTITUTION PRINCIPLES PASS
**Ready for Phase 1**: Yes - proceed with data model and API contracts
