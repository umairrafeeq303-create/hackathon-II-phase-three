# Feature Specification: Frontend UI & API Integration

**Feature Branch**: `003-frontend-ui`
**Created**: 2026-01-09
**Status**: Draft
**Input**: Frontend UI & API Integration - Next.js authentication and task management interface

## Overview

This specification defines the Next.js 14+ frontend application that provides a complete user interface for authentication and task management. This is Spec 3 of 3 total specifications for Phase II of the Todo Full-Stack Web Application.

**Purpose**: Create a responsive, user-friendly web interface that integrates with the authentication system (Spec 1) and task CRUD API (Spec 2) to enable users to manage their personal tasks through an intuitive dashboard.

**Key Stakeholders**:
- End users (need intuitive task management interface)
- Frontend application (Next.js 14+ with App Router, TypeScript, Tailwind CSS)
- Backend API (FastAPI endpoints from Spec 1 & 2)
- Better Auth (authentication integration)

**Integration Points**:
- **With Spec 1 (Auth)**: Uses Better Auth for signup/signin, manages JWT tokens, implements protected routes
- **With Spec 2 (Task API)**: Consumes all 6 task CRUD endpoints, handles API responses, manages task state

**Success Criteria**:
- Users can complete signup and login flows in under 60 seconds
- Task list loads in under 1 second on initial page visit
- All user interactions provide immediate feedback (loading states, success/error messages)
- Application is fully responsive on mobile (>= 375px), tablet (>= 768px), and desktop (>= 1024px)
- 95% of user actions succeed without errors (proper error handling)
- Zero unauthorized access to other users' tasks (client-side enforcement + backend validation)
- Task CRUD operations complete with visual confirmation in under 2 seconds

## User Scenarios & Testing *(mandatory)*

### User Story 1 - New User Signup and Onboarding (Priority: P1)

A new user visits the application and wants to create an account. They navigate to the signup page, enter their name, email, and password, submit the form, and are automatically logged in and redirected to an empty task dashboard with a welcome message.

**Why this priority**: User registration is the entry point to the application. Without this flow, users cannot access any features. This establishes the foundation for all subsequent user stories.

**Independent Test**: Can be fully tested by filling out the signup form with valid credentials, submitting it, and verifying that the user is redirected to the dashboard with an authenticated session and their name displayed in the header.

**Acceptance Scenarios**:

1. **Given** a new user visits the `/signup` page, **When** they enter name "John Doe", email "john@example.com", and password "SecurePass123", **Then** the system creates their account, stores a JWT token, and redirects them to the dashboard (`/`)
2. **Given** a user is on the signup form, **When** they submit without filling required fields, **Then** validation errors appear below each empty field in red text
3. **Given** a user enters an email that already exists, **When** they submit the form, **Then** an error message "Email already registered" appears at the top of the form
4. **Given** a user enters a password with only 6 characters, **When** they submit the form, **Then** an error message "Password must be at least 8 characters" appears below the password field
5. **Given** a user enters an invalid email format (missing @), **When** they submit the form, **Then** an error message "Invalid email format" appears below the email field
6. **Given** a user is filling out the signup form, **When** they click the submit button, **Then** the button text changes to "Creating account..." and is disabled until the request completes
7. **Given** a user successfully creates an account, **When** they land on the dashboard, **Then** they see a welcome message "Welcome, [Name]! Create your first task to get started."

---

### User Story 2 - Returning User Login (Priority: P1)

A registered user returns to the application and wants to access their tasks. They navigate to the login page, enter their email and password, submit the form, and are redirected to their task dashboard showing their existing tasks.

**Why this priority**: Login is equally critical to signup. Users must be able to return to their accounts to access their saved tasks. This is P1 because it's required for all task management features.

**Independent Test**: Can be fully tested by logging in with existing credentials and verifying that the user is redirected to the dashboard with their tasks displayed and their session persisted.

**Acceptance Scenarios**:

