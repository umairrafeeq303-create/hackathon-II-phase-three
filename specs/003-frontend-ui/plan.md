# Implementation Plan: Frontend UI & API Integration

**Branch**: `003-frontend-ui` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-frontend-ui/spec.md`

## Summary

This plan implements the Next.js 16 frontend application with Better Auth integration and complete UI for task management. The frontend consumes authentication APIs (Spec 1) and task CRUD APIs (Spec 2) to provide an intuitive, responsive interface for users to manage their personal tasks.

**Primary Requirement**: Create a production-ready Next.js frontend with TypeScript, Tailwind CSS, and Better Auth that enables users to signup, login, view their task dashboard, and perform all CRUD operations on tasks with proper authentication, error handling, and responsive design.

**Technical Approach**: Use Next.js 16 App Router for routing and pages, Better Auth with JWT plugin for authentication state management, centralized API client with JWT token interceptors for backend communication, Tailwind CSS for mobile-first responsive styling, and React hooks for state management within components.

## Technical Context

**Language/Version**: TypeScript 5.3+ with Next.js 16+ (React 19)
**Primary Dependencies**: Next.js 16, Better Auth 1.0, Tailwind CSS 3.4, React 19
**Storage**: Browser localStorage for JWT tokens, API calls to backend for all data persistence
**Testing**: Manual integration testing via user flows (automated testing out of scope for MVP)
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
**Project Type**: Web frontend (integrates with existing FastAPI backend)
**Performance Goals**:
- Initial page load < 2 seconds on broadband
- Task list render < 1 second
- User interactions respond within 100ms
- Filter/sort operations complete < 500ms
**Constraints**:
- Must integrate with existing backend API at `NEXT_PUBLIC_API_URL`
- JWT tokens from Better Auth must match backend validation
- BETTER_AUTH_SECRET must match backend configuration
- Mobile-first responsive design (>= 375px width)
- No server-side rendering optimization (client-side rendering acceptable for MVP)
**Scale/Scope**:
- 9 user stories (6 P1, 3 P2)
- 71 functional requirements
- 5 pages (/, /login, /signup, /api/auth/[...all])
- ~15-20 React components
- Single API client module
- 1 authentication provider
- Estimated 2000-3000 lines of TypeScript

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅ PASS
- All implementation via `/sp.implement` workflow
- Following spec.md → plan.md → tasks.md → implementation sequence
- No manual code editing permitted

### Principle II: Security-First Architecture ✅ PASS
- Better Auth with JWT plugin for authentication
- JWT tokens stored in localStorage with XSS protection via CSP headers
- Authorization header (`Bearer {token}`) on all API requests
- Protected routes redirect unauthenticated users to login
- User ID extracted from JWT token for API URL construction
- 401 responses trigger token clear and login redirect

### Principle III: Complete Separation of Concerns ✅ PASS
- Frontend (Next.js) operates independently from backend (FastAPI)
- All communication via REST API endpoints
- No direct database access from frontend
- API client abstraction layer for all backend calls
- Can run `npm run dev` independently (with backend URL configured)

### Principle IV: User Data Isolation and Ownership ✅ PASS
- User ID from JWT token used in all API URLs (`/api/{user_id}/tasks`)
- Frontend enforces client-side checks before API calls
- Backend validation ensures user can only access own tasks (403 on mismatch)
- No cross-user data displayed in UI

### Principle V: Production-Ready Code Quality ✅ PASS
- TypeScript with strict mode enabled
- All API error responses explicitly handled (400, 401, 403, 404, 422, 500)
- Environment variables for configuration (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET)
- No hardcoded secrets in codebase
- All async operations have loading states
- All user actions have success/error feedback

### Principle VI: RESTful API Design with JWT Authentication ✅ PASS
- Consumes existing backend REST API endpoints
- JWT token attached to all authenticated requests
- CORS handled by backend configuration
- JSON request/response format

### Technology Stack Standards ✅ PASS
- **Frontend**: Next.js 16+ App Router ✓, TypeScript strict mode ✓, Tailwind CSS ✓, Better Auth ✓
- **Deployment**: Vercel (planned)
- **Shared Config**: BETTER_AUTH_SECRET matches backend ✓

**Gate Status**: ✅ ALL GATES PASSED - Proceeding to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/003-frontend-ui/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology research)
├── data-model.md        # Phase 1 output (TypeScript types)
├── quickstart.md        # Phase 1 output (dev setup guide)
├── contracts/           # Phase 1 output (API client interface)
│   └── api-client.ts    # TypeScript interface definitions for API
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── layout.tsx            # Root layout with Header
│   │   ├── page.tsx              # Dashboard (protected route)
│   │   ├── login/
│   │   │   └── page.tsx          # Login page
│   │   ├── signup/
│   │   │   └── page.tsx          # Signup page
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/
│   │               └── route.ts  # Better Auth API handler
│   ├── components/               # React components
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx     # Login form with validation
│   │   │   ├── SignupForm.tsx    # Signup form with validation
│   │   │   └── ProtectedRoute.tsx # Auth guard wrapper
│   │   ├── layout/
│   │   │   ├── Header.tsx        # App header with user name + logout
│   │   │   └── Navigation.tsx    # Navigation (if needed)
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx      # List container with loading/empty states
│   │   │   ├── TaskItem.tsx      # Single task display with actions
│   │   │   ├── TaskForm.tsx      # Create/edit form (dual mode)
│   │   │   ├── TaskFilters.tsx   # Status + sort dropdowns
│   │   │   └── DeleteConfirmation.tsx # Delete modal
│   │   └── ui/
│   │       ├── Button.tsx        # Reusable button component
│   │       ├── Input.tsx         # Reusable input component
│   │       ├── Textarea.tsx      # Reusable textarea component
│   │       ├── Modal.tsx         # Reusable modal component
│   │       ├── Spinner.tsx       # Loading spinner
│   │       └── Toast.tsx         # Success/error toast messages
│   ├── lib/
│   │   ├── api.ts                # Centralized API client
│   │   ├── auth.ts               # Better Auth configuration
│   │   └── utils.ts              # Utility functions (token extraction, etc.)
│   ├── types/
│   │   └── index.ts              # TypeScript type definitions
│   └── styles/
│       └── globals.css           # Tailwind imports + global styles
├── public/                       # Static assets (favicon, etc.)
├── .env.local                    # Environment variables (not committed)
├── .env.example                  # Environment variable template
├── next.config.js                # Next.js configuration
├── tailwind.config.js            # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json                  # Dependencies and scripts

backend/ (unchanged - reference only for API integration)
└── src/
    ├── api/
    │   ├── auth.py               # Spec 1: /api/auth/signup, /api/auth/signin
    │   └── routes/
    │       └── tasks.py          # Spec 2: /api/{user_id}/tasks endpoints
    └── models/
        ├── user.py               # User model
        └── task.py               # Task model
```

