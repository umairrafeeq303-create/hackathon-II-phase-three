# Tasks: Frontend UI & API Integration

**Input**: Design documents from `/specs/003-frontend-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are NOT included in this task list as they were not requested in the feature specification. Manual integration testing will be performed in the final phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/` for Next.js application
- **Backend**: `backend/src/` (already implemented in Specs 1 & 2)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Next.js project structure and install dependencies

- [ ] T001 Verify frontend/ directory exists with package.json
- [ ] T002 Install Next.js dependencies: `cd frontend && npm install`
- [ ] T003 Install Better Auth and JWT library: `npm install better-auth jose`
- [ ] T004 [P] Create frontend/src/app/ directory structure for App Router
- [ ] T005 [P] Create frontend/src/components/ directory with auth/, tasks/, layout/, ui/ subdirectories
- [ ] T006 [P] Create frontend/src/lib/ directory for utilities
- [ ] T007 [P] Create frontend/src/types/ directory for TypeScript definitions
- [ ] T008 [P] Create frontend/src/styles/ directory for global styles
- [ ] T009 Create frontend/.env.local with NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET
- [ ] T010 Create frontend/.env.example as template for environment variables
- [ ] T011 Verify Next.js dev server runs: `npm run dev`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T012 [P] Create TypeScript types in frontend/src/types/index.ts (User, Task, TaskFilters, SignupFormData, LoginFormData, TaskCreateData, TaskUpdateData)
- [ ] T013 [P] Create utility functions in frontend/src/lib/utils.ts (email validation, password validation, token extraction from JWT)
- [ ] T014 Configure Better Auth in frontend/src/lib/auth.ts with JWT plugin, database connection, and BETTER_AUTH_SECRET
- [ ] T015 Create Better Auth API route handler in frontend/src/app/api/auth/[...all]/route.ts
- [ ] T016 Create centralized API client in frontend/src/lib/api.ts with base fetch configuration and JWT token interceptor
- [ ] T017 [P] Implement API client methods: signup(), signin() in frontend/src/lib/api.ts
- [ ] T018 [P] Implement API client methods: getTasks(), getTask(), createTask(), updateTask(), deleteTask(), toggleTask() in frontend/src/lib/api.ts
- [ ] T019 [P] Implement API client error handling with 401 redirect logic in frontend/src/lib/api.ts
- [ ] T020 [P] Create reusable UI components: Button in frontend/src/components/ui/Button.tsx
- [ ] T021 [P] Create reusable UI components: Input in frontend/src/components/ui/Input.tsx
- [ ] T022 [P] Create reusable UI components: Textarea in frontend/src/components/ui/Textarea.tsx
- [ ] T023 [P] Create reusable UI components: Modal in frontend/src/components/ui/Modal.tsx
- [ ] T024 [P] Create reusable UI components: Spinner in frontend/src/components/ui/Spinner.tsx
- [ ] T025 [P] Create reusable UI components: Toast in frontend/src/components/ui/Toast.tsx for success/error messages
- [ ] T026 Configure Tailwind CSS in frontend/tailwind.config.js with custom breakpoints (sm:640px, md:768px, lg:1024px)
- [ ] T027 Setup global styles in frontend/src/styles/globals.css with Tailwind imports and custom CSS variables
- [ ] T028 Configure TypeScript strict mode in frontend/tsconfig.json

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Signup and Onboarding (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create an account, be automatically logged in, and redirected to empty task dashboard

**Independent Test**: Fill out signup form with valid credentials (name, email, password), submit, verify redirect to dashboard with authenticated session and user name in header

### Implementation for User Story 1

- [ ] T029 [P] [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.tsx with name, email, password inputs
- [ ] T030 [US1] Add client-side validation to SignupForm (email format, password min 8 chars, required fields)
- [ ] T031 [US1] Implement signup form submission with Better Auth signup API call in SignupForm
- [ ] T032 [US1] Add loading state ("Creating account...") and error display to SignupForm
- [ ] T033 [US1] Create signup page in frontend/src/app/signup/page.tsx that renders SignupForm
- [ ] T034 [US1] Implement redirect to dashboard (/) after successful signup
- [ ] T035 [US1] Add link to login page ("Already have an account? Log in") in signup page

**Checkpoint**: At this point, users can create accounts and be automatically logged in to dashboard

---

## Phase 4: User Story 2 - Returning User Login (Priority: P1)

**Goal**: Enable registered users to login with email/password and access their tasks

**Independent Test**: Enter correct email and password on login page, verify redirect to dashboard with tasks loaded and session persisted

### Implementation for User Story 2

- [ ] T036 [P] [US2] Create LoginForm component in frontend/src/components/auth/LoginForm.tsx with email, password inputs
- [ ] T037 [US2] Add client-side validation to LoginForm (email format, password required)
- [ ] T038 [US2] Implement login form submission with Better Auth signin API call in LoginForm
- [ ] T039 [US2] Add loading state ("Signing in...") and error display to LoginForm
- [ ] T040 [US2] Display "Invalid email or password" error message (no indication of which field is wrong) in LoginForm
- [ ] T041 [US2] Create login page in frontend/src/app/login/page.tsx that renders LoginForm
- [ ] T042 [US2] Implement redirect to dashboard (/) after successful login
- [ ] T043 [US2] Add redirect to dashboard if user already authenticated when accessing /login
- [ ] T044 [US2] Add link to signup page ("Don't have an account? Sign up") in login page

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can signup and login

---

## Phase 5: User Story 3 - View Task Dashboard (Priority: P1)

**Goal**: Authenticated users can view their task dashboard with task list or empty state

**Independent Test**: Login as user with existing tasks, verify all tasks displayed in correct order with proper formatting and action buttons

### Implementation for User Story 3

- [ ] T045 [P] [US3] Create ProtectedRoute wrapper component in frontend/src/components/auth/ProtectedRoute.tsx with auth check and redirect logic
- [ ] T046 [P] [US3] Create Header component in frontend/src/components/layout/Header.tsx with app title, user name, logout button
- [ ] T047 [US3] Update root layout in frontend/src/app/layout.tsx to include Header component
- [ ] T048 [P] [US3] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx with checkbox, title, description, edit/delete buttons
- [ ] T049 [P] [US3] Add strikethrough styling for completed tasks in TaskItem
- [ ] T050 [US3] Create TaskList component in frontend/src/components/tasks/TaskList.tsx that maps tasks array to TaskItem components
- [ ] T051 [US3] Add empty state to TaskList ("No tasks yet. Create your first task to get started!" with Create Task button)
- [ ] T052 [US3] Add loading skeleton (3 placeholder items) to TaskList
- [ ] T053 [US3] Create dashboard page in frontend/src/app/page.tsx with ProtectedRoute wrapper
- [ ] T054 [US3] Implement task fetching from API in dashboard page using getTasks()
- [ ] T055 [US3] Add loading state management in dashboard page
- [ ] T056 [US3] Add error handling with "Failed to load tasks" message and Retry button in dashboard page
- [ ] T057 [US3] Render TaskList with fetched tasks in dashboard page
- [ ] T058 [US3] Implement session persistence check on dashboard load (refresh user session if valid token exists)

**Checkpoint**: At this point, authenticated users can view their task dashboard with all their tasks displayed

---

## Phase 6: User Story 4 - Create New Task (Priority: P1)

**Goal**: Authenticated users can create new tasks with title and optional description

**Independent Test**: Click "Create Task" button, fill in title and description, submit, verify task appears at top of list and form closes

### Implementation for User Story 4

- [ ] T059 [P] [US4] Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx with create/edit dual mode
- [ ] T060 [US4] Add title input (required, max 200 chars) with character counter to TaskForm
- [ ] T061 [US4] Add description textarea (optional, max 1000 chars) with character counter to TaskForm
- [ ] T062 [US4] Implement client-side validation in TaskForm (title required, character limits)
- [ ] T063 [US4] Add loading state ("Creating..." / "Updating...") to TaskForm submit button
- [ ] T064 [US4] Implement create task API call in TaskForm using createTask()
- [ ] T065 [US4] Add "Create Task" button to dashboard page that opens TaskForm modal
- [ ] T066 [US4] Implement task list update after successful creation (add new task to top of list) in dashboard page
- [ ] T067 [US4] Display success toast "Task created successfully" after creation
- [ ] T068 [US4] Close TaskForm modal after successful task creation

**Checkpoint**: At this point, users can create tasks and see them appear immediately in their task list

---

## Phase 7: User Story 6 - Filter and Sort Tasks (Priority: P1)

**Goal**: Users can filter tasks by status and sort by date or title

**Independent Test**: Apply status filter "Pending", verify only pending tasks shown; change sort to "Title (A-Z)", verify tasks reordered alphabetically

### Implementation for User Story 6

- [ ] T069 [P] [US6] Create TaskFilters component in frontend/src/components/tasks/TaskFilters.tsx with dropdowns
- [ ] T070 [US6] Add status filter dropdown to TaskFilters (All, Pending, Completed)
- [ ] T071 [US6] Add sort dropdown to TaskFilters (Created Date Newest, Created Date Oldest, Title A-Z, Title Z-A)
- [ ] T072 [US6] Add "Clear Filters" button to TaskFilters
- [ ] T073 [US6] Implement filter state management in dashboard page (status, sort, order)
- [ ] T074 [US6] Connect TaskFilters to dashboard page filter state
- [ ] T075 [US6] Implement filtered API call when filters change in dashboard page using getTasks(userId, filters)
- [ ] T076 [US6] Add loading indicator during filter application in dashboard page
- [ ] T077 [US6] Render TaskFilters component above TaskList in dashboard page

**Checkpoint**: At this point, users can filter and sort their task list dynamically

---

## Phase 8: User Story 5 - Toggle Task Completion (Priority: P1)

**Goal**: Users can mark tasks complete or reopen completed tasks by clicking checkbox

**Independent Test**: Click checkbox on pending task, verify it becomes checked with strikethrough; click again, verify it reverts to pending

### Implementation for User Story 5

- [ ] T078 [P] [US5] Implement checkbox click handler in TaskItem component
- [ ] T079 [US5] Add loading spinner to checkbox during API request in TaskItem
- [ ] T080 [US5] Implement toggle task API call in TaskItem using toggleTask()
- [ ] T081 [US5] Update task styling immediately after successful toggle (add/remove strikethrough) in TaskItem
- [ ] T082 [US5] Implement error rollback if toggle fails (revert checkbox state, show error toast) in TaskItem
- [ ] T083 [US5] Handle multiple rapid toggles with queued requests in TaskItem

**Checkpoint**: At this point, users can toggle task completion with immediate visual feedback

---

## Phase 9: User Story 7 - Edit Task (Priority: P2)

**Goal**: Users can modify existing task title and/or description

**Independent Test**: Click edit button on task, modify title, submit, verify changes reflected in task list

### Implementation for User Story 7

- [ ] T084 [P] [US7] Add edit mode support to TaskForm component (pre-populate title and description)
- [ ] T085 [US7] Add edit button to TaskItem component
- [ ] T086 [US7] Implement edit button click handler in TaskItem that opens TaskForm with current task data
- [ ] T087 [US7] Implement update task API call in TaskForm using updateTask()
- [ ] T088 [US7] Update task in dashboard page task list after successful edit
- [ ] T089 [US7] Display success toast "Task updated successfully" after edit
- [ ] T090 [US7] Add Cancel button to TaskForm that closes modal without saving changes

**Checkpoint**: At this point, users can edit existing tasks and see updates immediately

---

## Phase 10: User Story 8 - Delete Task (Priority: P2)

**Goal**: Users can permanently delete tasks with confirmation

**Independent Test**: Click delete button, confirm deletion in modal, verify task removed from list with animation

### Implementation for User Story 8

- [ ] T091 [P] [US8] Create DeleteConfirmation component in frontend/src/components/tasks/DeleteConfirmation.tsx with modal
- [ ] T092 [US8] Display task title in confirmation message "Are you sure you want to delete '[Task Title]'?" in DeleteConfirmation
- [ ] T093 [US8] Add Cancel and Delete buttons to DeleteConfirmation
- [ ] T094 [US8] Add loading state ("Deleting...") to Delete button in DeleteConfirmation
- [ ] T095 [US8] Add delete button to TaskItem component
- [ ] T096 [US8] Implement delete button click handler in TaskItem that opens DeleteConfirmation modal
- [ ] T097 [US8] Implement delete task API call in DeleteConfirmation using deleteTask()
- [ ] T098 [US8] Remove task from dashboard page task list after successful deletion with fade-out animation
- [ ] T099 [US8] Display success toast "Task deleted successfully" after deletion
- [ ] T100 [US8] Handle delete error and show error toast "Failed to delete task. Please try again."

**Checkpoint**: At this point, users can delete tasks with confirmation and immediate visual feedback

---

## Phase 11: User Story 9 - User Logout (Priority: P2)

**Goal**: Users can logout, clearing their session and redirecting to login page

**Independent Test**: Click logout button in header, verify redirected to login page, attempt to access dashboard, verify redirected back to login

### Implementation for User Story 9

- [ ] T101 [P] [US9] Implement logout button click handler in Header component
- [ ] T102 [US9] Add loading state ("Logging out...") to logout button in Header
- [ ] T103 [US9] Clear JWT token from localStorage on logout in Header
- [ ] T104 [US9] Clear Better Auth session on logout in Header
- [ ] T105 [US9] Redirect to /login after logout in Header
- [ ] T106 [US9] Verify protected route redirect works after logout (dashboard → login)

**Checkpoint**: At this point, all P2 user stories are complete and users have full CRUD + auth functionality

---

## Phase 12: Responsive Design & Polish

**Purpose**: Ensure mobile-first responsive design and final UI polish across all user stories

- [ ] T107 [P] Apply mobile-first responsive styles to all components (breakpoints: sm:640px, md:768px, lg:1024px)
- [ ] T108 [P] Test TaskForm modal: full-width on mobile, centered on desktop
- [ ] T109 [P] Test TaskList: stack items vertically on all screen sizes
- [ ] T110 [P] Test Header: hamburger menu on mobile (<640px), full layout on desktop
- [ ] T111 [P] Test login/signup forms: responsive padding and button sizes
- [ ] T112 Test on mobile device (≥375px width) - verify all features functional
- [ ] T113 Test on tablet device (≥768px width) - verify all features functional
- [ ] T114 Test on desktop device (≥1024px width) - verify all features functional
- [ ] T115 [P] Add focus states to all interactive elements (buttons, inputs, checkboxes)
- [ ] T116 [P] Add hover states to all buttons and clickable elements
- [ ] T117 [P] Verify all loading states display correctly (spinners, skeletons, disabled buttons)
- [ ] T118 [P] Verify all error messages are user-friendly and actionable
- [ ] T119 [P] Optimize bundle size by removing unused dependencies
- [ ] T120 Cross-browser testing (Chrome, Firefox, Safari, Edge)

---

## Phase 13: Integration Testing & Documentation

**Purpose**: Comprehensive testing of all user flows and documentation updates

- [ ] T121 Test complete signup flow: /signup → fill form → submit → redirected to dashboard
- [ ] T122 Test complete login flow: /login → enter credentials → submit → redirected to dashboard
- [ ] T123 Test task creation flow: dashboard → create task → task appears in list
- [ ] T124 Test task toggle flow: click checkbox → task status changes → strikethrough applied
- [ ] T125 Test task filtering flow: filter by status → only matching tasks shown
- [ ] T126 Test task sorting flow: sort by title A-Z → tasks reordered alphabetically
- [ ] T127 Test task editing flow: edit task → modify title → submit → changes reflected
- [ ] T128 Test task deletion flow: delete task → confirm → task removed from list
- [ ] T129 Test logout flow: click logout → redirected to login → cannot access dashboard
- [ ] T130 Test user isolation: create tasks as user A → login as user B → verify user A tasks not visible
- [ ] T131 Test session persistence: login → refresh page → verify still authenticated
- [ ] T132 Test error scenarios: network timeout, 401 unauthorized, 500 server error
- [ ] T133 Test loading states: all async operations show appropriate loading indicators
- [ ] T134 Create frontend/README.md with setup instructions, environment variables, and development workflow
- [ ] T135 Update root README.md to mark Spec 3 as complete
- [ ] T136 Verify all acceptance scenarios from spec.md are implemented and testable

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-11)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Responsive Design (Phase 12)**: Can start after any user story is complete, run in parallel with later stories
- **Integration Testing (Phase 13)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (Signup - P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Login - P1)**: Can start after Foundational (Phase 2) - Independent from US1 but integrates with dashboard
- **User Story 3 (Dashboard - P1)**: Can start after Foundational (Phase 2) - Depends on US1 or US2 for authentication to test
- **User Story 4 (Create Task - P1)**: Can start after Foundational (Phase 2) - Depends on US3 for task list display
- **User Story 6 (Filters - P1)**: Can start after Foundational (Phase 2) - Depends on US3 for task list to filter
- **User Story 5 (Toggle - P1)**: Can start after Foundational (Phase 2) - Depends on US3 for task list to toggle
- **User Story 7 (Edit - P2)**: Can start after Foundational (Phase 2) - Depends on US3 for task list to edit
- **User Story 8 (Delete - P2)**: Can start after Foundational (Phase 2) - Depends on US3 for task list to delete
- **User Story 9 (Logout - P2)**: Can start after Foundational (Phase 2) - Depends on US1 or US2 for authentication

### Within Each User Story

- Core components before integration
- Validation before API calls
- Success states before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T004-T008)
- All Foundational UI components marked [P] can run in parallel (T020-T025)
- Once Foundational phase completes, user stories can start in priority-grouped batches:
  - Batch 1 (P1 Auth): US1, US2 in parallel
  - Batch 2 (P1 Dashboard): US3 after auth complete
  - Batch 3 (P1 Tasks): US4, US5, US6 in parallel after dashboard complete
  - Batch 4 (P2): US7, US8, US9 in parallel