1. **Given** a registered user visits the `/login` page, **When** they enter their correct email and password, **Then** the system authenticates them, stores a JWT token, and redirects them to the dashboard with their tasks loaded
2. **Given** a user enters an incorrect password, **When** they submit the form, **Then** an error message "Invalid email or password" appears at the top of the form (no indication of which field is wrong for security)
3. **Given** a user enters an email that doesn't exist, **When** they submit the form, **Then** the same error message "Invalid email or password" appears (consistent with wrong password for security)
4. **Given** a user is on the login page, **When** they click "Don't have an account? Sign up", **Then** they are navigated to the `/signup` page
5. **Given** an authenticated user tries to access the `/login` page, **When** the page loads, **Then** they are immediately redirected to the dashboard (`/`)
6. **Given** a user submits the login form, **When** the request is processing, **Then** the submit button displays "Signing in..." and is disabled

---

### User Story 3 - View Task Dashboard (Priority: P1)

An authenticated user lands on their task dashboard and wants to see all their tasks. The dashboard displays a list of all their tasks with title, description preview, completion status, and action buttons. Empty states are shown if no tasks exist.

**Why this priority**: Viewing tasks is the core value proposition of the application. This must be P1 because it's the primary interface users interact with and is required immediately after authentication.

**Independent Test**: Can be fully tested by logging in as a user with existing tasks and verifying that all tasks are displayed in the correct order with proper formatting and action buttons visible.

**Acceptance Scenarios**:

1. **Given** a user has 5 tasks (3 pending, 2 completed), **When** they visit the dashboard, **Then** all 5 tasks are displayed in a list sorted by creation date (newest first)
2. **Given** a user has no tasks, **When** they visit the dashboard, **Then** they see an empty state message "No tasks yet. Create your first task to get started!" with a prominent "Create Task" button
3. **Given** a user is on the dashboard, **When** the task list is loading, **Then** they see 3 skeleton loading placeholders indicating data is being fetched
4. **Given** a user's tasks fail to load due to network error, **When** the error occurs, **Then** they see an error message "Failed to load tasks. Please try again." with a "Retry" button
5. **Given** a completed task in the list, **When** the user views it, **Then** the task title has a strikethrough style and the checkbox is checked
6. **Given** a pending task in the list, **When** the user views it, **Then** the task title has normal styling and the checkbox is unchecked
7. **Given** a user is viewing the dashboard, **When** they see the header, **Then** it displays their name, a logout button, and the dashboard title

---

### User Story 4 - Create New Task (Priority: P1)

An authenticated user wants to add a new task. They click the "Create Task" button, a modal/form appears with title and description inputs, they fill in the details, submit, and the new task immediately appears at the top of their task list.

**Why this priority**: Task creation is the primary action users take in the application. Without the ability to create tasks, the application has no value. This is P1 and must be fully functional for MVP.

**Independent Test**: Can be fully tested by clicking the create button, filling out the form with a title and description, submitting, and verifying that the task appears in the list and the database contains the new record.

**Acceptance Scenarios**:

1. **Given** a user is on the dashboard, **When** they click the "Create Task" button, **Then** a task creation form/modal appears with title and description inputs
2. **Given** the task creation form is open, **When** the user enters title "Buy groceries" and description "Milk, bread, eggs", **Then** both fields accept the input and display character counts (title: 14/200, description: 17/1000)
3. **Given** the user fills in only the title field, **When** they submit, **Then** the task is created with the title and an empty description
4. **Given** the user tries to submit without a title, **When** they click submit, **Then** an error message "Title is required" appears below the title field and the form is not submitted
5. **Given** the user enters a title with 201 characters, **When** they reach the limit, **Then** the title input stops accepting characters and displays an error "Title must be 200 characters or less"
6. **Given** the user successfully creates a task, **When** the API responds, **Then** the task appears at the top of the list, the form closes, and a success message "Task created successfully" appears briefly
7. **Given** the user is submitting a task, **When** the API request is in progress, **Then** the submit button displays "Creating..." and is disabled

---

### User Story 5 - Toggle Task Completion (Priority: P1)

