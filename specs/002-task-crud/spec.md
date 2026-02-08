# Feature Specification: Task CRUD API Backend

**Feature Branch**: `002-task-crud`
**Created**: 2026-01-09
**Status**: Draft
**Input**: Task CRUD API Backend - RESTful endpoints for task operations with JWT authentication and user ownership validation

## Overview

This specification defines the Task CRUD (Create, Read, Update, Delete) API Backend that enables authenticated users to manage their personal todo tasks. This is Spec 2 of 3 total specifications for Phase II of the Todo Full-Stack Web Application.

**Purpose**: Provide secure, RESTful API endpoints for task management operations where each user can only access and modify their own tasks. Integrates with the authentication system from Spec 1 (001-auth) to enforce user data isolation.

**Key Stakeholders**:
- End users (need to create, view, update, and delete their personal tasks)
- Frontend application (Next.js client consuming the API)
- Backend API (FastAPI providing task CRUD operations)
- Authentication system (Spec 1 - provides JWT token validation)
- Database (Neon PostgreSQL for task storage)

**Integration with Spec 1**:
- Uses JWT token validation from authentication system
- Leverages User model foreign key relationship
- Shares database connection and BETTER_AUTH_SECRET
- Reuses authentication middleware (get_current_user_id dependency)

**Success Criteria**:
- Users can create a new task in under 5 seconds
- Users can view their task list instantly (sub-second load time)
- System supports 10,000+ tasks per user without performance degradation
- Zero incidents of users accessing other users' tasks (100% data isolation)
- 98% of task operations succeed without errors
- Users can filter and sort tasks with results returned in under 1 second

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Task (Priority: P1)

A logged-in user wants to add a new task to their todo list. They provide a task title (required) and optionally a description. The system creates the task, associates it with the user's account, and returns the created task with a unique ID.

**Why this priority**: Task creation is the core entry point for task management. Without the ability to create tasks, the application has no value. This is the foundation of the todo feature.

**Independent Test**: Can be fully tested by authenticating a user, submitting a task creation request with title and description, and verifying that the task is stored in the database with correct user_id association and a 201 status is returned.

**Acceptance Scenarios**:

1. **Given** the user is authenticated with a valid JWT token, **When** they submit a POST request to `/api/{user_id}/tasks` with a title "Buy groceries", **Then** the system creates the task, associates it with the authenticated user, and returns the task object with ID, title, user_id, and timestamps with 201 status
2. **Given** the user submits a task with title and description, **When** the task is created, **Then** both title and description are stored and returned in the response
3. **Given** the user submits a task with only a title (no description), **When** the task is created, **Then** the description field is null/empty and the task is created successfully
4. **Given** the user submits a task with an empty title, **When** the request is processed, **Then** the system returns an error "Title is required" with 422 status code
5. **Given** the user submits a task with a title exceeding 200 characters, **When** the request is processed, **Then** the system returns an error "Title must be 200 characters or less" with 422 status code
6. **Given** the user submits a task with a description exceeding 1000 characters, **When** the request is processed, **Then** the system returns an error "Description must be 1000 characters or less" with 422 status code
7. **Given** the user_id in the URL does not match the JWT token's user_id, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code

---

### User Story 2 - View All Tasks (Priority: P1)

A logged-in user wants to see all their tasks in a list. The system retrieves all tasks belonging to the authenticated user and returns them in a structured format. Users can filter tasks by completion status and sort them by creation date or title.

**Why this priority**: Viewing tasks is equally critical to creating them. Users must be able to see their tasks to interact with them. This is P1 because it's required immediately after task creation to provide value.

**Independent Test**: Can be fully tested by creating multiple tasks for a user, then requesting the task list and verifying that only the user's tasks are returned with correct filtering and sorting applied.

**Acceptance Scenarios**:

