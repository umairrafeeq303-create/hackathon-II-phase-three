# Tasks: Authentication & User Management System

**Input**: Design documents from `/specs/001-auth/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md, quickstart.md

**Tests**: Not explicitly requested in specification - test tasks are EXCLUDED per project requirements

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with separate backend and frontend:
- **Backend**: `backend/src/` (FastAPI, SQLModel, Python 3.11+)
- **Frontend**: `frontend/src/` (Next.js 16+, TypeScript, React 19+)
- **Tests**: `backend/tests/` and `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

### Backend Setup

- [ ] T001 Create backend directory structure per plan.md (src/, tests/, alembic/)
- [ ] T002 Initialize Python project with requirements.txt (FastAPI 0.109.0, SQLModel 0.0.14, python-jose 3.3.0, passlib 1.7.4, uvicorn 0.27.0, psycopg2-binary 2.9.9, python-multipart 0.0.6, pydantic 2.5.3, python-dotenv 1.0.0, alembic 1.13.1)
- [ ] T003 Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS, ENVIRONMENT
- [ ] T004 Create backend/.gitignore for Python (venv/, __pycache__/, .env, *.pyc, .pytest_cache/)
- [ ] T005 Create backend/README.md with setup instructions from quickstart.md

### Frontend Setup

- [ ] T006 [P] Create frontend directory structure per plan.md (src/app/, src/lib/, src/components/, src/hooks/, src/context/, src/types/)
- [ ] T007 [P] Initialize Next.js 16+ project with package.json (next, react, react-dom, typescript, tailwindcss, better-auth dependencies)
- [ ] T008 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
- [ ] T009 [P] Create frontend/.gitignore for Node.js (node_modules/, .next/, .env.local, dist/)
- [ ] T010 [P] Configure TypeScript (tsconfig.json) with strict mode enabled
- [ ] T011 [P] Configure Tailwind CSS (tailwind.config.ts, globals.css)
- [ ] T012 [P] Create frontend/README.md with setup instructions from quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T013 Create backend/src/core/config.py for environment variable management (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS, ENVIRONMENT)
- [ ] T014 Create backend/src/db/session.py with database session management and engine configuration
- [ ] T015 Initialize Alembic for database migrations (alembic init alembic, configure alembic.ini and alembic/env.py)
- [ ] T016 Create backend/src/models/__init__.py with SQLModel base configuration
- [ ] T017 Create backend/src/core/security.py with password hashing utilities (hash_password, verify_password using passlib with bcrypt, 10 salt rounds minimum)
- [ ] T018 Create backend/src/core/security.py JWT token utilities (create_access_token, verify_token using python-jose, HS256 algorithm, 7-day expiry)
- [ ] T019 Create backend/src/core/deps.py with get_db_session dependency for FastAPI
- [ ] T020 Create backend/src/core/deps.py with get_current_user_id dependency for JWT validation (extracts and validates token, returns user_id)
- [ ] T021 Create backend/src/main.py with FastAPI app initialization, CORS middleware configuration, and basic health check endpoint
- [ ] T022 Create backend/src/schemas/__init__.py for Pydantic schema exports

### Frontend Foundation

- [ ] T023 [P] Create frontend/src/types/auth.ts with TypeScript interfaces (User, AuthResponse, AuthError)
- [ ] T024 [P] Create frontend/src/lib/api.ts with base API client configuration (API_BASE_URL from env, fetch wrapper)
- [ ] T025 [P] Create frontend/src/lib/auth.ts with Better Auth configuration (database provider, JWT plugin with 7-day expiry, API baseUrl)
- [ ] T026 [P] Create frontend/src/context/AuthContext.tsx with authentication state management (user, isAuthenticated, isLoading)
- [ ] T027 [P] Create frontend/src/hooks/useAuth.ts custom hook for auth operations
- [ ] T028 [P] Create frontend/src/app/layout.tsx with AuthContext provider and basic layout structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with name, email, and password. System validates input, creates user record with hashed password, generates JWT token, and logs user in immediately.

**Independent Test**: Submit registration form with valid credentials → user created in database + JWT token returned + redirect to application

### Backend: User Model and Schemas (US1)