An authenticated user wants to mark a task as complete or reopen a completed task. They click the checkbox next to a task, the system updates the backend, and the task's visual styling changes immediately to reflect the new status.

**Why this priority**: Task completion is a core interaction in any todo application. Users must be able to mark tasks done to track progress. This is P1 for MVP functionality.

**Independent Test**: Can be fully tested by clicking a task's checkbox, verifying the API call succeeds, and confirming the task's completed status changes both visually and in the database.

**Acceptance Scenarios**:

1. **Given** a user has a pending task, **When** they click the checkbox, **Then** the task is marked as completed, the title gets a strikethrough, and the checkbox becomes checked
2. **Given** a user has a completed task, **When** they click the checkbox, **Then** the task is marked as pending, the strikethrough is removed, and the checkbox becomes unchecked
3. **Given** a user toggles a task's completion, **When** the API request is processing, **Then** the checkbox shows a loading spinner to indicate the action is in progress
4. **Given** a user toggles a task but the API request fails, **When** the error occurs, **Then** the task's status reverts to its original state and an error message "Failed to update task" appears
5. **Given** a user toggles multiple tasks quickly, **When** the API requests are queued, **Then** each task shows its own loading state and updates independently as responses arrive

---

### User Story 6 - Filter and Sort Tasks (Priority: P1)

An authenticated user wants to organize their task view by filtering by completion status and sorting by different criteria. They use dropdown filters to show only pending/completed tasks and sort by creation date or title alphabetically.

**Why this priority**: As users accumulate tasks, filtering and sorting become essential for task management. This is P1 because it's critical for usability once users have more than a few tasks.

**Independent Test**: Can be fully tested by creating multiple tasks, then applying different filter and sort combinations and verifying that the task list updates correctly with the appropriate subset and order.

**Acceptance Scenarios**:

1. **Given** a user has both pending and completed tasks, **When** they select "Pending" from the status filter dropdown, **Then** only tasks with completed=false are displayed
2. **Given** a user has filtered to show only completed tasks, **When** they select "All" from the status filter, **Then** all tasks (both pending and completed) are displayed again
3. **Given** a user is viewing all tasks, **When** they select "Title (A-Z)" from the sort dropdown, **Then** tasks are reordered alphabetically by title in ascending order
4. **Given** a user has sorted by title, **When** they select "Created Date (Newest)" from the sort dropdown, **Then** tasks are reordered by creation date with newest first
5. **Given** a user applies a filter, **When** the task list updates, **Then** a brief loading indicator appears and the filtered results replace the current list smoothly
6. **Given** a user has active filters, **When** they click "Clear Filters", **Then** all filters reset to default (All tasks, sorted by creation date descending)

---

### User Story 7 - Edit Task (Priority: P2)

An authenticated user wants to modify an existing task's title or description. They click an "Edit" button on a task, a form pre-populated with current values appears, they make changes, submit, and the task updates in the list.

**Why this priority**: Task editing is important for maintaining accurate task information but is secondary to creating and viewing tasks. Users can work around this by deleting and recreating tasks if needed, making this P2.

**Independent Test**: Can be fully tested by clicking edit on a task, modifying its title or description, submitting, and verifying that the changes are reflected in the task list and database.

**Acceptance Scenarios**:

1. **Given** a user sees a task in their list, **When** they click the "Edit" icon/button, **Then** a modal/form appears with the task's current title and description pre-filled in the inputs
2. **Given** the edit form is open, **When** the user changes the title from "Buy groceries" to "Buy weekly groceries", **Then** the input accepts the new value and displays the updated character count
3. **Given** the user edits only the description, **When** they submit, **Then** only the description is updated and the title remains unchanged
4. **Given** the user clears the title field, **When** they try to submit, **Then** an error message "Title is required" prevents submission
5. **Given** the user successfully updates a task, **When** the API responds, **Then** the modal closes, the task list shows the updated values, and a success message "Task updated successfully" appears briefly
6. **Given** the user opens the edit form, **When** they click "Cancel", **Then** the modal closes and no changes are made to the task

---

### User Story 8 - Delete Task (Priority: P2)

