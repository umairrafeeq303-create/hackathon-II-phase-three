# Implementation Plan: Task CRUD API Backend

**Branch**: `002-task-crud` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-task-crud/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements the Task CRUD API Backend with RESTful endpoints for task management operations (Create, Read, Update, Delete, Toggle completion). The implementation integrates with Spec 1 (001-auth) authentication system to enforce JWT-based user isolation. The API provides 6 endpoints following `/api/{user_id}/tasks` pattern with filtering by status (all/pending/completed) and sorting by created date or title. All operations validate user ownership to ensure 100% data isolation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (web framework), SQLModel (ORM), python-jose (JWT), passlib with bcrypt (password hashing), pydantic (validation)
**Storage**: Neon Serverless PostgreSQL (accessed via DATABASE_URL environment variable)
**Testing**: pytest (unit, integration, contract tests)
**Target Platform**: Railway (production deployment), Linux server (development)
**Project Type**: Web (backend API service)
**Performance Goals**: Task creation <5 seconds, task list retrieval <1 second, filter/sort operations <1 second, support 1000 concurrent operations
**Constraints**: Sub-second response time for list operations with 10,000+ tasks per user, database queries must use indexes (sub-100ms), zero cross-user data access incidents
**Scale/Scope**: 6 API endpoints, 2 database models (User from Spec 1, Task new), support 10,000+ tasks per user, integrate with existing authentication from Spec 1

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development (Zero Manual Coding)
- ✅ **PASS**: All implementation via Claude Code with Spec-Kit Plus workflow
- Status: Plan generated via `/sp.plan`, implementation will use `/sp.tasks` and `/sp.implement`

### Principle II: Security-First Architecture
- ✅ **PASS**: JWT authentication mandatory for all task endpoints
- ✅ **PASS**: User ID from token must match user ID in URL path
- ✅ **PASS**: All endpoints validate ownership before operations
- ✅ **PASS**: No sensitive data in responses (password hashes, raw tokens)
- Status: Integrates with Spec 1 authentication (get_current_user_id dependency)

### Principle III: Complete Separation of Concerns
- ✅ **PASS**: Backend API provides RESTful endpoints
- ✅ **PASS**: Database access only via SQLModel ORM
- ✅ **PASS**: Frontend will communicate exclusively through REST API
- Status: Task endpoints independent from auth endpoints (Spec 1)

### Principle IV: User Data Isolation and Ownership
- ✅ **PASS**: All task queries filter by authenticated user_id
- ✅ **PASS**: Task creation associates with authenticated user
- ✅ **PASS**: Update/delete verify task ownership (403 on violation)
- ✅ **PASS**: Cross-user access returns 403 Forbidden
- Status: Three-tier validation (JWT → URL match → task ownership)

### Principle V: Production-Ready Code Quality
- ✅ **PASS**: Python type hints required
- ✅ **PASS**: Explicit error handling with HTTP status codes (400, 401, 403, 404, 422, 500)
- ✅ **PASS**: Environment variables for configuration (DATABASE_URL, BETTER_AUTH_SECRET)
- ✅ **PASS**: No hardcoded secrets
- Status: Validation via Pydantic schemas, consistent error format

### Principle VI: RESTful API Design with JWT Authentication
- ✅ **PASS**: All endpoints follow `/api/{user_id}/tasks` pattern
- ✅ **PASS**: HTTP methods: GET (read), POST (create), PUT (update), DELETE (delete), PATCH (toggle)
- ✅ **PASS**: JSON request/response format
- ✅ **PASS**: CORS configured for frontend origin
- ✅ **PASS**: API documentation via FastAPI Swagger UI
- Status: RESTful conventions enforced

**Constitution Compliance**: ✅ ALL GATES PASS - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py          # User model (from Spec 1)
│   │   └── task.py          # Task model (NEW - this feature)
│   ├── schemas/
│   │   ├── task.py          # Pydantic request/response schemas (NEW)
│   │   └── auth.py          # Auth schemas (from Spec 1)
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py      # Authentication routes (from Spec 1)
│   │   │   └── tasks.py     # Task CRUD routes (NEW - this feature)
│   │   └── dependencies/
│   │       └── auth.py      # JWT validation dependency (from Spec 1)
│   ├── core/
│   │   ├── config.py        # Configuration (DATABASE_URL, BETTER_AUTH_SECRET)
│   │   └── database.py      # Database session management (from Spec 1)
│   └── main.py              # FastAPI app initialization
└── tests/
    ├── test_tasks.py        # Task endpoint tests (NEW)
    ├── test_auth.py         # Auth tests (from Spec 1)
    └── conftest.py          # Shared test fixtures