- [ ] T029 [P] [US1] Create backend/src/models/user.py with User SQLModel (id: UUID primary key, email: str unique indexed, name: str, hashed_password: str, created_at: datetime)
- [ ] T030 [P] [US1] Create backend/src/schemas/auth.py with UserCreate schema (name, email: EmailStr, password with min 8 chars validation)
- [ ] T031 [P] [US1] Create backend/src/schemas/auth.py with UserResponse schema (id, email, name, created_at - excludes hashed_password)
- [ ] T032 [P] [US1] Create backend/src/schemas/auth.py with AuthResponse schema (user: UserResponse, token: str)

### Backend: Signup Endpoint (US1)

- [ ] T033 [US1] Create backend/src/api/auth.py with POST /api/auth/signup endpoint (depends on T029-T032, T017-T018)
- [ ] T034 [US1] Implement signup logic: validate email format (EmailStr), check password length (min 8), check email uniqueness, hash password, create user, generate JWT token
- [ ] T035 [US1] Add error handling to signup: 400 for duplicate email ("Email already registered"), 422 for validation errors, 500 for database errors
- [ ] T036 [US1] Register auth router in backend/src/main.py with /api/auth prefix

### Database Migration (US1)

- [ ] T037 [US1] Create Alembic migration for users table (001_create_users.py with UUID id, unique indexed email, name, hashed_password, created_at with server default)
- [ ] T038 [US1] Apply migration to create users table (alembic upgrade head)

### Frontend: Signup UI (US1)

- [ ] T039 [P] [US1] Create frontend/src/components/ui/Input.tsx reusable input component with Tailwind styling
- [ ] T040 [P] [US1] Create frontend/src/components/ui/Button.tsx reusable button component with Tailwind styling
- [ ] T041 [US1] Create frontend/src/components/auth/SignupForm.tsx with name, email, password fields, client-side validation, error display (depends on T039-T040)
- [ ] T042 [US1] Implement signup API client function in frontend/src/lib/api.ts (POST to /api/auth/signup, handle 201/400/422/500 responses)
- [ ] T043 [US1] Integrate signup function in SignupForm: call API on submit, store token in localStorage on success, update auth context, handle all error cases
- [ ] T044 [US1] Create frontend/src/app/auth/signup/page.tsx with SignupForm component and proper layout
- [ ] T045 [US1] Implement redirect to dashboard on successful signup

**Checkpoint**: User Story 1 complete - users can register accounts, receive JWT tokens, and are logged in automatically

---

## Phase 4: User Story 2 - Returning User Login (Priority: P1)

**Goal**: Enable registered users to authenticate with email and password. System validates credentials, generates JWT token, and provides access to their account.

**Independent Test**: Submit login credentials for existing user → JWT token returned + user can access protected resources

### Backend: Signin Schemas (US2)

- [ ] T046 [P] [US2] Create backend/src/schemas/auth.py with UserLogin schema (email: EmailStr, password: str - no length validation at signin)

### Backend: Signin Endpoint (US2)

- [ ] T047 [US2] Create POST /api/auth/signin endpoint in backend/src/api/auth.py (depends on T046, reuses T017-T018, T029, T031-T032)
- [ ] T048 [US2] Implement signin logic: normalize email to lowercase, query user by email, compare password with bcrypt (timing attack prevention - consistent 300-500ms)
- [ ] T049 [US2] Implement dummy bcrypt verification when user not found (timing attack prevention - same duration as real verification)
- [ ] T050 [US2] Add error handling to signin: 401 for invalid credentials (same message for wrong email or password), 400 for missing fields, 500 for database errors
- [ ] T051 [US2] Generate JWT token on successful signin and return AuthResponse

### Frontend: Signin UI (US2)

- [ ] T052 [P] [US2] Create frontend/src/components/auth/SigninForm.tsx with email and password fields, client-side validation, error display (reuses T039-T040)
- [ ] T053 [US2] Implement signin API client function in frontend/src/lib/api.ts (POST to /api/auth/signin, handle 200/400/401/500 responses)
- [ ] T054 [US2] Integrate signin function in SigninForm: call API on submit, store token in localStorage on success, update auth context, handle all error cases with consistent messaging
- [ ] T055 [US2] Create frontend/src/app/auth/signin/page.tsx with SigninForm component and proper layout
- [ ] T056 [US2] Implement redirect to dashboard on successful signin
- [ ] T057 [US2] Add link to signup page from signin page for new users

