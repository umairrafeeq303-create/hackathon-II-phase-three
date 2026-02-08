---
id: 002
title: Create Frontend UI Implementation Plan
stage: plan
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: frontend-ui
branch: 003-frontend-ui
user: apple
command: /sp.plan
labels: ["planning", "frontend", "architecture", "nextjs", "better-auth", "typescript", "tailwind"]
links:
  spec: specs/003-frontend-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-frontend-ui/plan.md
tests:
  - Constitutional compliance validated (all 6 principles passed)
  - Technical context fully specified (no NEEDS CLARIFICATION markers)
  - Integration points with Spec 1 & 2 documented
  - Phase 0 research tasks defined (8 research areas)
  - Phase 1 design artifacts specified (data-model.md, contracts/, quickstart.md)
---

## Prompt

User executed `/sp.plan` with context about Frontend UI & API Integration implementation.

**User Input**:
```
# sp.plan - Frontend UI & API Integration Implementation Plan

## Context
Specs 1 (Auth) and 2 (Task API) are complete. Now implement the Next.js frontend that connects everything together.

## Reference Documents
- /sp.constitution
- Completed Spec 1, 2, and 3 specifications
- Existing backend implementation

## Plan Structure
[18 detailed phases covering: Next.js setup, TypeScript types, Better Auth, API client, Authentication pages, Layout components, Protected routes, Dashboard, Task components, Filters, CRUD operations, Responsive design, Testing, Polish & Documentation]

Format as: "Implementation Plan: Frontend UI & API Integration - Phase II Todo App"
```

**Context Available**:
- Spec 3 (Frontend UI) complete with 9 user stories, 71 functional requirements, 10 success criteria
- Constitution with 6 core principles
- Existing backend with FastAPI + SQLModel (Specs 1 & 2 implemented)
- Frontend directory with Next.js 16 + Better Auth already in package.json

**Planning Workflow**:
1. Setup: Run setup-plan.sh to get feature context
2. Load context: Read spec.md, constitution.md, plan template
3. Execute planning: Fill Technical Context, Constitution Check, Phase 0 research, Phase 1 design
4. Report artifacts generated

## Response snapshot

Created comprehensive 770-line implementation plan with:

**Technical Context** (fully specified):
- Language: TypeScript 5.3+ with Next.js 16 (React 19)
- Dependencies: Next.js 16, Better Auth 1.0, Tailwind CSS 3.4
- Storage: localStorage for JWT tokens, API backend for data
- Testing: Manual integration testing
- Platform: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Performance: <2s initial load, <1s task list, <100ms interaction feedback, <500ms filters
- Constraints: Backend API integration, JWT token matching, mobile-first (≥375px)
- Scope: 9 user stories, 71 requirements, ~15-20 components, 2000-3000 LOC

**Constitution Check** (✅ ALL 6 PRINCIPLES PASSED):
- ✅ I. Spec-Driven Development: All via /sp.implement workflow
- ✅ II. Security-First Architecture: Better Auth + JWT, protected routes, 401 handling
- ✅ III. Separation of Concerns: Independent frontend/backend, REST API only
- ✅ IV. User Data Isolation: user_id in all API URLs, backend validates ownership
- ✅ V. Production-Ready Quality: TypeScript strict, error handling, env vars, loading states
- ✅ VI. RESTful API Design: Consumes backend REST endpoints, JWT on all requests

**Project Structure**:
- Documentation: plan.md, research.md, data-model.md, quickstart.md, contracts/
- Source: frontend/src/ with app/, components/, lib/, types/, styles/
- Web app structure with Next.js App Router conventions

**Phase 0: Research** (8 research tasks):
1. Better Auth + Next.js 16 integration patterns
2. JWT token management best practices
3. Next.js 16 App Router patterns (protected routes, loading, errors)
4. Tailwind CSS responsive design (mobile-first breakpoints)
5. TypeScript API client patterns (fetch wrapper, typing, interceptors)
6. Form validation strategies (client-side, real-time feedback)
7. State management for task list (React hooks, optimistic updates)
8. Loading and error states (skeletons, spinners, toasts, boundaries)

**Phase 1: Design** (3 artifacts):
1. data-model.md: TypeScript types for User, Task, TaskFilters, Forms, API responses
2. contracts/api-client.ts: API client interface for auth + task endpoints
3. quickstart.md: Dev setup, environment config, testing flows, common issues

