# Task Breakdown: Task CRUD API Backend

**Feature**: Task CRUD API Backend
**Branch**: `002-task-crud`
**Created**: 2026-01-09
**Total Tasks**: 28
**Estimated Time**: 6-8 hours

## Overview

This task breakdown implements Spec 2 (Task CRUD API Backend) organized by user story priorities. Each phase represents a complete, independently testable increment of functionality.

**User Stories**:
- US1 (P1): Create New Task
- US2 (P1): View All Tasks (with filtering and sorting)
- US3 (P2): View Single Task Details
- US4 (P2): Update Task
- US5 (P2): Delete Task
- US6 (P1): Toggle Task Completion

**Implementation Strategy**: Deliver P1 user stories first (US1, US2, US6) for MVP, then add P2 stories (US3, US4, US5) for full feature set.

---

## Phase 1: Setup and Prerequisites

**Goal**: Prepare project structure and verify Spec 1 integration points

**Independent Test**: Run backend server and verify Spec 1 auth endpoints are functional

### Tasks

- [X] T001 Verify Spec 1 authentication system is complete in backend/src/core/deps.py
- [X] T002 Verify User model exists in backend/src/models/user.py with id field
- [X] T003 Verify database session dependency exists in backend/src/db/session.py
- [X] T004 Create backend/src/models/task.py file for Task model
- [X] T005 Create backend/src/schemas/task.py file for Task schemas
- [X] T006 Create backend/src/api/routes/tasks.py file for Task routes

---

## Phase 2: Foundation - Task Model and Schemas

**Goal**: Create database model and validation schemas used by all user stories

**Independent Test**: Import Task model and schemas without errors; table created in database on startup

### Tasks

- [X] T007 [P] Implement Task SQLModel in backend/src/models/task.py with fields: id, user_id (FK to users.id), title (max 200), description (max 1000, optional), completed (default False), created_at, updated_at
- [X] T008 [P] Add indexes to Task model on user_id and completed fields in backend/src/models/task.py
- [X] T009 [P] Configure foreign key CASCADE DELETE from tasks.user_id to users.id in backend/src/models/task.py
- [X] T010 [P] Implement TaskBase schema with title and description validation in backend/src/schemas/task.py
- [X] T011 [P] Implement TaskCreate schema inheriting from TaskBase in backend/src/schemas/task.py
- [X] T012 [P] Implement TaskUpdate schema with optional fields in backend/src/schemas/task.py
- [X] T013 [P] Implement TaskResponse schema with all task fields in backend/src/schemas/task.py
- [X] T014 [P] Add whitespace stripping validators to TaskBase schema in backend/src/schemas/task.py
- [X] T015 Import Task model in backend/src/main.py to trigger table creation
- [X] T016 Restart backend server and verify tasks table created in Neon database

---

## Phase 3: User Story 1 - Create New Task (P1)

**Goal**: Enable authenticated users to create tasks with title and optional description

**Independent Test**:
1. Authenticate as user A
2. POST /api/{user_a_id}/tasks with title "Test Task"
3. Verify 201 response with task object containing id, user_id, title, completed=false, timestamps
4. Verify task stored in database with correct user_id

**Acceptance Criteria**: All 7 acceptance scenarios from US1 in spec.md

### Tasks

- [X] T017 [US1] Create APIRouter with prefix "/api/{user_id}/tasks" and tag "tasks" in backend/src/api/routes/tasks.py
- [X] T018 [US1] Implement verify_user_match helper function to validate URL user_id matches JWT user_id in backend/src/api/routes/tasks.py
- [X] T019 [US1] Implement POST /api/{user_id}/tasks endpoint accepting TaskCreate schema in backend/src/api/routes/tasks.py
- [X] T020 [US1] Add JWT authentication using get_current_user_id dependency from Spec 1 in POST endpoint
- [X] T021 [US1] Add user_id validation logic calling verify_user_match in POST endpoint
- [X] T022 [US1] Create Task object with user_id from JWT token in POST endpoint
- [X] T023 [US1] Save task to database and return 201 with TaskResponse in POST endpoint
- [X] T024 [US1] Include tasks router in backend/src/main.py with app.include_router(tasks.router)
- [ ] T025 [US1] Test create task endpoint: valid title, title+description, missing title (422), title >200 chars (422), user_id mismatch (403)