- All responsive design tasks marked [P] can run in parallel (T107-T111, T115-T119)

---

## Parallel Example: Foundational Phase

```bash
# Launch all UI components together:
Task: "Create reusable UI components: Button in frontend/src/components/ui/Button.tsx"
Task: "Create reusable UI components: Input in frontend/src/components/ui/Input.tsx"
Task: "Create reusable UI components: Textarea in frontend/src/components/ui/Textarea.tsx"
Task: "Create reusable UI components: Modal in frontend/src/components/ui/Modal.tsx"
Task: "Create reusable UI components: Spinner in frontend/src/components/ui/Spinner.tsx"
Task: "Create reusable UI components: Toast in frontend/src/components/ui/Toast.tsx"
```

## Parallel Example: User Story 1 (Signup)

```bash
# Launch signup form component and signup page together:
Task: "Create SignupForm component in frontend/src/components/auth/SignupForm.tsx"
Task: "Create signup page in frontend/src/app/signup/page.tsx"
# Note: page will initially render empty until form component is complete
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3, 4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Signup)
4. Complete Phase 4: User Story 2 (Login)
5. Complete Phase 5: User Story 3 (Dashboard)
6. Complete Phase 6: User Story 4 (Create Task)
7. **STOP and VALIDATE**: Test signup → login → view dashboard → create task flow
8. Deploy/demo if ready

### Incremental Delivery (Full P1 Scope)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Signup) + 2 (Login) → Test auth flow → Deploy/Demo
3. Add User Story 3 (Dashboard) → Test task viewing → Deploy/Demo
4. Add User Story 4 (Create Task) → Test task creation → Deploy/Demo
5. Add User Story 6 (Filters) + 5 (Toggle) → Test task management → Deploy/Demo (P1 COMPLETE!)
6. Add User Story 7 (Edit) + 8 (Delete) + 9 (Logout) → Test P2 features → Deploy/Demo
7. Add Phase 12 (Responsive Design) → Test on all devices → Deploy/Demo
8. Complete Phase 13 (Integration Testing) → Final validation → Production release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Signup) + User Story 2 (Login)
   - Developer B: User Story 3 (Dashboard) + User Story 5 (Toggle)
   - Developer C: User Story 4 (Create Task) + User Story 6 (Filters)
3. After P1 stories complete:
   - Developer A: User Story 7 (Edit)
   - Developer B: User Story 8 (Delete)
   - Developer C: User Story 9 (Logout) + Responsive Design
4. Team integrates and tests together in Phase 13

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All API calls must include JWT token from localStorage via API client
- All forms must have loading states and error handling
- All async operations must show visual feedback within 100ms
- Empty states must show friendly messages with clear calls-to-action
- Environment variables must be configured before Better Auth will work
- Backend API (Specs 1 & 2) must be running for integration testing
- CORS must be configured on backend to allow frontend origin

---

**Total Tasks**: 136
**Estimated Time**: 25-30 hours
**MVP Scope**: Phases 1-6 (T001-T068) = ~15 hours
**P1 Complete**: Phases 1-8 (T001-T083) = ~18 hours
**Full Feature Set**: All phases (T001-T136) = ~25-30 hours

**Branch**: `003-frontend-ui`
**Prerequisites**: Spec 1 (Authentication) and Spec 2 (Task CRUD API) must be complete and backend running
