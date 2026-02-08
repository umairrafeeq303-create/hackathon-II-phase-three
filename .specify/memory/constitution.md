<!--
SYNC IMPACT REPORT:

Version Change: 1.0.0 → 1.1.0
Type: MINOR (Added Phase III AI capabilities)
Rationale: Extended constitution with AI chatbot architecture principles while preserving all Phase II principles and technologies

Modified/Added Principles:
- Added: VII. Stateless Conversational AI Architecture
- Added: VIII. MCP Tool Design Principles
- Added: IX. AI Agent Safety and Transparency
- Preserved: I-VI from Phase II (all existing principles)

Modified/Added Sections:
- Technology Stack Standards: Added OpenAI Agents SDK, Official MCP SDK, OpenAI API, OpenAI ChatKit
- Added new environment variables: OPENAI_API_KEY
- Recent Changes: Added 004-ai-chatbot entry

Template Consistency Status:
✅ plan-template.md - Constitution Check section will evaluate AI architecture principles
✅ spec-template.md - Requirements structure supports conversational AI user stories
✅ tasks-template.md - Task categorization supports AI chatbot implementation phases

Follow-up TODOs: None
-->

# Todo Full-Stack Web Application (Phase III: AI Chatbot) Constitution

## Core Principles

### I. Spec-Driven Development (Zero Manual Coding)
All implementation MUST be performed through Claude Code with Spec-Kit Plus workflow. Manual code editing is prohibited. The workflow follows: specification (sp.specify) → planning (sp.plan) → task generation (sp.tasks) → implementation (sp.implement) with validation at each stage.

**Rationale**: Ensures consistent, documented, and traceable development process where all changes are intentional and aligned with specifications. Prevents ad-hoc modifications that bypass architectural review.

### II. Security-First Architecture
User authentication via Better Auth with JWT tokens is mandatory for all API endpoints. Passwords MUST be hashed with bcrypt (minimum 10 salt rounds). All endpoints MUST validate JWT tokens via Authorization: Bearer header. User ID from token MUST match user ID in endpoint URL path. No sensitive data (password hashes, raw tokens) in API responses.

**Rationale**: Protects user data and prevents unauthorized access. JWT tokens provide stateless authentication. bcrypt ensures password security. Token-to-URL validation prevents privilege escalation.

### III. Complete Separation of Concerns
Frontend (Next.js) and Backend (FastAPI) MUST operate as independent services. Frontend communicates with backend exclusively through REST API. Database access MUST only occur through backend via SQLModel ORM. Each service MUST be runnable independently for development and testing.

**Rationale**: Enables independent deployment, testing, and scaling. Prevents tight coupling. Allows different teams to work in parallel. Facilitates technology upgrades without full system rewrites.

### IV. User Data Isolation and Ownership
Each user MUST only access their own tasks. All task queries MUST filter by authenticated user_id. Task creation MUST associate tasks with authenticated user. Update and delete operations MUST verify task ownership before execution. Cross-user data access MUST return 403 Forbidden.

**Rationale**: Ensures data privacy and prevents data leakage. Critical for multi-tenant applications. Protects against unauthorized data manipulation.

### V. Production-Ready Code Quality
Frontend MUST use TypeScript with strict type checking. Backend MUST use Python type hints. All error conditions MUST have explicit handling with appropriate HTTP status codes (400, 401, 403, 404, 422, 500). Environment variables MUST be used for all configuration. No hardcoded secrets or credentials in codebase.

**Rationale**: Type safety prevents runtime errors. Explicit error handling improves debugging and user experience. Environment variables enable secure configuration management across environments.

### VI. RESTful API Design with JWT Authentication
All API endpoints follow `/api/{user_id}/` pattern. HTTP methods: GET (read), POST (create), PUT (update), DELETE (delete). JSON request/response format with consistent structure. CORS configured to allow frontend origin only. API documentation generated via FastAPI Swagger UI.

**Rationale**: RESTful conventions ensure predictable API behavior. URL structure encodes ownership. CORS restrictions prevent unauthorized frontend access. Generated docs reduce maintenance burden.

### VII. Stateless Conversational AI Architecture
AI chatbot server MUST be completely stateless. All conversation state and history MUST be stored in the database. Every request MUST independently load conversation context from database without relying on server memory. Server maintains NO in-memory conversation state or session storage.

**Rationale**: Enables horizontal scaling, prevents state loss on server restart, supports multi-instance deployment without session affinity. Critical for production resilience and cloud-native architecture.