**Structure Decision**: Web application structure (Option 2 from template) with independent `frontend/` and `backend/` directories. Frontend uses Next.js App Router convention with `src/app/` for pages and `src/components/` for reusable components. API client centralized in `src/lib/api.ts` for all backend communication. TypeScript types in `src/types/` for type safety across application.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - all constitutional principles are satisfied.

---

## Phase 0: Research & Technology Verification

**Goal**: Verify all technology choices, resolve unknowns, and establish best practices for Next.js 16 + Better Auth + TypeScript + Tailwind CSS integration.

### Research Tasks

1. **Better Auth with Next.js 16 Integration**
   - Research: Better Auth 1.0 setup with Next.js 16 App Router
   - Focus: API route handler configuration, client hooks usage, JWT plugin setup
   - Output: Configuration pattern for `src/lib/auth.ts` and `src/app/api/auth/[...all]/route.ts`

2. **JWT Token Management Best Practices**
   - Research: localStorage vs cookies for JWT storage, token extraction from Better Auth, XSS protection strategies
   - Focus: How to extract user ID from JWT token, how to attach token to fetch requests
   - Output: Token storage decision and extraction utility functions

3. **Next.js 16 App Router Patterns**
   - Research: Protected route implementation, client vs server components, loading states, error handling
   - Focus: Authentication guards, redirect patterns, metadata configuration
   - Output: ProtectedRoute wrapper pattern and page structure