**Implementation Phases** (13 phases for /sp.tasks reference):
- Phase 1: Project Setup
- Phase 2: Foundation (types, API client, utils, Better Auth)
- Phase 3: Authentication UI (US1 & US2 - P1)
- Phase 4: Protected Routes & Layout (US3 - P1)
- Phase 5: Task Display (US3 - P1)
- Phase 6: Task Creation (US4 - P1)
- Phase 7: Task Completion Toggle (US5 - P1)
- Phase 8: Task Filtering & Sorting (US6 - P1)
- Phase 9: Task Editing (US7 - P2)
- Phase 10: Task Deletion (US8 - P2)
- Phase 11: Logout (US9 - P2)
- Phase 12: Responsive Design & Polish
- Phase 13: Integration Testing & Documentation

**Dependencies & Sequencing**:
- Critical path: Setup → Foundation → Authentication → Protected Routes → All protected features
- Parallelizable: After Phase 4, Phases 5-11 can run in parallel
- File coordination: Sequential updates to api.ts, types/index.ts, page.tsx

**Validation Checkpoints**:
After each phase verify: tasks complete, dev server runs, UI renders, tests pass, API works, auth persists, no console errors

**Risk Mitigation**:
- Better Auth complexity: Phase 0 research validates pattern
- JWT token expiry: Phase 2 implements 401 interceptor
- TypeScript mismatches: Phase 1 contracts from Spec 1 & 2 docs
- CORS issues: Documented in quickstart with backend config
- Responsive breakage: Phase 12 dedicated multi-device testing
- Form validation inconsistency: Phase 2 reusable validation utilities
- State management complexity: Start with hooks, ADR if library needed

**Success Criteria Mapping**:
All 10 success criteria from spec.md mapped to specific implementation phases with clear strategies for achievement.

**Architectural Decision Triggers**:
Documented 4 scenarios requiring ADRs: state management library addition, token storage change, real-time updates requirement, CSS framework addition.

## Outcome

- ✅ Impact: Complete architectural plan ready for task generation. Defines all technical decisions, implementation phases, and integration patterns for Next.js frontend. Establishes foundation for 2000-3000 LOC application with 15-20 components.
- 🧪 Tests: Constitutional compliance validated (6/6 principles passed). Technical context complete (0 NEEDS CLARIFICATION markers). Integration points documented for Specs 1 & 2. Phase 0 research covers 8 critical technology areas. Phase 1 design specifies 3 concrete artifacts.
- 📁 Files: Created 1 file: specs/003-frontend-ui/plan.md (770 lines) with complete architectural plan including technical context, constitution check, project structure, research tasks, design specifications, implementation phases, dependencies, validation checkpoints, risk mitigation, and success criteria mapping.
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed task breakdown with specific file paths, acceptance criteria, and dependencies. After tasks.md complete, execute `/sp.implement` to begin frontend development.
- 🧠 Reflection: Plan successfully bridges specification (what to build) with implementation (how to build it). All 71 functional requirements from spec.md mapped to implementation phases. Technical decisions documented with clear rationale. Phase 0 research addresses all unknowns before coding begins. Phase 1 design creates concrete artifacts (data-model.md, contracts/, quickstart.md) that guide implementation. Constitutional compliance ensures security, quality, and architectural integrity. 13-phase implementation structure provides clear roadmap from empty frontend/ directory to production-ready application. Risk mitigation addresses all high-impact concerns proactively.

## Evaluation notes (flywheel)

- Failure modes observed: None. Planning workflow completed successfully with all gates passed.
- Graders run and results (PASS/FAIL): Constitution Check - ALL PASS (6/6 principles). Technical Context - COMPLETE (0 unresolved). Phase definitions - COMPREHENSIVE (Phase 0: 8 tasks, Phase 1: 3 artifacts, Phases 1-13: implementation roadmap).
- Prompt variant (if applicable): N/A (standard /sp.plan workflow)
- Next experiment (smallest change to try): Consider adding explicit performance budgets (bundle size limits, FCP targets) as measurable outputs in Phase 1 design for future frontend plans. Consider documenting API payload size expectations in contracts/ to catch performance issues early.