An authenticated user wants to permanently remove a task. They click a "Delete" button on a task, a confirmation dialog appears to prevent accidental deletion, they confirm, and the task is removed from the list and database.

**Why this priority**: Task deletion is important for task management but is lower priority than creation, viewing, and completion. Users can leave unwanted tasks unchecked if deletion isn't available, making this P2.

**Independent Test**: Can be fully tested by clicking delete on a task, confirming the deletion in the dialog, and verifying that the task is removed from both the UI and database.

**Acceptance Scenarios**:

1. **Given** a user sees a task in their list, **When** they click the "Delete" icon/button, **Then** a confirmation modal appears with the message "Are you sure you want to delete '[Task Title]'?"
2. **Given** the delete confirmation modal is open, **When** the user clicks "Cancel", **Then** the modal closes and the task remains in the list
3. **Given** the delete confirmation modal is open, **When** the user clicks "Delete" to confirm, **Then** the API request is sent, the modal shows a loading state with "Deleting..." button text
4. **Given** the user confirms deletion, **When** the API responds successfully, **Then** the task is immediately removed from the list with a fade-out animation and a success message "Task deleted successfully" appears
5. **Given** the user tries to delete a task but the API request fails, **When** the error occurs, **Then** the task remains in the list and an error message "Failed to delete task. Please try again." appears

---

### User Story 9 - User Logout (Priority: P2)

An authenticated user wants to end their session and log out. They click the "Logout" button in the header, their session is cleared, and they are redirected to the login page.

**Why this priority**: Logout is important for security and account switching but is secondary to core task management features. Users can simply close the browser tab if logout isn't available, making this P2.

**Independent Test**: Can be fully tested by clicking the logout button and verifying that the JWT token is cleared from storage, the user is redirected to the login page, and attempting to access the dashboard redirects back to login.

**Acceptance Scenarios**:

1. **Given** a user is logged in and viewing the dashboard, **When** they click the "Logout" button in the header, **Then** their session is cleared, JWT token is removed from storage, and they are redirected to the `/login` page
2. **Given** a user has just logged out, **When** they try to navigate back to the dashboard, **Then** they are immediately redirected to the login page because they are not authenticated
3. **Given** a user clicks logout, **When** the action is processing, **Then** the logout button displays "Logging out..." briefly before the redirect

---

### Edge Cases

- **Network timeout during task creation**: System shows error message "Request timed out. Please try again." and allows user to retry
- **JWT token expires while user is active**: On next API call, receive 401 response, clear token, redirect to login with message "Your session has expired. Please log in again."
- **User creates 100+ tasks**: List remains performant with virtual scrolling or pagination implemented on backend
- **Task title/description contains special characters (emojis, HTML tags)**: Content is properly sanitized and displayed safely without XSS vulnerabilities
- **User rapidly clicks action buttons (create, delete, toggle)**: Buttons are disabled during API calls to prevent duplicate requests
- **Browser back button during form submission**: Form state is preserved or user is warned about unsaved changes
- **User closes browser before task creation completes**: On next visit, task may or may not appear depending on when the API request completed (eventual consistency acceptable)
- **Multiple browser tabs open with same session**: State synchronization is not required (users see stale data until page refresh) - acceptable for MVP
- **User tries to access dashboard without authentication**: Immediately redirected to login page with no flash of content

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication UI

- **FR-001**: System MUST provide a signup page at `/signup` with name, email, and password inputs that integrate with Better Auth
- **FR-002**: System MUST provide a login page at `/login` with email and password inputs that integrate with Better Auth
- **FR-003**: System MUST validate email format client-side before submission (must contain @ and domain)
- **FR-004**: System MUST validate password length client-side (minimum 8 characters)
- **FR-005**: System MUST display validation errors below each input field in red text
- **FR-006**: System MUST show loading states on form submit buttons ("Creating account...", "Signing in...")
- **FR-007**: System MUST automatically redirect authenticated users away from `/login` and `/signup` pages to the dashboard
- **FR-008**: System MUST provide links between signup and login pages for easy navigation