4. **Tailwind CSS Responsive Design**
   - Research: Mobile-first breakpoints, form styling, button states, modal patterns
   - Focus: Breakpoints (sm: 640px, md: 768px, lg: 1024px), component variants
   - Output: Tailwind configuration and utility class patterns

5. **TypeScript API Client Pattern**
   - Research: Centralized fetch wrapper, request/response typing, error handling, interceptors
   - Focus: How to create typed API methods, how to handle 401 globally
   - Output: API client architecture with TypeScript interfaces

6. **Form Validation Strategies**
   - Research: Client-side validation patterns, real-time feedback, error display
   - Focus: Email/password validation, character limits, required fields
   - Output: Validation utility functions and error state management

7. **State Management for Task List**
   - Research: React hooks (useState, useEffect), optimistic updates, error rollback
   - Focus: Task list state, filter state, loading state, CRUD operation handling
   - Output: State management pattern (no external library needed)

8. **Loading and Error States**
   - Research: Skeleton loaders, spinner patterns, toast notifications, error boundaries
   - Focus: UX patterns for async operations
   - Output: Loading component library and error handling utilities

**Output**: `research.md` with all decisions documented including rationale, alternatives considered, and recommended patterns

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete

### 1. Data Model (`data-model.md`)

Extract TypeScript types from spec.md functional requirements:

**User Entity**:
```typescript
interface User {
  id: string;          // UUID from JWT token
  email: string;
  name: string;
}
```

**Task Entity**:
```typescript
interface Task {
  id: number;
  user_id: string;     // UUID
  title: string;       // max 200 characters
  description: string | null;  // max 1000 characters
  completed: boolean;
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
}
```

**Task Filter State**:
```typescript
interface TaskFilters {
  status: 'all' | 'pending' | 'completed';
  sort: 'created' | 'title';
  order: 'asc' | 'desc';
}
```

**Form Data Types**:
```typescript
interface SignupFormData {
  name: string;
  email: string;
  password: string;
}

interface LoginFormData {
  email: string;
  password: string;
}

interface TaskCreateData {
  title: string;
  description?: string;
}

interface TaskUpdateData {
  title?: string;
  description?: string;
}
```

**API Response Types**:
```typescript
interface ApiSuccessResponse<T> {
  data: T;
}

interface ApiErrorResponse {
  detail: string;
}
```

**Validation Rules** (from spec requirements):
- Email: must contain @ and domain
- Password: minimum 8 characters
- Task title: required, max 200 characters
- Task description: optional, max 1000 characters

**State Transitions**:
- Task: pending ↔ completed (toggle operation)
- User session: unauthenticated → authenticated → unauthenticated

### 2. API Contracts (`contracts/api-client.ts`)

Generate TypeScript interface for API client from Spec 1 & 2 endpoints:

```typescript
// Authentication endpoints (Spec 1)
interface AuthAPI {
  /**
   * POST /api/auth/signup
   * Creates new user account
   * Returns: { token: string, user: { id: string, email: string, name: string } }
   */
  signup(data: SignupFormData): Promise<{ token: string; user: User }>;

  /**
   * POST /api/auth/signin
   * Authenticates existing user
   * Returns: { token: string, user: { id: string, email: string, name: string } }
   */
  signin(data: LoginFormData): Promise<{ token: string; user: User }>;
}

// Task endpoints (Spec 2)
interface TaskAPI {
  /**
   * GET /api/{user_id}/tasks?status={status}&sort={sort}&order={order}
   * Fetches all user's tasks with optional filtering and sorting
   * Returns: Task[]
   */
  getTasks(userId: string, filters?: Partial<TaskFilters>): Promise<Task[]>;

  /**
   * GET /api/{user_id}/tasks/{task_id}
   * Fetches single task by ID
   * Returns: Task
   */
  getTask(userId: string, taskId: number): Promise<Task>;

  /**
   * POST /api/{user_id}/tasks
   * Creates new task
   * Returns: Task
   */
  createTask(userId: string, data: TaskCreateData): Promise<Task>;

  /**
   * PUT /api/{user_id}/tasks/{task_id}
   * Updates existing task
   * Returns: Task
   */
  updateTask(userId: string, taskId: number, data: TaskUpdateData): Promise<Task>;

  /**
   * DELETE /api/{user_id}/tasks/{task_id}
   * Deletes task
   * Returns: { message: string }
   */
  deleteTask(userId: string, taskId: number): Promise<{ message: string }>;

  /**
   * PATCH /api/{user_id}/tasks/{task_id}/toggle
   * Toggles task completion status
   * Returns: Task
   */
  toggleTask(userId: string, taskId: number): Promise<Task>;
}

// Combined API client interface
interface APIClient extends AuthAPI, TaskAPI {
  /**
   * Sets JWT token for authenticated requests
   */
  setToken(token: string): void;

  /**
   * Clears JWT token (logout)
   */
  clearToken(): void;

  /**
   * Gets current JWT token
   */
  getToken(): string | null;
}
```