frontend/
├── src/
│   ├── app/
│   │   ├── auth/            # Auth pages (from Spec 1)
│   │   └── tasks/           # Task pages (Spec 3 - frontend)
│   └── lib/
│       └── api.ts           # API client (Spec 3 - frontend)
└── tests/
```

**Structure Decision**: Web application with separate backend and frontend. This feature extends the backend with Task model and task routes. The backend follows FastAPI best practices with models (database), schemas (validation), routes (endpoints), and dependencies (middleware). Integration points with Spec 1 are clearly marked.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected**. All constitution principles are satisfied:
- Spec-Driven Development enforced via `/sp.plan` workflow
- Security-First Architecture via JWT authentication and ownership validation
- Separation of Concerns via backend API design
- User Data Isolation via three-tier validation
- Production-Ready Quality via type hints and error handling
- RESTful API Design via standard conventions

No additional complexity justification required.

## Phase 0: Research & Technical Decisions

**Status**: ✅ COMPLETE

**Output**: `research.md` (10 technical decisions documented)

### Key Research Findings

1. **SQLModel Task Model**: Integer primary key with foreign key to User, indexes on user_id and completed
2. **Pydantic Schemas**: Separate schemas for create, update, and response with automatic whitespace stripping
3. **FastAPI Router**: Dependency injection pattern with JWT validation from Spec 1
4. **Authentication Integration**: Reuses existing `get_current_user_id` dependency, two-step validation (JWT + URL)
5. **Ownership Validation**: Three-tier validation pattern (JWT → URL match → task ownership)
6. **Filtering/Sorting**: Enum-based query parameters with SQLModel query chaining
7. **Database Optimization**: Single-column indexes on user_id and completed (sufficient for performance targets)
8. **Error Handling**: Consistent HTTP status codes with enumeration prevention (404 instead of 403)
9. **Timestamp Management**: Manual updated_at updates in route handlers
10. **Testing Strategy**: pytest with in-memory SQLite for fast integration tests

**All Technical Context unknowns resolved** - Ready for Phase 1 design.

## Phase 1: Design & Contracts

**Status**: ✅ COMPLETE

**Outputs**:
- `data-model.md`: Complete Task model with 7 fields, validation rules, state transitions, performance considerations
- `contracts/task-api.yaml`: OpenAPI 3.0 specification for all 6 endpoints with examples and error responses
- `quickstart.md`: Step-by-step implementation guide with code samples, validation steps, and checklists

### Data Model Summary

**Task Model**:
- 7 fields: id (int PK), user_id (UUID FK), title (str 200), description (str 1000), completed (bool), created_at, updated_at
- Foreign key to User with CASCADE DELETE
- Indexes on user_id and completed
- Default values: completed=False, timestamps auto-generated

**Schemas**:
- TaskCreate: Required title, optional description
- TaskUpdate: All fields optional (partial updates)
- TaskResponse: All fields for client consumption
- Automatic whitespace stripping and validation

**State Transitions**: Created → Updated → Completed → Reopened → Deleted

### API Contracts Summary

**6 Endpoints Defined**:
1. `GET /api/{user_id}/tasks` - List tasks with filtering (status) and sorting (created/title)
2. `POST /api/{user_id}/tasks` - Create new task
3. `GET /api/{user_id}/tasks/{task_id}` - Get single task
4. `PUT /api/{user_id}/tasks/{task_id}` - Update task (title/description)
5. `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
6. `PATCH /api/{user_id}/tasks/{task_id}/toggle` - Toggle completion status

**Authentication**: Bearer JWT token required for all endpoints

**Error Responses**: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 422 (validation error), 500 (server error)

### Agent Context Update

**Status**: ✅ COMPLETE

Agent context file updated with:
- Language: Python 3.11+
- Frameworks: FastAPI, SQLModel, python-jose, passlib, pydantic
- Database: Neon Serverless PostgreSQL

## Re-evaluation: Constitution Check (Post-Design)

*Required gate after Phase 1 design completion*

### Principle I: Spec-Driven Development (Zero Manual Coding)
- ✅ **PASS**: Design artifacts generated via `/sp.plan` command
- ✅ **PASS**: Implementation will follow `/sp.tasks` and `/sp.implement` workflow

### Principle II: Security-First Architecture
- ✅ **PASS**: JWT authentication enforced in all 6 endpoints (Bearer token required)
- ✅ **PASS**: User ID validation at three tiers (JWT extraction → URL match → task ownership)
- ✅ **PASS**: Enumeration prevention (404 instead of 403 for non-owned tasks)
- ✅ **PASS**: No sensitive data in TaskResponse schema

### Principle III: Complete Separation of Concerns
- ✅ **PASS**: Task model isolated in `backend/src/models/task.py`
- ✅ **PASS**: Validation schemas in `backend/src/schemas/task.py`
- ✅ **PASS**: Route handlers in `backend/src/api/routes/tasks.py`
- ✅ **PASS**: Database access only via SQLModel ORM