1. **Given** the user has created 5 tasks, **When** they request GET `/api/{user_id}/tasks`, **Then** the system returns all 5 tasks sorted by created_at descending (newest first)
2. **Given** the user has both completed and pending tasks, **When** they request GET `/api/{user_id}/tasks?status=pending`, **Then** the system returns only tasks where completed=false
3. **Given** the user has both completed and pending tasks, **When** they request GET `/api/{user_id}/tasks?status=completed`, **Then** the system returns only tasks where completed=true
4. **Given** the user requests GET `/api/{user_id}/tasks?status=all`, **When** the request is processed, **Then** the system returns all tasks regardless of completion status
5. **Given** the user requests GET `/api/{user_id}/tasks?sort=title&order=asc`, **When** the request is processed, **Then** the system returns tasks sorted alphabetically by title in ascending order
6. **Given** the user requests GET `/api/{user_id}/tasks?sort=created&order=desc`, **When** the request is processed, **Then** the system returns tasks sorted by creation date with newest first (default behavior)
7. **Given** user A has 10 tasks and user B has 5 tasks, **When** user A requests GET `/api/{userA_id}/tasks`, **Then** the system returns only user A's 10 tasks and none of user B's tasks
8. **Given** the user has no tasks, **When** they request GET `/api/{user_id}/tasks`, **Then** the system returns an empty array with 200 status code
9. **Given** the user_id in the URL does not match the JWT token's user_id, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code

---

### User Story 3 - View Single Task Details (Priority: P2)

A logged-in user wants to view the details of a specific task. The system retrieves and returns the task if it belongs to the authenticated user.

**Why this priority**: Viewing individual task details is important for task management but is lower priority than creating and listing tasks. Users can see basic info in the list view, so detailed view is a secondary need.

**Independent Test**: Can be fully tested by creating a task, then requesting it by ID and verifying that the complete task details are returned with all fields populated.

**Acceptance Scenarios**:

1. **Given** the user has a task with ID 42, **When** they request GET `/api/{user_id}/tasks/42`, **Then** the system returns the complete task object including id, user_id, title, description, completed, created_at, and updated_at
2. **Given** the user requests a task ID that doesn't exist, **When** the request is processed, **Then** the system returns an error "Task not found" with 404 status code
3. **Given** user A requests a task that belongs to user B, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code (not "Task not found" to prevent enumeration)
4. **Given** the user_id in the URL does not match the JWT token's user_id, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code

---

### User Story 4 - Update Task (Priority: P2)

A logged-in user wants to modify an existing task's title or description. The system validates ownership, updates the specified fields, and updates the updated_at timestamp.

**Why this priority**: Task editing is important for task management but is secondary to creation and viewing. Users need to fix typos or update task details, making this P2.

**Independent Test**: Can be fully tested by creating a task, updating its title and/or description, and verifying that the changes are persisted and the updated_at timestamp is modified.

**Acceptance Scenarios**:

1. **Given** the user has a task with title "Buy groceries", **When** they send PUT `/api/{user_id}/tasks/{id}` with title "Buy groceries and milk", **Then** the system updates the title and returns the updated task with a new updated_at timestamp
2. **Given** the user has a task, **When** they update only the description, **Then** the system updates the description while keeping the title unchanged and updates the updated_at timestamp
3. **Given** the user sends an update request with both title and description, **When** the request is processed, **Then** both fields are updated and updated_at is updated
4. **Given** the user sends an update request with neither title nor description, **When** the request is processed, **Then** the system returns an error "At least one field (title or description) must be provided" with 400 status code
5. **Given** the user sends an update with an empty title, **When** the request is processed, **Then** the system returns an error "Title cannot be empty" with 422 status code
6. **Given** the user sends an update with a title exceeding 200 characters, **When** the request is processed, **Then** the system returns an error "Title must be 200 characters or less" with 422 status code
7. **Given** the user sends an update for a task that doesn't exist, **When** the request is processed, **Then** the system returns an error "Task not found" with 404 status code
8. **Given** user A tries to update user B's task, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code
9. **Given** the user_id in the URL does not match the JWT token's user_id, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code

---

### User Story 5 - Delete Task (Priority: P2)

A logged-in user wants to remove a task from their list. The system validates ownership and permanently deletes the task from the database.

**Why this priority**: Task deletion is important for keeping the task list clean but is not critical for initial value delivery. Users can leave tasks uncompleted instead of deleting them, making this P2.

**Independent Test**: Can be fully tested by creating a task, deleting it, and verifying that it no longer appears in the task list and cannot be retrieved by ID.

**Acceptance Scenarios**:

1. **Given** the user has a task with ID 42, **When** they send DELETE `/api/{user_id}/tasks/42`, **Then** the system deletes the task and returns a success message with 200 status code
2. **Given** the user has deleted a task, **When** they try to retrieve it by ID, **Then** the system returns "Task not found" with 404 status code
3. **Given** the user tries to delete a task that doesn't exist, **When** the request is processed, **Then** the system returns an error "Task not found" with 404 status code
4. **Given** user A tries to delete user B's task, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code
5. **Given** the user_id in the URL does not match the JWT token's user_id, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code
6. **Given** the user deletes a task, **When** they request their task list, **Then** the deleted task does not appear in the list

---

### User Story 6 - Toggle Task Completion (Priority: P1)

A logged-in user wants to mark a task as complete or reopen a completed task. The system toggles the completion status and updates the updated_at timestamp.

**Why this priority**: Marking tasks as complete is core to todo functionality. This is what makes a todo list valuable - tracking what's done. This is P1 because it's essential to the task management workflow.

**Independent Test**: Can be fully tested by creating a task (completed=false), toggling its status to completed=true, toggling again to completed=false, and verifying state changes persist.

**Acceptance Scenarios**:

1. **Given** the user has a pending task (completed=false), **When** they send PATCH `/api/{user_id}/tasks/{id}/complete`, **Then** the system sets completed=true and returns the updated task with new updated_at timestamp
2. **Given** the user has a completed task (completed=true), **When** they send PATCH `/api/{user_id}/tasks/{id}/complete`, **Then** the system sets completed=false and returns the updated task with new updated_at timestamp
3. **Given** the user toggles a task completion status, **When** they request the task list filtered by status, **Then** the task appears in the correct filtered group (pending or completed)
4. **Given** the user tries to toggle a task that doesn't exist, **When** the request is processed, **Then** the system returns an error "Task not found" with 404 status code
5. **Given** user A tries to toggle user B's task, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code
6. **Given** the user_id in the URL does not match the JWT token's user_id, **When** the request is processed, **Then** the system returns an error "Forbidden" with 403 status code

---

### Edge Cases

- What happens when a user has 10,000+ tasks and requests the full list? System returns all tasks but should consider pagination in future (not in scope for this spec)
- What happens when a user tries to create a task with special characters or Unicode in title/description? System accepts and stores UTF-8 characters correctly
- What happens when multiple requests try to update the same task simultaneously? Database transaction isolation ensures last-write-wins behavior with updated_at reflecting the final update
- What happens when a user's JWT token expires while they're viewing their tasks? Next API request with expired token returns 401 and frontend prompts re-login
- What happens when a user is deleted from the database? Foreign key cascade delete removes all their tasks automatically
- What happens when sorting by title with mixed case? System uses case-insensitive sorting (implementation detail: database LOWER() function or application-level sorting)
- What happens when a task has no description (NULL)? API returns empty string or null consistently in JSON response
- What happens when two users create tasks at the exact same time? Each task is associated with the correct user_id and there's no conflict (user_id is part of the data)

## Requirements *(mandatory)*

### Functional Requirements

#### Task Model and Storage

- **FR-001**: System MUST store tasks with the following fields: id (integer, auto-increment primary key), user_id (UUID foreign key to users.id), title (string, max 200 characters), description (string, max 1000 characters, optional), completed (boolean, default false), created_at (timestamp), updated_at (timestamp)
- **FR-002**: System MUST enforce foreign key constraint from tasks.user_id to users.id with CASCADE DELETE behavior (when user is deleted, all their tasks are deleted)
- **FR-003**: System MUST create database indexes on user_id and completed fields for query performance
- **FR-004**: System MUST automatically set created_at timestamp when a task is created
- **FR-005**: System MUST automatically update updated_at timestamp whenever a task is modified

#### Task Creation

- **FR-006**: System MUST provide POST `/api/{user_id}/tasks` endpoint for creating new tasks
- **FR-007**: System MUST require title field for task creation (non-empty, max 200 characters)
- **FR-008**: System MUST accept optional description field (max 1000 characters)
- **FR-009**: System MUST strip leading/trailing whitespace from title and description
- **FR-010**: System MUST associate created task with authenticated user's user_id from JWT token
- **FR-011**: System MUST initialize completed field to false for new tasks
- **FR-012**: System MUST return created task object with 201 status code on success

#### Task Retrieval (List)