**Error Handling Contract**:
```typescript
interface APIError extends Error {
  status: number;       // HTTP status code
  message: string;      // User-friendly error message
  detail?: string;      // Technical error details
}

// Expected status codes and handling:
// 200/201: Success
// 400: Bad request (invalid input format)
// 401: Unauthorized (clear token, redirect to login)
// 403: Forbidden (accessing other user's data)
// 404: Not found (task doesn't exist)
// 422: Validation error (field-specific errors)
// 500: Server error (show generic error message)
```

### 3. Development Quickstart (`quickstart.md`)

```markdown
# Frontend Development Quickstart

## Prerequisites
- Node.js 18+ and npm
- Backend API running at configured URL (default: http://localhost:8000)
- Backend environment variable BETTER_AUTH_SECRET must match frontend

## Environment Setup

1. Copy environment template:
   ```bash
   cp .env.example .env.local
   ```

2. Configure variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=<same-as-backend-secret>
   ```

## Installation

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

Application available at: http://localhost:3000

## Build

```bash
npm run build
npm start
```

## Type Checking

```bash
npm run type-check
```

## Project Structure

- `src/app/`: Next.js pages (App Router)
- `src/components/`: Reusable React components
- `src/lib/`: Utilities (API client, auth config)
- `src/types/`: TypeScript type definitions
- `src/styles/`: Global styles and Tailwind imports

## Key Files

- `src/lib/api.ts`: API client for all backend communication
- `src/lib/auth.ts`: Better Auth configuration
- `src/app/api/auth/[...all]/route.ts`: Better Auth API handler
- `src/components/auth/ProtectedRoute.tsx`: Authentication guard

## Development Flow

1. Start backend server (port 8000)
2. Start frontend dev server (port 3000)
3. Access http://localhost:3000
4. Create account at /signup
5. Login and manage tasks

## Testing User Flows

1. **Signup Flow**: /signup → fill form → submit → redirected to dashboard
2. **Login Flow**: /login → enter credentials → submit → redirected to dashboard
3. **Task Management**: dashboard → create task → toggle completion → edit → delete
4. **Filtering**: dashboard → filter by status → sort by title/date
5. **Logout**: click logout button → redirected to /login

## Common Issues

- **401 errors**: Check BETTER_AUTH_SECRET matches backend
- **CORS errors**: Verify backend CORS_ORIGINS includes http://localhost:3000
- **Connection refused**: Ensure backend is running on port 8000
- **Type errors**: Run `npm run type-check` to identify issues
```

### 4. Agent Context Update

Run agent context update script:
```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This updates `CLAUDE.md` to include:
- Next.js 16 App Router patterns
- Better Auth integration approach
- TypeScript API client pattern
- Tailwind CSS responsive design guidelines

**Output**:
- `data-model.md`: Complete TypeScript type definitions
- `contracts/api-client.ts`: Typed API client interface
- `quickstart.md`: Developer setup and testing guide
- `CLAUDE.md`: Updated with frontend-specific patterns

---

## Re-evaluation of Constitution Check

*Execute after Phase 1 design is complete*

### Principle I: Spec-Driven Development ✅ PASS
- Design follows specification requirements exactly
- All 71 functional requirements mapped to implementation components
- No deviations from spec.md