**Implementation Requirements**:
- Server maintains NO in-memory conversation state or session storage
- Every chat request loads conversation history from database independently
- MCP tools are pure functions with no instance variables or shared state
- Conversation and Message tables store all conversation data
- Database queries optimized with indexes for <50ms history loading
- Supports server restart without losing conversation context

### VIII. MCP Tool Design Principles
MCP (Model Context Protocol) tools MUST be stateless, independently validate all parameters including user ownership, and return standardized response formats. Each tool MUST perform complete validation without relying on agent or middleware validation.

**Rationale**: Ensures security enforcement at tool level (defense in depth), prevents privilege escalation if agent misbehaves, enables independent tool testing, and maintains consistency across all tool operations.

**Implementation Requirements**:
- Each MCP tool validates user_id parameter matches resource ownership
- Tools return standardized success format: {task_id, status, title}
- Tools return standardized error format: {error, code}
- No shared state between tool invocations
- Tools use database session per invocation (no persistent connections)
- All parameters validated before database operations

### IX. AI Agent Safety and Transparency
AI agent behavior MUST be guided by clear system prompts with explicit tool selection criteria and error handling guidelines. Tool invocations MUST be logged and optionally displayed to users for transparency. Agent responses MUST NOT expose sensitive data or technical implementation details.

**Rationale**: Ensures predictable and safe AI behavior, builds user trust through transparency, prevents information disclosure, and enables debugging of agent decisions.

**Implementation Requirements**:
- System prompts define personality, tool selection rules, and error handling
- Agent responses use friendly, conversational language (no technical jargon)
- Tool calls included in API response for optional display to users
- All tool invocations logged with parameters and results
- Agent cannot access or expose other users' data through natural language manipulation
- Rate limiting and cost monitoring for AI API usage

## Technology Stack Standards

**Frontend Requirements**:
- Next.js 16+ with App Router (no Pages Router)
- TypeScript with strict mode enabled
- Tailwind CSS for styling
- Better Auth for authentication client
- OpenAI ChatKit (React components for conversational UI)
- Deployed to Vercel

**Backend Requirements**:
- Python FastAPI framework
- SQLModel ORM for database operations
- python-jose for JWT handling
- passlib with bcrypt for password hashing
- OpenAI Agents SDK 1.0+ (AI agent orchestration with tool invocation)
- Official MCP SDK (Model Context Protocol for stateless tool server)
- OpenAI API (GPT-3.5-turbo or GPT-4 for natural language processing)
- Deployed to Railway

**Database Requirements**:
- Neon Serverless PostgreSQL
- Connection via DATABASE_URL environment variable
- SQLModel schema definitions

**Shared Configuration**:
- BETTER_AUTH_SECRET shared between frontend and backend
- Same secret used for JWT signing and verification
- OPENAI_API_KEY (required for OpenAI API access)

## API Requirements

**Endpoint Structure**:
All endpoints MUST follow `/api/{user_id}/` pattern where `{user_id}` is the authenticated user's UUID.

**Authentication**:
- Authorization header format: `Authorization: Bearer <jwt_token>`
- Token MUST contain user_id claim
- Token MUST be validated on every request
- User ID in token MUST match user ID in URL path