---

## Phase 4: User Story 6 - Toggle Task Completion (P1)

**Goal**: Enable users to mark tasks complete or reopen completed tasks

**Independent Test**:
1. Authenticate as user A
2. Create task (completed=false)
3. PATCH /api/{user_a_id}/tasks/{task_id}/toggle
4. Verify 200 response with completed=true and updated_at changed
5. PATCH again, verify completed=false

**Acceptance Criteria**: All 6 acceptance scenarios from US6 in spec.md

### Tasks

- [ ] T026 [US6] Implement get_user_task_or_404 helper function to fetch task with ownership validation in backend/src/api/routes/tasks.py
- [ ] T027 [US6] Implement PATCH /api/{user_id}/tasks/{task_id}/toggle endpoint in backend/src/api/routes/tasks.py
- [ ] T028 [US6] Add JWT authentication using get_current_user_id in PATCH toggle endpoint
- [ ] T029 [US6] Add user_id validation in PATCH toggle endpoint
- [ ] T030 [US6] Fetch task using get_user_task_or_404 in PATCH toggle endpoint
- [ ] T031 [US6] Toggle completed field (not task.completed) in PATCH toggle endpoint
- [ ] T032 [US6] Update updated_at timestamp to datetime.utcnow() in PATCH toggle endpoint
- [ ] T033 [US6] Save and return updated task with 200 status in PATCH toggle endpoint
- [ ] T034 [US6] Test toggle endpoint: pending→completed, completed→pending, non-existent task (404), wrong user (403)

---

## Phase 5: User Story 2 - View All Tasks (P1)

**Goal**: Enable users to view their task list with filtering by status and sorting

**Independent Test**:
1. Authenticate as user A
2. Create 3 tasks: 2 pending, 1 completed
3. GET /api/{user_a_id}/tasks
4. Verify returns 3 tasks sorted by created_at desc
5. GET /api/{user_a_id}/tasks?status=completed
6. Verify returns only 1 completed task
7. Authenticate as user B
8. GET /api/{user_b_id}/tasks
9. Verify returns 0 tasks (user isolation)

**Acceptance Criteria**: All 9 acceptance scenarios from US2 in spec.md

### Tasks

- [ ] T035 [US2] Create TaskStatus enum (ALL, PENDING, COMPLETED) in backend/src/api/routes/tasks.py
- [ ] T036 [US2] Create SortField enum (CREATED, TITLE) in backend/src/api/routes/tasks.py
- [ ] T037 [US2] Create SortOrder enum (ASC, DESC) in backend/src/api/routes/tasks.py
- [ ] T038 [US2] Implement GET /api/{user_id}/tasks endpoint with query params: status, sort, order in backend/src/api/routes/tasks.py
- [ ] T039 [US2] Add JWT authentication using get_current_user_id in GET list endpoint
- [ ] T040 [US2] Add user_id validation in GET list endpoint
- [ ] T041 [US2] Build base query filtering by current_user_id in GET list endpoint
- [ ] T042 [US2] Add status filter logic (PENDING: completed==False, COMPLETED: completed==True, ALL: no filter) in GET list endpoint
- [ ] T043 [US2] Add sorting logic (TITLE: Task.title.collate("NOCASE"), CREATED: Task.created_at) in GET list endpoint
- [ ] T044 [US2] Add order logic (ASC or DESC) to query in GET list endpoint
- [ ] T045 [US2] Execute query and return list of TaskResponse with 200 status in GET list endpoint
- [ ] T046 [US2] Test list endpoint: all tasks, filter pending, filter completed, sort by title asc, sort by created desc, user isolation, empty list

---

## Phase 6: User Story 3 - View Single Task Details (P2)

**Goal**: Enable users to view complete details of a specific task

**Independent Test**:
1. Authenticate as user A
2. Create task
3. GET /api/{user_a_id}/tasks/{task_id}
4. Verify 200 response with complete task object (all fields)
5. Authenticate as user B
6. GET /api/{user_a_id}/tasks/{task_id}
7. Verify 404 response (not 403, enumeration prevention)

**Acceptance Criteria**: All 4 acceptance scenarios from US3 in spec.md

### Tasks