### Principle II: Security-First Architecture ✅ PASS
- JWT token management clearly defined in contracts
- Protected route pattern established
- 401 handling redirects to login
- User ID validation enforced

### Principle III: Complete Separation of Concerns ✅ PASS
- API client abstraction isolates backend communication
- No direct database references
- Frontend can run independently with mock API

### Principle IV: User Data Isolation and Ownership ✅ PASS
- User ID from JWT token used in all API calls
- No cross-user data access patterns
- Backend enforces final validation

### Principle V: Production-Ready Code Quality ✅ PASS
- TypeScript types defined for all data structures
- Error handling patterns documented
- Environment variables for all configuration
- Loading states designed for all async operations

### Principle VI: RESTful API Design with JWT Authentication ✅ PASS
- API contracts match backend REST endpoints
- JWT token handling standardized
- JSON request/response format

**Final Gate Status**: ✅ ALL GATES PASSED - Ready for Phase 2 (/sp.tasks)

---

## Implementation Phases Overview (for `/sp.tasks` reference)

### Phase Structure for Task Generation

When `/sp.tasks` is executed, it should generate tasks organized by the user story priorities defined in spec.md:

**Phase 1: Project Setup**
- Initialize Next.js project structure (if not done)
- Install and configure dependencies
- Setup environment variables
- Configure TypeScript and Tailwind CSS

**Phase 2: Foundation (Shared Infrastructure)**
- Create TypeScript types (from data-model.md)
- Create API client (from contracts/api-client.ts)
- Create utility functions (token management, validation)
- Setup Better Auth configuration

**Phase 3: Authentication UI (US1 & US2 - P1)**
- Create signup page and form
- Create login page and form
- Implement form validation
- Integrate with Better Auth
- Test auth flows

**Phase 4: Protected Routes & Layout (US3 - P1)**
- Create ProtectedRoute wrapper
- Create Header component
- Create dashboard page layout
- Implement authentication checks

**Phase 5: Task Display (US3 - P1)**
- Create TaskList component
- Create TaskItem component
- Implement empty states
- Implement loading states
- Connect to API for task fetching

**Phase 6: Task Creation (US4 - P1)**
- Create TaskForm component (create mode)
- Implement validation
- Connect to create API endpoint
- Add success feedback

**Phase 7: Task Completion Toggle (US5 - P1)**
- Implement checkbox functionality
- Connect to toggle API endpoint
- Add loading states
- Implement error rollback

**Phase 8: Task Filtering and Sorting (US6 - P1)**
- Create TaskFilters component
- Implement status filter
- Implement sort options
- Connect to filtered API calls

**Phase 9: Task Editing (US7 - P2)**
- Add edit mode to TaskForm
- Pre-populate form data
- Connect to update API endpoint
- Add success feedback

**Phase 10: Task Deletion (US8 - P2)**
- Create DeleteConfirmation component
- Connect to delete API endpoint
- Implement confirmation flow
- Add animation for removal

**Phase 11: Logout (US9 - P2)**
- Implement logout functionality
- Clear token and session
- Redirect to login

**Phase 12: Responsive Design & Polish**
- Apply mobile-first responsive styles
- Test on multiple screen sizes
- Add final UI polish
- Cross-browser testing

**Phase 13: Integration Testing & Documentation**
- Test complete user flows
- Verify all acceptance scenarios from spec.md
- Update documentation
- Final validation

---

## Dependencies and Sequencing

### Critical Path (must be sequential):
1. Phase 1 (Setup) → Phase 2 (Foundation) → All other phases
2. Phase 2 (API Client, Types) → All phases that use API
3. Phase 3 (Authentication) → Phase 4 (Protected Routes) → Phase 5+ (All protected features)

### Parallelizable Work:
- After Phase 4 complete: Phases 5-11 can proceed in parallel if multiple developers
- UI components (TaskList, TaskItem, TaskForm, TaskFilters) can be developed simultaneously
- Phase 12 (Responsive Design) can run in parallel with Phases 9-11

### File Coordination (sequential within same file):
- `src/lib/api.ts`: All API methods must be added sequentially
- `src/types/index.ts`: Types can be added incrementally
- `src/app/page.tsx`: Dashboard must be built incrementally