#### JWT Token Management

- **FR-009**: System MUST store JWT tokens obtained from Better Auth in a secure, HTTP-only cookie or local storage
- **FR-010**: System MUST attach JWT token to Authorization header of all API requests to backend (format: `Bearer {token}`)
- **FR-011**: System MUST handle 401 Unauthorized responses by clearing token and redirecting to login
- **FR-012**: System MUST extract user ID from JWT token to construct API endpoint URLs (`/api/{user_id}/tasks`)
- **FR-013**: System MUST refresh user session on page load if valid token exists

#### Protected Routes

- **FR-014**: System MUST redirect unauthenticated users from the dashboard (`/`) to the login page
- **FR-015**: System MUST show a loading spinner during authentication check before rendering protected pages
- **FR-016**: System MUST persist user session across page refreshes and browser restarts (until token expires)

#### Dashboard Layout

- **FR-017**: System MUST display a header with user's name, logout button, and application title
- **FR-018**: System MUST display a prominent "Create Task" button above the task list
- **FR-019**: System MUST display filter controls (status dropdown, sort dropdown, clear button) above the task list
- **FR-020**: System MUST display task list or empty state based on task count

#### Task Display

- **FR-021**: System MUST fetch all user's tasks on dashboard load by calling GET `/api/{user_id}/tasks`
- **FR-022**: System MUST display each task with: checkbox, title, description preview (truncated to 100 characters), edit button, delete button
- **FR-023**: System MUST apply strikethrough styling to completed task titles
- **FR-024**: System MUST show checked checkboxes for completed tasks and unchecked for pending tasks
- **FR-025**: System MUST display an empty state message when user has no tasks: "No tasks yet. Create your first task to get started!"
- **FR-026**: System MUST show skeleton loading placeholders (3 items) while tasks are being fetched

#### Task Creation

- **FR-027**: System MUST open a modal/form when "Create Task" button is clicked
- **FR-028**: System MUST provide title input (required, max 200 characters) with character counter
- **FR-029**: System MUST provide description textarea (optional, max 1000 characters) with character counter
- **FR-030**: System MUST validate that title is not empty before submission
- **FR-031**: System MUST send POST request to `/api/{user_id}/tasks` with title and description
- **FR-032**: System MUST add newly created task to the top of the task list immediately after API success
- **FR-033**: System MUST close the form and show success message "Task created successfully" after creation
- **FR-034**: System MUST prevent form submission while API request is in progress (disable submit button)

#### Task Completion Toggle

- **FR-035**: System MUST toggle task completion when checkbox is clicked
- **FR-036**: System MUST send PATCH request to `/api/{user_id}/tasks/{task_id}/toggle` when checkbox is clicked
- **FR-037**: System MUST show loading spinner on checkbox during API request
- **FR-038**: System MUST update task styling immediately after API success (add/remove strikethrough)
- **FR-039**: System MUST revert checkbox state if API request fails and show error message

#### Task Filtering

- **FR-040**: System MUST provide status filter dropdown with options: All, Pending, Completed
- **FR-041**: System MUST call GET `/api/{user_id}/tasks?status={all|pending|completed}` when status filter changes
- **FR-042**: System MUST update task list to show only filtered tasks
- **FR-043**: System MUST show loading indicator during filter application

#### Task Sorting

- **FR-044**: System MUST provide sort dropdown with options: Created Date (Newest), Created Date (Oldest), Title (A-Z), Title (Z-A)
- **FR-045**: System MUST call GET `/api/{user_id}/tasks?sort={created|title}&order={asc|desc}` when sort changes
- **FR-046**: System MUST reorder task list based on selected sort criteria

#### Task Editing

- **FR-047**: System MUST open edit modal/form when edit button is clicked on a task
- **FR-048**: System MUST pre-populate form inputs with current task title and description
- **FR-049**: System MUST validate title is not empty before submission
- **FR-050**: System MUST send PUT request to `/api/{user_id}/tasks/{task_id}` with updated fields
- **FR-051**: System MUST update task in the list immediately after API success
- **FR-052**: System MUST close form and show success message "Task updated successfully"