- **FR-013**: System MUST provide GET `/api/{user_id}/tasks` endpoint for retrieving user's task list
- **FR-014**: System MUST filter tasks by authenticated user_id (only return tasks belonging to the authenticated user)
- **FR-015**: System MUST support status query parameter with values: "all" (default), "pending" (completed=false), "completed" (completed=true)
- **FR-016**: System MUST support sort query parameter with values: "created" (default, sort by created_at), "title" (sort alphabetically)
- **FR-017**: System MUST support order query parameter with values: "desc" (default), "asc"
- **FR-018**: System MUST combine filtering and sorting (e.g., return completed tasks sorted by title ascending)
- **FR-019**: System MUST return empty array with 200 status when user has no tasks
- **FR-020**: System MUST return all tasks in a single response (pagination not required in this spec)

#### Task Retrieval (Single)

- **FR-021**: System MUST provide GET `/api/{user_id}/tasks/{id}` endpoint for retrieving a single task
- **FR-022**: System MUST verify that the task with the given ID exists
- **FR-023**: System MUST verify that the task belongs to the authenticated user
- **FR-024**: System MUST return complete task object with all fields (id, user_id, title, description, completed, created_at, updated_at)
- **FR-025**: System MUST return 404 status when task doesn't exist
- **FR-026**: System MUST return 403 status when task belongs to a different user (not 404, to prevent enumeration)

#### Task Update

- **FR-027**: System MUST provide PUT `/api/{user_id}/tasks/{id}` endpoint for updating tasks
- **FR-028**: System MUST accept optional title field (if provided, must be non-empty, max 200 characters)
- **FR-029**: System MUST accept optional description field (if provided, max 1000 characters)
- **FR-030**: System MUST require at least one field (title or description) in update request
- **FR-031**: System MUST verify that the task exists and belongs to the authenticated user
- **FR-032**: System MUST update only the provided fields (title, description, or both)
- **FR-033**: System MUST update updated_at timestamp to current time
- **FR-034**: System MUST return updated task object with 200 status code on success

#### Task Deletion

- **FR-035**: System MUST provide DELETE `/api/{user_id}/tasks/{id}` endpoint for deleting tasks
- **FR-036**: System MUST verify that the task exists and belongs to the authenticated user
- **FR-037**: System MUST permanently remove the task from the database
- **FR-038**: System MUST return success message with 200 status code on successful deletion
- **FR-039**: System MUST return 404 status when task doesn't exist
- **FR-040**: System MUST return 403 status when task belongs to a different user

#### Task Completion Toggle

- **FR-041**: System MUST provide PATCH `/api/{user_id}/tasks/{id}/complete` endpoint for toggling completion status
- **FR-042**: System MUST verify that the task exists and belongs to the authenticated user
- **FR-043**: System MUST toggle completed field (false → true, true → false)
- **FR-044**: System MUST update updated_at timestamp to current time
- **FR-045**: System MUST return updated task object with new completion status and 200 status code

#### Authentication and Authorization

- **FR-046**: System MUST require valid JWT token in Authorization header (Bearer scheme) for all task endpoints
- **FR-047**: System MUST extract user_id from JWT token payload using get_current_user_id dependency from Spec 1
- **FR-048**: System MUST validate that user_id in URL path matches user_id from JWT token
- **FR-049**: System MUST return 401 status when JWT token is missing, invalid, or expired
- **FR-050**: System MUST return 403 status when user_id in URL doesn't match JWT token's user_id
- **FR-051**: System MUST return 403 status when user tries to access/modify another user's task (ownership validation)

#### Error Handling and Validation

- **FR-052**: System MUST validate all input fields according to specified constraints (length, required/optional)
- **FR-053**: System MUST return 422 status for validation errors with descriptive messages
- **FR-054**: System MUST return 400 status for malformed requests (invalid JSON, missing required fields in schema)
- **FR-055**: System MUST return consistent error response format: `{"detail": "Error message"}`
- **FR-056**: System MUST handle database errors gracefully and return 500 status with generic error message (not exposing database details)
- **FR-057**: System MUST validate that task_id in URL is a valid integer
- **FR-058**: System MUST validate that status, sort, and order query parameters are valid enum values

#### API Documentation