**HTTP Status Codes**:
- 200: Successful GET, PUT, DELETE
- 201: Successful POST (resource created)
- 400: Bad Request (invalid input format)
- 401: Unauthorized (missing or invalid token)
- 403: Forbidden (user attempting to access another user's data)
- 404: Not Found (resource doesn't exist)
- 422: Unprocessable Entity (validation failed)
- 500: Internal Server Error

**Response Format**:
All responses MUST be JSON with consistent structure. Error responses MUST include descriptive messages.

**CORS Configuration**:
Backend MUST allow requests only from the configured frontend origin. Credentials MUST be allowed for cookie/token handling.

## Security Standards

**Password Management**:
- Passwords MUST be hashed with bcrypt
- Minimum 10 salt rounds
- Plain-text passwords NEVER stored or logged
- Password hashes NEVER returned in API responses

**JWT Token Standards**:
- Tokens signed with BETTER_AUTH_SECRET
- Token expiry: maximum 7 days
- Tokens MUST include user_id claim
- Token validation on every protected endpoint

**User Isolation**:
- Every task query filtered by authenticated user_id
- Task ownership verified before updates/deletes
- Cross-user access attempts return 403 Forbidden
- User enumeration prevented (consistent error messages)

**Environment Security**:
- All secrets in environment variables
- No credentials in version control
- .env files in .gitignore
- Environment variable templates documented

**Production Security**:
- HTTPS enforced in production
- Secure cookie settings (httpOnly, secure flags)
- SQL injection prevention via ORM parameterization
- XSS prevention via frontend framework defaults

## Database Schema Requirements

**Users Table**:
```
id: UUID (Primary Key)
email: String (Unique, Indexed)
name: String
hashed_password: String
created_at: DateTime
```

**Tasks Table**:
```
id: Integer (Primary Key, Auto-increment)
user_id: UUID (Foreign Key → Users.id, Indexed)
title: String (max 200 characters)
description: String (max 1000 characters)
completed: Boolean (Indexed)
created_at: DateTime
updated_at: DateTime
```

**Conversations Table** (Phase III):
```
id: UUID (Primary Key)
user_id: UUID (Foreign Key → Users.id, Indexed)
title: String (optional, auto-generated)
created_at: DateTime
updated_at: DateTime
```

**Messages Table** (Phase III):
```
id: UUID (Primary Key)
conversation_id: UUID (Foreign Key → Conversations.id, Indexed)
role: String (user|assistant|tool)
content: String
tool_calls: JSON (optional, for agent tool invocations)
created_at: DateTime
```

**Constraints**:
- Foreign key from Tasks.user_id to Users.id with cascade delete
- Foreign key from Conversations.user_id to Users.id with cascade delete
- Foreign key from Messages.conversation_id to Conversations.id with cascade delete
- Unique constraint on Users.email
- Indexes on: user_id, email, completed status, conversation_id
- NOT NULL constraints on all required fields

## Development Workflow

1. **Specification** (`/sp.specify`): Define feature requirements and user stories
2. **Planning** (`/sp.plan`): Generate architectural plan and technical approach
3. **Task Generation** (`/sp.tasks`): Break plan into actionable, dependency-ordered tasks
4. **Implementation** (`/sp.implement`): Execute tasks via Claude Code
5. **Validation**: Verify implementation matches specification
6. **Iteration**: Refine based on validation results
7. **Deployment**: Deploy frontend to Vercel, backend to Railway

**Repository Structure**:
```
/frontend     - Next.js application
/backend      - FastAPI application
.specify/     - Spec-Kit Plus templates and configuration
specs/        - Feature specifications and plans
history/      - Prompt history records and ADRs
```

## Quality Gates

**Before Implementation**:
- Specification MUST be complete and unambiguous
- All user stories MUST have acceptance criteria
- Architecture plan MUST address security requirements
- Database schema MUST be defined

**During Implementation**:
- Each task MUST be validated before marking complete
- Authentication checks MUST be verified on protected endpoints
- User ownership validation MUST be tested
- Error handling MUST cover all edge cases

**Before Deployment**:
- Environment variables MUST be documented
- Frontend and backend MUST run independently
- Database migrations (if any) MUST be documented
- All CRUD operations MUST be functional
- User isolation MUST be verified

## Deployment and Documentation Standards

**Frontend Deployment (Vercel)**:
- Environment variables: NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
- Automatic deployment on git push to main
- Production domain configured

**Backend Deployment (Railway)**:
- Environment variables: DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS, OPENAI_API_KEY
- Automatic deployment on git push to main
- Health check endpoint configured

**Documentation Requirements**:
- README with setup instructions
- Environment variable template (.env.example)
- API documentation via FastAPI Swagger
- Database schema documentation
- Deployment instructions

## Governance

This constitution supersedes all other development practices and MUST be enforced at every stage.

**Amendment Process**:
1. Proposed changes documented with rationale
2. Impact analysis on existing features
3. Migration plan for incompatible changes
4. Approval required before adoption
5. Version increment following semantic versioning

**Compliance Verification**:
- All code reviews MUST verify constitutional compliance
- Spec validation MUST confirm security requirements met
- Task generation MUST include ownership validation tasks
- Deployment checklists MUST verify environment security

**Complexity Justification**:
Any violation of simplicity or addition of complexity MUST be justified with:
- Specific problem being solved
- Why simpler alternatives are insufficient
- Long-term maintenance cost acknowledged

**Runtime Guidance**:
For agent-specific development guidance and execution workflows, refer to `CLAUDE.md` in the project root.

**Version**: 1.1.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-27