#### Task Deletion

- **FR-053**: System MUST open confirmation modal when delete button is clicked
- **FR-054**: System MUST display task title in confirmation message: "Are you sure you want to delete '[Task Title]'?"
- **FR-055**: System MUST provide Cancel and Delete buttons in confirmation modal
- **FR-056**: System MUST send DELETE request to `/api/{user_id}/tasks/{task_id}` when user confirms
- **FR-057**: System MUST remove task from list immediately after API success with fade-out animation
- **FR-058**: System MUST show success message "Task deleted successfully"

#### Error Handling

- **FR-059**: System MUST display user-friendly error messages for all API failures
- **FR-060**: System MUST handle network timeout errors with message "Request timed out. Please try again."
- **FR-061**: System MUST handle 500 server errors with message "Server error. Please try again later."
- **FR-062**: System MUST handle 403 forbidden errors with message "You don't have permission to access this resource."
- **FR-063**: System MUST log all errors to browser console for debugging

#### Responsive Design

- **FR-064**: System MUST be fully functional on mobile devices (>= 375px width)
- **FR-065**: System MUST stack task list items vertically on all screen sizes
- **FR-066**: System MUST show hamburger menu icon on mobile (<640px) instead of desktop header layout
- **FR-067**: System MUST render full-width forms on mobile and centered modals on desktop

#### Loading States

- **FR-068**: System MUST show loading spinner in submit buttons during form submission
- **FR-069**: System MUST show skeleton loaders during initial task list load
- **FR-070**: System MUST disable action buttons (create, edit, delete, toggle) while requests are processing
- **FR-071**: System MUST show loading spinner in checkbox during toggle request

### Key Entities

- **User**: Authenticated user with id (UUID from JWT), email, and name. Represented by Better Auth session.
- **Task**: Todo item with id (number), user_id (UUID), title (string, max 200), description (optional string, max 1000), completed (boolean), created_at (ISO datetime), updated_at (ISO datetime)
- **TaskFilters**: Current filter state with status (all|pending|completed), sort (created|title), order (asc|desc)
- **Session**: Authentication state containing JWT token and user information from Better Auth

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete the entire signup flow (form fill, validation, submission, redirect) in under 60 seconds
- **SC-002**: Task dashboard loads and displays task list within 1 second of navigation on broadband connection
- **SC-003**: All user interactions (button clicks, form submissions) provide visual feedback within 100 milliseconds
- **SC-004**: Application is fully responsive and functional on screen widths from 375px (mobile) to 2560px (large desktop)
- **SC-005**: 95% of API calls complete successfully with proper error handling and user feedback
- **SC-006**: Task creation, update, and deletion operations complete with visual confirmation in under 2 seconds
- **SC-007**: Zero instances of users accessing tasks that don't belong to them (enforced by client redirect + backend validation)
- **SC-008**: Users can perform all core actions (create, view, toggle, filter) without encountering blocking errors
- **SC-009**: Authenticated sessions persist across browser tabs and page refreshes until token expiry
- **SC-010**: Loading states are displayed for all asynchronous operations to prevent user confusion

## Assumptions

- Better Auth is properly configured with JWT plugin and BETTER_AUTH_SECRET matches backend configuration
- Backend API (Spec 1 & 2) is fully implemented and accessible at configured NEXT_PUBLIC_API_URL
- CORS is configured on backend to allow requests from frontend origin
- JWT tokens have 7-day expiration (as specified in Spec 1)
- Users have modern browsers with JavaScript enabled (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Network latency is reasonable (<500ms for API calls under normal conditions)
- Tasks are fetched fresh on each dashboard visit (no client-side caching beyond component state)
- Multiple tabs with same session can have stale data (no real-time synchronization required)
- Users accept that tasks may take up to 2 seconds to appear after creation due to API latency
- Mobile users have touch-capable devices with minimum 375px viewport width
- Tailwind CSS v3+ is installed and configured in the Next.js project
- TypeScript is enforced with strict type checking enabled