### Principle IV: User Data Isolation and Ownership
- ✅ **PASS**: All queries include `where(Task.user_id == current_user_id)` filter
- ✅ **PASS**: `get_user_task_or_404` helper enforces ownership on single-task operations
- ✅ **PASS**: Foreign key constraint ensures referential integrity
- ✅ **PASS**: CASCADE DELETE prevents orphaned tasks

### Principle V: Production-Ready Code Quality
- ✅ **PASS**: Python type hints in all model, schema, and route definitions
- ✅ **PASS**: Pydantic validators for whitespace stripping and empty string prevention
- ✅ **PASS**: Explicit HTTP status codes documented in OpenAPI contract
- ✅ **PASS**: Environment variables (DATABASE_URL, BETTER_AUTH_SECRET) required

### Principle VI: RESTful API Design with JWT Authentication
- ✅ **PASS**: URL pattern `/api/{user_id}/tasks` follows RESTful resource conventions
- ✅ **PASS**: HTTP methods aligned with operations (GET, POST, PUT, DELETE, PATCH)
- ✅ **PASS**: JSON request/response format in all contracts
- ✅ **PASS**: OpenAPI 3.0 specification generated for Swagger UI

**Post-Design Constitution Compliance**: ✅ ALL GATES PASS - Approved for task generation

## Implementation Readiness

### Dependencies Satisfied
- ✅ Spec 1 (001-auth) provides User model, JWT validation, database connection
- ✅ Database schema defined with foreign keys and indexes
- ✅ API contracts complete with all 6 endpoints
- ✅ Request/response schemas with validation rules
- ✅ Error handling patterns documented

### Performance Targets Validated
- ✅ Indexes on user_id and completed support sub-second queries
- ✅ Query patterns reviewed (no N+1 queries, efficient filtering)
- ✅ Database connection pooling via SQLModel
- ✅ Expected to handle 10,000+ tasks per user with <1s response time

### Security Requirements Met
- ✅ JWT authentication on all endpoints
- ✅ Three-tier ownership validation
- ✅ Enumeration prevention (consistent 404 responses)
- ✅ Input validation via Pydantic
- ✅ SQL injection prevention via ORM parameterization

### Documentation Complete
- ✅ research.md: Technical decisions and rationale
- ✅ data-model.md: Complete model specifications
- ✅ contracts/task-api.yaml: OpenAPI contract
- ✅ quickstart.md: Implementation guide with validation steps

## Next Steps

**Phase 2: Task Generation** (User action required)

Run the following command to generate actionable, dependency-ordered tasks:

```bash
/sp.tasks
```

This will create `specs/002-task-crud/tasks.md` with:
- Dependency-ordered task list (database → models → routes → tests)
- Test cases for each endpoint
- Validation criteria for each task
- Integration checkpoints

**Expected Implementation Order** (from quickstart.md):
1. Phase 1: Database Model (Task model, migration)
2. Phase 2: Core CRUD (Create, List, Get)
3. Phase 3: Task Management (Update, Delete, Toggle)
4. Phase 4: Filtering & Sorting
5. Phase 5: Testing & Validation

## Artifacts Generated

| File | Status | Lines | Purpose |
|------|--------|-------|---------|
| plan.md | ✅ Complete | 280+ | Implementation plan (this file) |
| research.md | ✅ Complete | 350+ | Technical decisions and rationale |
| data-model.md | ✅ Complete | 400+ | Database models and schemas |
| contracts/task-api.yaml | ✅ Complete | 580+ | OpenAPI 3.0 specification |
| quickstart.md | ✅ Complete | 650+ | Implementation guide |

**Total Documentation**: 2,200+ lines covering architecture, design, and implementation guidance

## Success Criteria Verification

Based on feature specification success criteria:

| Criteria | Design Support | Validation Method |
|----------|---------------|------------------|
| Task creation <5s | ✅ Indexed insert | Integration test timing |
| List view <1s | ✅ Indexed queries | Load test with 10k tasks |
| 10k+ tasks supported | ✅ Database indexes | Performance test |
| 100% data isolation | ✅ Three-tier validation | Security test suite |
| 98% success rate | ✅ Error handling | Production monitoring |
| Filter/sort <1s | ✅ Indexed WHERE/ORDER BY | Integration test timing |

All success criteria have design support and validation methods defined.

## Planning Phase Complete

**Status**: ✅ `/sp.plan` COMPLETE

**Timestamp**: 2026-01-09

**Branch**: `002-task-crud`

**Ready for**: `/sp.tasks` (task generation phase)

---

*Generated by `/sp.plan` command on 2026-01-09*