- [ ] T047 [US3] Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [ ] T048 [US3] Add JWT authentication using get_current_user_id in GET single endpoint
- [ ] T049 [US3] Add user_id validation in GET single endpoint
- [ ] T050 [US3] Fetch task using get_user_task_or_404 helper in GET single endpoint
- [ ] T051 [US3] Return TaskResponse with 200 status in GET single endpoint
- [ ] T052 [US3] Test get single endpoint: existing task, non-existent task (404), wrong user (404 not 403)

---

## Phase 7: User Story 4 - Update Task (P2)

**Goal**: Enable users to modify task title and/or description

**Independent Test**:
1. Authenticate as user A
2. Create task with title "Original"
3. PUT /api/{user_a_id}/tasks/{task_id} with {"title": "Updated"}
4. Verify 200 response with updated title and new updated_at
5. Verify description unchanged

**Acceptance Criteria**: All 9 acceptance scenarios from US4 in spec.md

### Tasks

- [ ] T053 [US4] Implement PUT /api/{user_id}/tasks/{task_id} endpoint accepting TaskUpdate schema in backend/src/api/routes/tasks.py
- [ ] T054 [US4] Add JWT authentication using get_current_user_id in PUT endpoint
- [ ] T055 [US4] Add user_id validation in PUT endpoint
- [ ] T056 [US4] Fetch task using get_user_task_or_404 in PUT endpoint
- [ ] T057 [US4] Extract update_data using task_update.dict(exclude_unset=True) in PUT endpoint
- [ ] T058 [US4] Validate at least one field provided, raise 422 if empty in PUT endpoint
- [ ] T059 [US4] Apply updates using setattr loop in PUT endpoint
- [ ] T060 [US4] Update updated_at timestamp to datetime.utcnow() in PUT endpoint
- [ ] T061 [US4] Save and return updated task with 200 status in PUT endpoint
- [ ] T062 [US4] Test update endpoint: update title, update description, update both, empty update (422), invalid values (422), non-existent task (404), wrong user (403)

---

## Phase 8: User Story 5 - Delete Task (P2)

**Goal**: Enable users to permanently delete tasks

**Independent Test**:
1. Authenticate as user A
2. Create task
3. DELETE /api/{user_a_id}/tasks/{task_id}
4. Verify 200 response with success message
5. GET /api/{user_a_id}/tasks/{task_id}
6. Verify 404 response (task deleted)

**Acceptance Criteria**: All 6 acceptance scenarios from US5 in spec.md

### Tasks

- [ ] T063 [US5] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/src/api/routes/tasks.py
- [ ] T064 [US5] Add JWT authentication using get_current_user_id in DELETE endpoint
- [ ] T065 [US5] Add user_id validation in DELETE endpoint
- [ ] T066 [US5] Fetch task using get_user_task_or_404 in DELETE endpoint
- [ ] T067 [US5] Delete task from database using session.delete(task) in DELETE endpoint
- [ ] T068 [US5] Commit transaction and return success message with 200 status in DELETE endpoint
- [ ] T069 [US5] Test delete endpoint: delete existing task, verify deletion, non-existent task (404), wrong user (403)

---

## Phase 9: Polish and Validation

**Goal**: Final integration testing, documentation, and deployment readiness

### Tasks

- [ ] T070 [P] Run full integration test: signup → create tasks → list → filter → sort → toggle → update → delete
- [ ] T071 [P] Test user isolation: user A cannot access user B's tasks (all endpoints return 403/404)
- [ ] T072 [P] Test CASCADE DELETE: delete user, verify all user's tasks deleted
- [ ] T073 [P] Verify all endpoints appear in Swagger UI at /docs
- [ ] T074 [P] Test performance: create 100 tasks, verify list endpoint <1 second
- [ ] T075 Update backend README.md with Task CRUD API documentation

---

## Dependencies and Execution Order

### User Story Dependency Graph

```
Phase 1 (Setup) → Phase 2 (Foundation) → Phase 3 (US1: Create Task) [P1]
                                       ↓
                                       Phase 4 (US6: Toggle Complete) [P1]
                                       ↓
                                       Phase 5 (US2: View All Tasks) [P1]
                                       ↓
                                       Phase 6 (US3: View Single) [P2]
                                       ↓
                                       Phase 7 (US4: Update Task) [P2]
                                       ↓
                                       Phase 8 (US5: Delete Task) [P2]
                                       ↓
                                       Phase 9 (Polish)
```

