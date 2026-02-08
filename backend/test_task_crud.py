#!/usr/bin/env python3
"""
Test script for Task CRUD API endpoints.
Tests all 6 endpoints with authentication and various scenarios.
"""
import requests
import json
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:8000"

# Test user credentials (assuming user already exists from 001-auth)
TEST_EMAIL = "testcrud2@example.com"
TEST_PASSWORD = "TestCrud123"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(test_name):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST: {test_name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def signup_user():
    """Sign up a new test user."""
    print_test("Sign up new test user")
    response = requests.post(
        f"{BASE_URL}/api/auth/signup",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "name": "Test User"
        }
    )
    if response.status_code in [200, 201]:
        print_success("User created successfully")
        return True
    elif response.status_code == 400 and "already exists" in response.text.lower():
        print_success("User already exists, continuing...")
        return True
    else:
        print_error(f"Signup failed: {response.status_code} - {response.text}")
        return False

def login_user():
    """Login and get JWT token."""
    print_test("Login to get JWT token")
    response = requests.post(
        f"{BASE_URL}/api/auth/signin",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    if response.status_code == 200:
        data = response.json()
        token = data.get("token")  # Changed from access_token to token
        user_id = data.get("user", {}).get("id")
        print_success(f"Logged in successfully. User ID: {user_id}")
        return token, user_id
    else:
        print_error(f"Login failed: {response.status_code} - {response.text}")
        return None, None

def test_create_task(token, user_id):
    """Test creating a task."""
    print_test("Create Task (POST /api/{user_id}/tasks)")

    headers = {"Authorization": f"Bearer {token}"}
    task_data = {
        "title": "Test Task - Buy groceries",
        "description": "Milk, eggs, bread"
    }

    response = requests.post(
        f"{BASE_URL}/api/{user_id}/tasks/",
        json=task_data,
        headers=headers
    )

    if response.status_code == 201:
        task = response.json()
        print_success(f"Task created successfully")
        print(f"  ID: {task['id']}")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Completed: {task['completed']}")
        print(f"  Created: {task['created_at']}")
        return task['id']
    else:
        print_error(f"Create failed: {response.status_code} - {response.text}")
        return None

def test_list_tasks(token, user_id):
    """Test listing all tasks."""
    print_test("List All Tasks (GET /api/{user_id}/tasks)")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/{user_id}/tasks/",
        headers=headers
    )

    if response.status_code == 200:
        tasks = response.json()
        print_success(f"Listed {len(tasks)} task(s)")
        for task in tasks:
            print(f"  - [{task['id']}] {task['title']} (completed: {task['completed']})")
        return tasks
    else:
        print_error(f"List failed: {response.status_code} - {response.text}")
        return []

def test_list_tasks_filtered(token, user_id, status):
    """Test listing tasks with status filter."""
    print_test(f"List Tasks with Status Filter (status={status})")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/{user_id}/tasks/?status={status}",
        headers=headers
    )

    if response.status_code == 200:
        tasks = response.json()
        print_success(f"Listed {len(tasks)} {status} task(s)")
        for task in tasks:
            print(f"  - [{task['id']}] {task['title']} (completed: {task['completed']})")
        return tasks
    else:
        print_error(f"List filtered failed: {response.status_code} - {response.text}")
        return []

def test_get_task(token, user_id, task_id):
    """Test getting a single task."""
    print_test(f"Get Single Task (GET /api/{user_id}/tasks/{task_id})")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
        headers=headers
    )

    if response.status_code == 200:
        task = response.json()
        print_success(f"Retrieved task {task_id}")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Completed: {task['completed']}")
        return task
    else:
        print_error(f"Get task failed: {response.status_code} - {response.text}")
        return None

def test_update_task(token, user_id, task_id):
    """Test updating a task."""
    print_test(f"Update Task (PUT /api/{user_id}/tasks/{task_id})")

    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "title": "Test Task - Buy groceries and milk (UPDATED)",
        "description": "Milk, eggs, bread, butter"
    }

    response = requests.put(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
        json=update_data,
        headers=headers
    )

    if response.status_code == 200:
        task = response.json()
        print_success(f"Task {task_id} updated successfully")
        print(f"  New Title: {task['title']}")
        print(f"  New Description: {task['description']}")
        print(f"  Updated At: {task['updated_at']}")
        return task
    else:
        print_error(f"Update failed: {response.status_code} - {response.text}")
        return None

