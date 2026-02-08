---
id: 0002
title: Update constitution for Phase III AI chatbot
stage: constitution
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: apple
command: /sp.constitution
labels: ["constitution", "ai-chatbot", "phase-iii", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - CLAUDE.md
tests:
  - none
---

## Prompt

```
# /sp.constitution Prompt for Phase III: Todo AI Chatbot

**Command**: `/sp.constitution`

**Purpose**: Update project constitution to include Phase III AI chatbot principles and technology stack additions

---

## Prompt to Execute

```
/sp.constitution

Update the project constitution (.specify/memory/constitution.md) to include Phase III AI Chatbot capabilities and technology standards.

## New Technologies to Add:

**Backend Technologies (Add to existing list)**:
- OpenAI Agents SDK 1.0+ (AI agent orchestration with tool invocation)
- Official MCP SDK (Model Context Protocol for stateless tool server)
- OpenAI API (GPT-3.5-turbo or GPT-4 for natural language processing)

**Frontend Technologies (Add to existing list)**:
- OpenAI ChatKit (React components for conversational UI)

**Environment Variables (Add to existing list)**:
- OPENAI_API_KEY (required for OpenAI API access)

## New Architectural Principles to Document:

### VII. Stateless Conversational AI Architecture

**Principle**: AI chatbot server MUST be completely stateless. All conversation state and history MUST be stored in the database. Every request MUST independently load conversation context from database without relying on server memory.

**Rationale**: Enables horizontal scaling, prevents state loss on server restart, supports multi-instance deployment without session affinity. Critical for production resilience and cloud-native architecture.

**Implementation Requirements**:
- Server maintains NO in-memory conversation state or session storage
- Every chat request loads conversation history from database independently
- MCP tools are pure functions with no instance variables or shared state
- Conversation and Message tables store all conversation data
- Database queries optimized with indexes for <50ms history loading
- Supports server restart without losing conversation context

### VIII. MCP Tool Design Principles

**Principle**: MCP (Model Context Protocol) tools MUST be stateless, independently validate all parameters including user ownership, and return standardized response formats. Each tool MUST perform complete validation without relying on agent or middleware validation.

**Rationale**: Ensures security enforcement at tool level (defense in depth), prevents privilege escalation if agent misbehaves, enables independent tool testing, and maintains consistency across all tool operations.

**Implementation Requirements**:
- Each MCP tool validates user_id parameter matches resource ownership
- Tools return standardized success format: {task_id, status, title}
- Tools return standardized error format: {error, code}
- No shared state between tool invocations
- Tools use database session per invocation (no persistent connections)
- All parameters validated before database operations

### IX. AI Agent Safety and Transparency

**Principle**: AI agent behavior MUST be guided by clear system prompts with explicit tool selection criteria and error handling guidelines. Tool invocations MUST be logged and optionally displayed to users for transparency. Agent responses MUST NOT expose sensitive data or technical implementation details.

**Rationale**: Ensures predictable and safe AI behavior, builds user trust through transparency, prevents information disclosure, and enables debugging of agent decisions.

**Implementation Requirements**:
- System prompts define personality, tool selection rules, and error handling
- Agent responses use friendly, conversational language (no technical jargon)
- Tool calls included in API response for optional display to users
- All tool invocations logged with parameters and results
- Agent cannot access or expose other users' data through natural language manipulation
- Rate limiting and cost monitoring for AI API usage

## Updated Technology Stack Section:

Add to **Active Technologies** section:
- OpenAI Agents SDK 1.0+ (agent orchestration, tool integration, conversation management) (004-ai-chatbot)
- Official MCP SDK (stateless tool server for task operations) (004-ai-chatbot)
- OpenAI API / GPT-3.5-turbo (natural language processing and intent recognition) (004-ai-chatbot)
- OpenAI ChatKit (React components for conversational UI) (004-ai-chatbot)

## Recent Changes Section:

Add entry:
- 004-ai-chatbot: Added OpenAI Agents SDK, Official MCP SDK, OpenAI API (GPT-3.5-turbo), OpenAI ChatKit for conversational AI task management with stateless architecture

## Constitution Version Update:

Update version from current to next minor version (e.g., 1.0.0 → 1.1.0)

Document in SYNC IMPACT REPORT:
- Version Change: 1.0.0 → 1.1.0
- Type: MINOR (Added Phase III AI capabilities)
- Rationale: Extended constitution with AI chatbot architecture principles
- Modified Principles: Added VII (Stateless AI), VIII (MCP Tools), IX (AI Safety)
- Modified Technologies: Added OpenAI stack components

Please update the constitution file with these additions while preserving all existing Phase II principles and technologies.
```
```

## Response snapshot

Updated the project constitution from version 1.0.0 to 1.1.0 with Phase III AI chatbot principles and technology stack.

**Changes made:**

1. **Added Three New Architectural Principles:**
   - VII. Stateless Conversational AI Architecture (stateless server, database-stored conversation history)
   - VIII. MCP Tool Design Principles (stateless tools, independent validation, standardized responses)
   - IX. AI Agent Safety and Transparency (system prompts, logging, user trust)

2. **Updated Technology Stack:**
   - Backend: Added OpenAI Agents SDK 1.0+, Official MCP SDK, OpenAI API (GPT-3.5-turbo/GPT-4)
   - Frontend: Added OpenAI ChatKit
   - Configuration: Added OPENAI_API_KEY environment variable

3. **Extended Database Schema:**
   - Added Conversations table (id, user_id, title, timestamps)
   - Added Messages table (id, conversation_id, role, content, tool_calls, created_at)
   - Added foreign key constraints with cascade delete

4. **Updated Files:**
   - .specify/memory/constitution.md (version 1.1.0)
   - CLAUDE.md (Active Technologies and Recent Changes sections)

All Phase II principles (I-VI) preserved. Templates remain compatible with constitution changes.

## Outcome

- ✅ Impact: Constitution successfully updated to v1.1.0 with Phase III AI chatbot architecture principles
- 🧪 Tests: Not applicable (documentation update)
- 📁 Files: Modified .specify/memory/constitution.md and CLAUDE.md
- 🔁 Next prompts: Ready to proceed with /sp.specify for Phase III AI chatbot feature
- 🧠 Reflection: Constitution amendment follows semantic versioning (MINOR bump for new principles), maintains backward compatibility with Phase II, establishes security-first AI architecture with stateless design

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All placeholders filled, principles documented with rationale and implementation requirements, version incremented correctly, Sync Impact Report complete
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): None required - constitution update complete and ready for Phase III specification