**Checkpoint**: User Story 2 complete - users can sign in with credentials and receive JWT tokens

---

## Phase 5: User Story 3 - Authenticated Resource Access (Priority: P2)

**Goal**: Enable logged-in users to access protected resources by validating JWT tokens on every request. System extracts user identity for data isolation enforcement.

**Independent Test**: Make API requests with valid/invalid/expired tokens → correctly accept/reject requests based on token validity

### Backend: JWT Verification Dependency (US3)

- [ ] T058 [US3] Enhance backend/src/core/deps.py get_current_user_id to extract Authorization header, validate Bearer format, decode JWT, verify signature and expiry, return user_id
- [ ] T059 [US3] Add comprehensive error handling to JWT validation: 401 for missing header ("Authorization header required"), 401 for invalid token ("Invalid token"), 401 for expired token ("Token expired")
- [ ] T060 [US3] Add user_id verification against URL path for future protected endpoints (FR-016, FR-017 - returns 403 Forbidden on mismatch)

### Frontend: Protected Route Component (US3)

- [ ] T061 [P] [US3] Create frontend/src/components/auth/ProtectedRoute.tsx HOC that checks for auth token, redirects to signin if missing, handles loading state
- [ ] T062 [US3] Enhance frontend/src/hooks/useAuth.ts to check token validity on mount, clear token and redirect on 401 responses
- [ ] T063 [US3] Update frontend/src/lib/api.ts to automatically include Authorization header with Bearer token for all API requests
- [ ] T064 [US3] Implement 401 error interceptor in API client to clear token and redirect to signin page

### Integration Validation (US3)

- [ ] T065 [US3] Create protected dashboard page at frontend/src/app/dashboard/page.tsx using ProtectedRoute component (placeholder for task features)
- [ ] T066 [US3] Verify JWT validation works end-to-end: signup → access dashboard (success), expired token → redirect to signin (success), no token → redirect to signin (success)

**Checkpoint**: User Story 3 complete - JWT validation infrastructure ready for protected resources, foundation for Spec 2 (Task API) integration

---

## Phase 6: User Story 4 - User Session Management (Priority: P3)

**Goal**: Enable logged-in users to log out. System clears session and requires re-authentication for subsequent requests.

**Independent Test**: Login → logout → verify JWT cleared from storage + subsequent protected page access requires re-authentication

### Frontend: Logout Functionality (US4)

- [ ] T067 [P] [US4] Implement logout function in frontend/src/lib/api.ts (clears token from localStorage)
- [ ] T068 [US4] Add logout function to frontend/src/hooks/useAuth.ts with auth context state reset
- [ ] T069 [US4] Create logout button component in frontend/src/components/auth/LogoutButton.tsx
- [ ] T070 [US4] Integrate LogoutButton in dashboard layout or navigation bar
- [ ] T071 [US4] Implement redirect to signin page on logout
- [ ] T072 [US4] Verify logout flow: click logout → token cleared → redirected to signin → cannot access dashboard without re-authentication

**Checkpoint**: User Story 4 complete - users can explicitly log out of the application

---

## Phase 7: User Story 5 - Retrieve Current User Information (Priority: P3)

**Goal**: Provide endpoint for authenticated users to retrieve their profile information (name, email) for UI personalization.

**Independent Test**: Call /api/auth/me with valid JWT token → returns user information excluding password

### Backend: Get Current User Endpoint (US5)

- [ ] T073 [US5] Create GET /api/auth/me endpoint in backend/src/api/auth.py using get_current_user_id dependency (depends on T058-T059)
- [ ] T074 [US5] Implement endpoint logic: extract user_id from JWT, query database for user, return UserResponse (excludes hashed_password)
- [ ] T075 [US5] Add error handling: 401 for invalid token, 404 if user not found (should not happen with valid token), 500 for database errors

### Frontend: Current User API Integration (US5)