- **FR-059**: System MUST provide OpenAPI/Swagger documentation at `/docs` endpoint
- **FR-060**: System MUST document all endpoints with request/response schemas, status codes, and examples
- **FR-061**: System MUST document authentication requirements for each endpoint

### Key Entities

- **Task**: Represents a todo item belonging to a user. Contains title (what needs to be done), description (optional details), completion status, ownership (user_id foreign key), and timestamps. Tasks are isolated per user and cannot be shared between users.

- **User** (from Spec 1): Represents an authenticated user account. Tasks reference User via user_id foreign key. User deletion cascades to delete all associated tasks.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new task and receive confirmation in under 5 seconds from button click to task appearing in their list
- **SC-002**: Users can view their complete task list (up to 10,000 tasks) in under 1 second
- **SC-003**: System handles 1,000 concurrent task operations (create, read, update, delete) without errors or performance degradation
- **SC-004**: 100% of task operations verify user ownership (zero incidents of users accessing other users' tasks)
- **SC-005**: 98% of task API requests complete successfully (excluding user errors like invalid input)
- **SC-006**: Users can filter and sort their task list with results returned in under 1 second
- **SC-007**: Task completion toggle updates are reflected immediately (within 1 second) in filtered views
- **SC-008**: System correctly enforces all validation rules with appropriate error messages, resulting in 95% of validation errors being understood and corrected by users on first retry
- **SC-009**: Database queries utilize indexes on user_id and completed fields, maintaining sub-100ms query times even with 10,000+ tasks per user
- **SC-010**: All task operations update the updated_at timestamp consistently within 1 second of system time

## Assumptions

1. **Authentication System**: Spec 1 (001-auth) authentication system is fully implemented and operational, providing JWT token validation via get_current_user_id dependency
2. **User Model**: Users table exists with UUID primary key as defined in Spec 1
3. **Database Performance**: Neon PostgreSQL database provides sufficient performance for single-query operations without requiring complex optimization or caching layers
4. **Concurrent Users**: Expected load is moderate (hundreds to low thousands of concurrent users), not requiring distributed caching or read replicas
5. **Task Volume**: Most users will have fewer than 1,000 tasks, with 10,000 tasks per user as the upper boundary for testing
6. **Pagination**: All tasks returned in a single response is acceptable for this spec; pagination can be added in future if needed
7. **Real-time Updates**: System does not require WebSocket or real-time push notifications for task updates (polling/refresh is acceptable)
8. **Data Retention**: Tasks are retained indefinitely until explicitly deleted by user or cascaded when user is deleted
9. **Character Encoding**: All text fields support UTF-8 encoding for international characters
10. **Sorting Behavior**: Title sorting uses case-insensitive alphabetical order (implementation may use database LOWER() function)
11. **Timestamp Precision**: DateTime fields use standard SQL timestamp precision (microseconds) which is sufficient for ordering and display
12. **Foreign Key Behavior**: Database supports CASCADE DELETE for foreign key constraints (standard in PostgreSQL)
13. **Error Response Format**: FastAPI's default HTTPException detail format is acceptable ({"detail": "message"})
14. **CORS Configuration**: Frontend origin is already configured in backend CORS settings from Spec 1
15. **Environment**: Backend runs on Railway with DATABASE_URL and BETTER_AUTH_SECRET environment variables already configured from Spec 1

## Out of Scope

The following features are explicitly excluded from this specification:

1. **Task Sharing**: Ability to share tasks with other users or make tasks publicly visible
2. **Task Categories/Tags**: Grouping tasks into categories, adding tags, or organizing with labels
3. **Task Due Dates**: Setting deadlines or due dates for tasks
4. **Task Reminders**: Scheduling notifications or reminders for tasks
5. **Task Priority**: Assigning priority levels (high, medium, low) to tasks
6. **Subtasks**: Creating hierarchical task structures with parent/child relationships
7. **Task Attachments**: Uploading files or images associated with tasks
8. **Task Comments**: Adding comments or notes to tasks
9. **Task History**: Tracking edit history or changes over time
10. **Task Search**: Full-text search functionality across task titles and descriptions
11. **Pagination**: Paginated results for large task lists (returns all tasks in one response)
12. **Bulk Operations**: Deleting or updating multiple tasks in a single request
13. **Task Archiving**: Soft-delete or archive functionality (only hard delete supported)
14. **Task Recurrence**: Recurring tasks or templates
15. **Collaboration Features**: Real-time collaborative editing or presence indicators
16. **Import/Export**: Importing tasks from or exporting tasks to external formats (CSV, JSON, etc.)
17. **Frontend UI**: All user interface components (covered in Spec 3)
18. **User Authentication**: Login, signup, JWT token generation (covered in Spec 1)

## Notes

### Integration Dependencies

This specification depends on Spec 1 (001-auth) and must be implemented after Spec 1 is complete. Key integration points:

- **JWT Token Validation**: Uses `get_current_user_id` dependency from `backend/src/core/deps.py`
- **User Model**: Foreign key references User model from `backend/src/models/user.py`
- **Database Connection**: Shares database session from `backend/src/db/session.py`
- **Authentication Secret**: Uses same `BETTER_AUTH_SECRET` environment variable for JWT verification
- **Error Response Format**: Follows same HTTPException pattern as auth endpoints

### Database Schema Notes

The tasks table schema is designed for optimal query performance:

```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Index Justification**:
- `idx_tasks_user_id`: Critical for user-scoped queries (every query filters by user_id)
- `idx_tasks_completed`: Supports status filtering (pending vs completed views)
- Composite index on (user_id, completed) considered but not included - single indexes sufficient for expected query patterns

**Foreign Key Cascade**: CASCADE DELETE ensures automatic cleanup when user is deleted, maintaining referential integrity without orphaned tasks.

### API Design Patterns

All endpoints follow RESTful conventions:

- **Resource**: `/api/{user_id}/tasks` (collection) and `/api/{user_id}/tasks/{id}` (individual resource)
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete), PATCH (partial update)
- **Status Codes**: Follow HTTP standards (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error)
- **Content Type**: JSON for all requests and responses
- **Authentication**: JWT Bearer token in Authorization header

**URL Pattern Rationale**: Including `{user_id}` in URL path makes ownership explicit and enables URL-based authorization validation before database queries.

### Security Considerations

1. **User Enumeration Prevention**: When a task doesn't exist OR belongs to another user, return 403 Forbidden (not 404) to prevent attackers from determining which task IDs exist
2. **Authorization Chain**: Validate JWT → Extract user_id → Verify URL user_id match → Verify task ownership (for task-specific operations)
3. **Input Sanitization**: Strip whitespace from title/description to prevent storage bloat and display issues
4. **SQL Injection**: SQLModel ORM with parameterized queries prevents SQL injection attacks
5. **Rate Limiting**: Not included in this spec but should be considered for production (prevent abuse of create/update/delete endpoints)

### Frontend Integration Preview (Spec 3)

While frontend UI is out of scope, this API is designed to support the following frontend features:

- Task list view with filter tabs (All, Pending, Completed)
- Sort dropdown (Creation Date, Alphabetical)
- Task creation form (title required, description optional)
- Inline task editing
- Delete confirmation dialog
- Checkbox toggle for completion status
- Real-time error feedback on validation errors

Frontend will consume this API via `frontend/src/lib/api.ts` API client module.

### Testing Strategy Notes

Each endpoint will require:

- **Unit Tests**: Validate request/response schemas, business logic, error handling
- **Integration Tests**: Full request/response cycle with database, test user ownership validation
- **Security Tests**: Attempt cross-user access, verify JWT validation, test authorization failures
- **Performance Tests**: Bulk data scenarios (1000+ tasks), concurrent request handling
- **Edge Cases**: Empty lists, maximum field lengths, special characters, concurrent updates

Test data should include multiple users with varying numbers of tasks to validate isolation.

### Implementation Order Recommendation

Suggested implementation sequence for maximum value delivery:

1. **Phase 1**: Task model + Create task (FR-001 to FR-012) - Enables basic task entry
2. **Phase 2**: List tasks with filtering (FR-013 to FR-020) - Enables viewing created tasks
3. **Phase 3**: Toggle completion (FR-041 to FR-045) - Enables core "mark as done" workflow
4. **Phase 4**: Update task + Delete task (FR-027 to FR-040) - Enables task management
5. **Phase 5**: View single task (FR-021 to FR-026) - Completes CRUD operations

This order delivers a functional todo app after Phase 3, with Phases 4-5 adding convenience features.