---

## Validation Checkpoints

After each phase in `/sp.implement`, verify:
- ✅ All tasks in phase marked complete
- ✅ Dev server runs without TypeScript errors
- ✅ UI renders correctly in browser
- ✅ Manual test of new features passes
- ✅ API integration works (check network tab)
- ✅ Authentication state persists across refreshes
- ✅ No console errors in browser dev tools

---

## Architectural Decisions Requiring ADRs

During implementation, if the following decisions arise, create ADRs via `/sp.adr`:

1. **State Management Library Addition** (if React hooks prove insufficient)
   - Decision: Add Zustand/Redux or stay with hooks
   - Impact: Long-term maintainability
   - Justification required: Why hooks insufficient

2. **Token Storage Change** (if localStorage proves problematic)
   - Decision: Switch to httpOnly cookies
   - Impact: Better Auth configuration change
   - Justification required: Security vs convenience trade-off

3. **Real-time Updates** (if multi-tab synchronization required)
   - Decision: Add WebSocket connection
   - Impact: Backend changes needed
   - Justification required: Is eventual consistency acceptable?

4. **CSS Framework Addition** (if Tailwind proves limiting)
   - Decision: Add shadcn/ui or Headless UI
   - Impact: Bundle size increase
   - Justification required: Why Tailwind utilities insufficient?

---

## Success Criteria Mapping

How this plan achieves each success criterion from spec.md:

- **SC-001** (Signup in <60s): Phases 3 (auth UI) + validation patterns
- **SC-002** (Dashboard loads <1s): Phase 5 (optimized task display) + API client caching
- **SC-003** (Feedback <100ms): Phase 2 (loading states) + all CRUD phases
- **SC-004** (Responsive 375px-2560px): Phase 12 (responsive design) with Tailwind breakpoints
- **SC-005** (95% API success): Phase 2 (error handling) applied to all API calls
- **SC-006** (CRUD confirms <2s): Phases 6-11 (all CRUD operations) with success toasts
- **SC-007** (Zero unauthorized access): Phase 4 (protected routes) + API client user_id validation
- **SC-008** (Core actions without errors): All phases with comprehensive error handling
- **SC-009** (Session persistence): Phase 2 (token management) + Phase 4 (auth checks)
- **SC-010** (Loading states for all async): Phase 2 (loading components) used throughout

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Better Auth integration complexity | High | Phase 0 research task #1 validates integration pattern |
| JWT token expiry during active session | Medium | Phase 2 implements 401 interceptor for automatic redirect |
| TypeScript type mismatches with backend | High | Phase 1 contracts generated from Spec 1 & 2 documentation |
| CORS issues in development | Medium | Documented in quickstart.md with backend configuration steps |
| Responsive design breakage | Medium | Phase 12 dedicated testing on multiple devices/screen sizes |
| Form validation inconsistency | Medium | Phase 2 creates reusable validation utilities |
| State management complexity | Medium | Start with React hooks; ADR process if state library needed |

---

## Notes for `/sp.tasks` Command

When generating tasks.md from this plan:

1. **Task Granularity**: Each task should be 15-30 minutes of focused work
2. **Testability**: Each task must have clear acceptance criteria from spec.md
3. **Dependencies**: Mark tasks that must wait for others (e.g., "AFTER T042")
4. **User Story Mapping**: Tag each task with user story ID (e.g., "[US1]", "[US2]")
5. **Priority Inheritance**: Tasks for P1 user stories are P1, tasks for P2 user stories are P2
6. **File References**: Include absolute file paths for all file creation/modification tasks
7. **API Integration Points**: Highlight tasks that require backend running
8. **Validation Tasks**: Include explicit testing tasks after each phase

---

**Plan Status**: ✅ COMPLETE - Ready for `/sp.tasks` command execution

**Next Steps**:
1. Run `/sp.tasks` to generate actionable task breakdown
2. Review tasks.md for completeness
3. Execute `/sp.implement` to begin implementation
4. Follow validation checkpoints after each phase
5. Create ADRs for any architectural decisions during implementation