def test_toggle_completion(token, user_id, task_id):
    """Test toggling task completion."""
    print_test(f"Toggle Completion (PATCH /api/{user_id}/tasks/{task_id}/complete)")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}/complete",
        headers=headers
    )

    if response.status_code == 200:
        task = response.json()
        print_success(f"Task {task_id} completion toggled")
        print(f"  Completed: {task['completed']}")
        print(f"  Updated At: {task['updated_at']}")
        return task
    else:
        print_error(f"Toggle failed: {response.status_code} - {response.text}")
        return None

def test_delete_task(token, user_id, task_id):
    """Test deleting a task."""
    print_test(f"Delete Task (DELETE /api/{user_id}/tasks/{task_id})")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
        headers=headers
    )

    if response.status_code == 200:
        result = response.json()
        print_success(f"Task {task_id} deleted successfully")
        print(f"  Message: {result['message']}")
        return True
    else:
        print_error(f"Delete failed: {response.status_code} - {response.text}")
        return False

def test_sorting(token, user_id):
    """Test sorting functionality."""
    print_test("Test Sorting (sort=title&order=asc)")

    # Create multiple tasks
    headers = {"Authorization": f"Bearer {token}"}
    titles = ["Zebra task", "Apple task", "Banana task"]
    created_ids = []

    for title in titles:
        response = requests.post(
            f"{BASE_URL}/api/{user_id}/tasks/",
            json={"title": title},
            headers=headers
        )
        if response.status_code == 201:
            created_ids.append(response.json()['id'])

    print_success(f"Created {len(created_ids)} test tasks for sorting")

    # Test sorting by title ascending
    response = requests.get(
        f"{BASE_URL}/api/{user_id}/tasks/?sort=title&order=asc",
        headers=headers
    )

    if response.status_code == 200:
        tasks = response.json()
        print_success("Tasks sorted by title (ascending):")
        for task in tasks:
            print(f"  - {task['title']}")

        # Cleanup
        for task_id in created_ids:
            requests.delete(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)

        return True
    else:
        print_error(f"Sorting test failed: {response.status_code}")
        return False

def run_all_tests():
    """Run all tests in sequence."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Task CRUD API Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    # Sign up user (if needed)
    signup_user()

    # Login
    token, user_id = login_user()
    if not token or not user_id:
        print_error("Cannot proceed without authentication")
        return

    # Test 1: Create task
    task_id = test_create_task(token, user_id)
    if not task_id:
        print_error("Cannot proceed without creating a task")
        return

    # Test 2: List all tasks
    test_list_tasks(token, user_id)

    # Test 3: Get single task
    test_get_task(token, user_id, task_id)

    # Test 4: Update task
    test_update_task(token, user_id, task_id)

    # Test 5: Toggle completion (mark as complete)
    test_toggle_completion(token, user_id, task_id)

    # Test 6: List completed tasks
    test_list_tasks_filtered(token, user_id, "completed")

    # Test 7: Toggle completion again (mark as incomplete)
    test_toggle_completion(token, user_id, task_id)

    # Test 8: List pending tasks
    test_list_tasks_filtered(token, user_id, "pending")

    # Test 9: Test sorting
    test_sorting(token, user_id)

    # Test 10: Delete task
    test_delete_task(token, user_id, task_id)

    # Test 11: Verify deletion
    print_test(f"Verify Deletion (GET /api/{user_id}/tasks/{task_id} should return 404)")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
    if response.status_code == 404:
        print_success("Task successfully deleted (404 returned)")
    else:
        print_error(f"Expected 404, got {response.status_code}")

    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{GREEN}All tests completed!{RESET}")
    print(f"{GREEN}{'='*60}{RESET}\n")

if __name__ == "__main__":
    run_all_tests()
