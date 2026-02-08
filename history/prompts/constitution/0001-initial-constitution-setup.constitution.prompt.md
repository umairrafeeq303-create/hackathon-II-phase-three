---
id: 0001
title: Initial Constitution Setup
stage: constitution
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: apple
command: /sp.constitution
labels: ["constitution", "project-setup", "governance", "hackathon-phase-2"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

Project: Todo Full-Stack Web Application (Phase II - Hackathon)

Core Principles:

- Spec-driven development through Agentic Dev Stack workflow

- Zero manual coding - all implementation via Claude Code

- Complete separation of concerns (Frontend, Backend, Database)

- Security-first approach with JWT authentication

- User data isolation and ownership validation

- Production-ready code quality

Key Standards:

- Architecture: Clean separation of Next.js frontend and FastAPI backend

- Authentication: Better Auth with JWT tokens (shared secret across services)

- API Design: RESTful conventions with proper HTTP methods and status codes

- Database: SQLModel ORM with Neon PostgreSQL (proper relationships and indexes)

- Security: All endpoints protected, user ownership enforced, passwords hashed

- Code Quality: TypeScript for frontend, type hints for backend, proper error handling

- Documentation: Clear README, API docs (Swagger), environment variable templates

Technology Constraints:

- Frontend: Next.js 16+ (App Router only), TypeScript, Tailwind CSS, Better Auth

- Backend: Python FastAPI, SQLModel, python-jose (JWT), passlib (bcrypt)

- Database: Neon Serverless PostgreSQL

- Deployment: Vercel (frontend), Railway (backend)

- No manual coding: All code generated through Claude Code with Spec-Kit Plus

API Requirements:

- All endpoints under /api/{user_id}/ pattern

- JWT token required in Authorization: Bearer <token> header

- User ID in URL must match authenticated user from token

- Proper status codes: 200, 201, 400, 401, 403, 404, 422, 500

- JSON responses with consistent structure

- CORS configured for frontend origin only

Security Standards:

- Passwords hashed with bcrypt (10 salt rounds minimum)

- JWT tokens signed with BETTER_AUTH_SECRET (shared between services)

- Token expiry: 7 days maximum

- User isolation: Users can only access their own tasks

- No sensitive data in responses (no password hashes)

- Environment variables for all secrets

- HTTPS only in production

Database Schema Requirements:

- Users table: id (PK, UUID), email (unique), name, hashed_password, created_at

- Tasks table: id (PK, int), user_id (FK), title (200 chars max), description (1000 chars max), completed (boolean), created_at, updated_at

- Indexes: user_id, email, completed status

- Foreign key constraints enforced

Success Criteria:

- All 5 basic CRUD features implemented as web application

- User signup/signin working with Better Auth

- All API endpoints functional with JWT protection

- Users can only see and modify their own tasks

- Responsive frontend interface (mobile and desktop)

- Zero manual coding - all via Claude Code

- Deployable to Vercel (frontend) and Railway (backend)

- Complete documentation with setup instructions

Development Workflow:

1. Write specification (sp.specify)

2. Generate implementation plan (sp.plan)

3. Break into subtasks

4. Implement via Claude Code (no manual edits)

5. Validate against spec

6. Iterate if needed

7. Deploy and verify

Quality Gates:

- All specs must be complete before implementation

- Each feature must pass authentication checks

- User ownership validation on all endpoints

- Error handling for all edge cases

- Environment variables properly documented

- Frontend and backend can run independently

- Database migrations (if any) documented

Constraints:

- Must use exact tech stack specified (no substitutions)

- All code generated through Claude Code workflow

- No hardcoded secrets or credentials

- Monorepo structure with /frontend and /backend directories

- Shared BETTER_AUTH_SECRET between frontend and backend

- Database connection via environment variable only

Review Standards:

- Prompts quality and effectiveness

- Spec completeness and clarity

- Implementation accuracy vs specs

- Iteration efficiency

- Final product functionality

- Documentation completeness

## Response snapshot

Created initial project constitution v1.0.0 for Todo Full-Stack Web Application (Phase II - Hackathon).

**Constitution Structure**:
- 6 Core Principles: Spec-Driven Development, Security-First Architecture, Separation of Concerns, User Data Isolation, Production-Ready Code Quality, RESTful API Design
- Technology Stack Standards: Next.js 16+/FastAPI/Neon PostgreSQL with specific library requirements
- API Requirements: `/api/{user_id}/` pattern with JWT authentication and proper HTTP status codes
- Security Standards: bcrypt password hashing, JWT token validation, user isolation, environment variable management
- Database Schema: Users and Tasks tables with proper indexes and foreign key constraints
- Development Workflow: 7-step spec-driven process from specification to deployment
- Quality Gates: Pre-implementation, during implementation, and pre-deployment checkpoints
- Deployment Standards: Vercel (frontend) and Railway (backend) with environment configuration
- Governance: Amendment process, compliance verification, complexity justification requirements

**Version Rationale**:
- Version 1.0.0 (MAJOR): Initial constitution establishing all core governance principles
- Ratified and Last Amended: 2026-01-09

**Template Consistency**:
- ✅ plan-template.md: Constitution Check section aligns with principles
- ✅ spec-template.md: Requirements structure supports security and ownership validation
- ✅ tasks-template.md: Task categorization supports phased development approach

**No Follow-up TODOs**: All placeholders filled, no deferred items.

## Outcome

- ✅ Impact: Established complete project governance framework with 6 core principles, technology constraints, security standards, and quality gates for hackathon Phase II todo application development
- 🧪 Tests: N/A (constitutional document, no tests required)
- 📁 Files: Created/updated .specify/memory/constitution.md (264 lines)
- 🔁 Next prompts: Execute `/sp.specify` to create feature specification for todo application using constitutional principles
- 🧠 Reflection: Constitution successfully captures all requirements from user input including zero-manual-coding constraint, security-first approach, and complete tech stack specification. Clear governance model with semantic versioning and amendment process.

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders successfully filled, template consistency validated
- Graders run and results (PASS/FAIL): Template consistency check PASS (all 3 templates validated)
- Prompt variant (if applicable): N/A (initial constitution creation)
- Next experiment (smallest change to try): N/A (foundation established, ready for feature specification phase)