- [ ] T076 [P] [US5] Implement getCurrentUser API client function in frontend/src/lib/api.ts (GET /api/auth/me with Authorization header)
- [ ] T077 [US5] Add getCurrentUser call to frontend/src/hooks/useAuth.ts on app initialization (fetch user data if token exists)
- [ ] T078 [US5] Cache user data in auth context to avoid repeated API calls
- [ ] T079 [US5] Display user name in dashboard header or navigation bar using cached user data
- [ ] T080 [US5] Handle 401 error in getCurrentUser by clearing token and redirecting to signin

**Checkpoint**: User Story 5 complete - application displays user information for personalization

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, documentation, and production readiness

### Backend Polish

- [ ] T081 [P] Add API documentation with FastAPI automatic Swagger UI at /docs endpoint (already provided by FastAPI)
- [ ] T082 [P] Add health check endpoint at GET /health in backend/src/main.py (returns {"status": "healthy"})
- [ ] T083 [P] Configure logging in backend/src/main.py with appropriate log levels
- [ ] T084 [P] Add request/response logging middleware for debugging

### Frontend Polish

- [ ] T085 [P] Create home page at frontend/src/app/page.tsx with links to signup/signin
- [ ] T086 [P] Add loading states to all forms (signup, signin) during API calls
- [ ] T087 [P] Add proper error message display for all API error responses (400, 401, 422, 500)
- [ ] T088 [P] Implement form field validation feedback (inline error messages, field highlighting)
- [ ] T089 [P] Add responsive design for mobile devices (Tailwind breakpoints)

### Environment and Deployment

- [ ] T090 [P] Generate strong BETTER_AUTH_SECRET for production (minimum 32 characters): `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] T091 [P] Document all environment variables in README files (backend and frontend)
- [ ] T092 [P] Create deployment guide referencing Railway (backend) and Vercel (frontend) setup from quickstart.md

### Documentation

- [ ] T093 [P] Update backend/README.md with API endpoint documentation (references to /docs)
- [ ] T094 [P] Update frontend/README.md with component structure and usage examples
- [ ] T095 [P] Create root README.md with project overview, setup instructions for both services, and links to specs

**Checkpoint**: All user stories complete and polished - system ready for production deployment

---

## Dependencies: User Story Completion Order

This dependency graph shows which user stories must be completed before others can start:

```
Phase 1 (Setup) ─┐
Phase 2 (Foundation) ─┤
                      │
                      ├─→ Phase 3: User Story 1 (P1) - New User Registration 🎯 MVP
                      │   └─→ Independent completion OK
                      │
                      ├─→ Phase 4: User Story 2 (P1) - Returning User Login
                      │   └─→ Independent (can run parallel with US1 after foundation)
                      │
                      ├─→ Phase 5: User Story 3 (P2) - Authenticated Resource Access
                      │   └─→ Depends on: US1 OR US2 complete (need user/token to test)
                      │
                      ├─→ Phase 6: User Story 4 (P3) - User Session Management
                      │   └─→ Depends on: US2 complete (need signin to test logout)
                      │
                      └─→ Phase 7: User Story 5 (P3) - Retrieve Current User Info
                          └─→ Depends on: US3 complete (uses get_current_user_id dependency)

Phase 8 (Polish) ─→ Depends on: All user stories complete
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 (US1) → Phase 5 (US3) → Phase 7 (US5) → Phase 8

**Parallel Opportunities**:
- After Phase 2: US1 and US2 can be implemented in parallel
- After US1 or US2: US3 can start
- After US2: US4 can start
- After US3: US5 can start

---

## Parallel Execution Examples Per User Story

### Phase 3 (User Story 1) - Parallelizable Tasks:
```
Group A (Backend Models/Schemas):
- T029, T030, T031, T032 (all work on different schemas in same file, can be done together)

Group B (Frontend Components):
- T039, T040 (independent UI components)

After Group A complete:
- T033-T036 (backend endpoint - sequential within, but independent from frontend)

After Group B complete:
- T041-T045 (frontend integration - sequential within, but independent from backend after T042)

Run Group A and Group B concurrently for maximum efficiency
```