**MVP Scope** (minimum viable product):
- Phase 1: Setup
- Phase 2: Foundation
- Phase 3: US1 (Create Task)
- Phase 4: US6 (Toggle Complete)
- Phase 5: US2 (View All Tasks)

This gives users the ability to create, view, and complete tasks - the core todo functionality.

**Full Feature Set**:
- Add Phase 6 (US3: View Single)
- Add Phase 7 (US4: Update Task)
- Add Phase 8 (US5: Delete Task)
- Add Phase 9 (Polish)

### Sequential Execution Rules

**Must Complete Before Others**:
- T001-T006 (Setup) MUST complete before all other phases
- T007-T016 (Foundation) MUST complete before US1, US2, US3, US4, US5, US6
- T017-T024 (US1: Create) MUST complete before T070 (integration test)
- T026 (get_user_task_or_404 helper) MUST complete before T047-T069 (all endpoints that fetch tasks)

**Can Execute in Parallel** (marked with [P]):
- T007-T014 can run in parallel (different aspects of model/schemas)
- T035-T037 can run in parallel (enum definitions)
- T070-T074 can run in parallel (independent test scenarios)

### File Coordination

Tasks affecting the same file MUST run sequentially:

**backend/src/models/task.py**: T007 → T008 → T009 (sequential)
**backend/src/schemas/task.py**: T010 → T011 → T012 → T013 → T014 (sequential)
**backend/src/api/routes/tasks.py**: T017 → T018 → T019 → T020 → T021 → T022 → T023 → T026 → T027 → ... (all route tasks sequential)
**backend/src/main.py**: T015 → T024 (sequential)

---

## Implementation Guidance

### Phase-by-Phase Execution

1. **Complete Phase 1 (Setup)** before any other work - verifies Spec 1 integration
2. **Complete Phase 2 (Foundation)** to create shared model and schemas
3. **Implement P1 User Stories** (US1, US6, US2) for MVP
4. **Verify MVP works** with integration tests
5. **Add P2 User Stories** (US3, US4, US5) for full feature set
6. **Polish and validate** with comprehensive testing

### Validation Checkpoints

After each phase, verify:
- ✅ All tasks in phase marked complete
- ✅ Server restarts without errors
- ✅ Swagger UI reflects new endpoints
- ✅ Manual tests pass (use curl or Swagger UI)
- ✅ User isolation maintained (different users cannot access each other's tasks)

### Testing Strategy

**Unit Tests** (optional, not in this task list):
- Schema validation (TaskCreate, TaskUpdate, TaskResponse)
- Helper functions (verify_user_match, get_user_task_or_404)

**Integration Tests** (included in tasks):
- T025: Test US1 create endpoint
- T034: Test US6 toggle endpoint
- T046: Test US2 list endpoint with filters
- T052: Test US3 get single endpoint
- T062: Test US4 update endpoint
- T069: Test US5 delete endpoint
- T070-T074: Full system integration tests

**Security Tests** (included in tasks):
- T071: User isolation validation
- Every endpoint tests 403/404 responses for wrong user access

---

## Task Completion Tracking

**Phase 1 (Setup)**: 0/6 complete
**Phase 2 (Foundation)**: 0/10 complete
**Phase 3 (US1 - Create Task)**: 0/9 complete
**Phase 4 (US6 - Toggle Complete)**: 0/9 complete
**Phase 5 (US2 - View All Tasks)**: 0/12 complete
**Phase 6 (US3 - View Single)**: 0/6 complete
**Phase 7 (US4 - Update Task)**: 0/10 complete
**Phase 8 (US5 - Delete Task)**: 0/7 complete
**Phase 9 (Polish)**: 0/6 complete

**Total Progress**: 0/75 tasks complete (0%)

---

## Next Steps

1. Review this task breakdown
2. Execute `/sp.implement` to begin implementation
3. Follow tasks sequentially, marking each [X] when complete
4. Test after each user story phase
5. Deploy MVP after Phase 5, or continue to full feature set

---

*Generated by `/sp.tasks` on 2026-01-09*