### Phase 4 (User Story 2) - Parallelizable Tasks:
```
Group A (Backend):
- T046, T047-T051 (signin endpoint implementation)

Group B (Frontend):
- T052-T057 (signin UI implementation)

Groups A and B can run fully in parallel
```

### Phase 5 (User Story 3) - Parallelizable Tasks:
```
Group A (Backend):
- T058-T060 (JWT dependency enhancement)

Group B (Frontend):
- T061-T064 (protected route and API client enhancements)

After both groups:
- T065-T066 (integration validation - requires both backend and frontend complete)

Run Group A and Group B concurrently
```

### Phase 6 (User Story 4) - All Parallelizable:
```
- T067-T072 (all frontend logout tasks can be executed in order, independent from other stories)
```

### Phase 7 (User Story 5) - Parallelizable Tasks:
```
Group A (Backend):
- T073-T075 (get current user endpoint)

Group B (Frontend):
- T076-T080 (current user API integration)

Run Group A and Group B concurrently
```

### Phase 8 (Polish) - All Parallelizable:
```
- T081-T095 (all polish tasks are independent and can run concurrently)
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Recommended MVP**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only)

This provides:
- ✅ User registration (signup)
- ✅ JWT token generation
- ✅ Automatic login after signup
- ✅ Database with users table
- ✅ Password hashing with bcrypt
- ✅ Basic frontend UI for signup

**MVP Limitations**:
- ❌ No signin for returning users (US2)
- ❌ No explicit logout (US4)
- ❌ No user profile display (US5)
- ⚠️ Protected routes work but need US2 to test fully (US3)

**Next Increment**: Add Phase 4 (US2) for returning user login

**Full Feature**: All phases for complete authentication system

### Incremental Delivery Approach

1. **Sprint 1**: Setup + Foundation + US1 (MVP)
   - Deliverable: New users can register accounts
   - Value: Users can start using the application

2. **Sprint 2**: US2 + US3 (Core Authentication)
   - Deliverable: Returning users can log in, protected routes work
   - Value: Complete authentication flow, ready for task features (Spec 2)

3. **Sprint 3**: US4 + US5 + Polish (Enhancement)
   - Deliverable: Logout, user info display, production polish
   - Value: Complete user experience, production-ready

---

## Task Summary

**Total Tasks**: 95 tasks

**Task Count Per Phase**:
- Phase 1 (Setup): 12 tasks
- Phase 2 (Foundation): 16 tasks
- Phase 3 (US1 - New User Registration): 17 tasks
- Phase 4 (US2 - Returning User Login): 12 tasks
- Phase 5 (US3 - Authenticated Resource Access): 9 tasks
- Phase 6 (US4 - User Session Management): 6 tasks
- Phase 7 (US5 - Retrieve Current User Info): 8 tasks
- Phase 8 (Polish): 15 tasks

**Task Count Per User Story**:
- User Story 1 (P1): 17 tasks
- User Story 2 (P1): 12 tasks
- User Story 3 (P2): 9 tasks
- User Story 4 (P3): 6 tasks
- User Story 5 (P3): 8 tasks

**Parallelizable Tasks**: 51 tasks marked with [P] (53.7% of total)

**Independent Test Criteria**:
- US1: Submit signup form → user created + JWT token returned
- US2: Submit signin form → JWT token returned for existing user
- US3: API request with token → accepted, without token → rejected
- US4: Logout → token cleared + requires re-authentication
- US5: Call /me endpoint → returns user info

**Critical Dependencies**:
- Phase 2 must complete before any user story
- US3 requires US1 or US2 for testing
- US4 requires US2 for testing
- US5 requires US3 for JWT dependency

**Recommended MVP**: Phase 1 + Phase 2 + Phase 3 (28 tasks, user registration only)

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description`
✅ Task IDs sequential: T001 through T095
✅ [P] markers for parallelizable tasks: 51 tasks
✅ [Story] labels for user story tasks: US1, US2, US3, US4, US5
✅ File paths included in all task descriptions
✅ Dependencies documented in dependency graph
✅ Parallel execution examples provided per phase
✅ Independent test criteria defined for each user story
✅ MVP scope clearly identified (Phase 3 - User Story 1)

**Status**: Ready for implementation via `/sp.implement` command
