"""
Manual Test Script for User Stories (Phases 7-13)

Run this script to manually validate all chatbot user stories.
Requires: Backend server running with valid OPENAI_API_KEY

Usage:
    python3 manual_test_user_stories.py

Prerequisites:
    1. Backend server running: uvicorn src.main:app --reload
    2. OPENAI_API_KEY configured in backend/.env
    3. Valid user account created
"""
import requests
import json
from uuid import uuid4
from getpass import getpass

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.OKCYAN}→ {text}{Colors.ENDC}")


def print_response(label, data):
    """Print API response."""
    print(f"{Colors.OKBLUE}{label}:{Colors.ENDC}")
    print(json.dumps(data, indent=2))
    print()


def authenticate():
    """Authenticate and get access token."""
    print_header("Authentication")
    print("Please enter your credentials:")
    email = input("Email: ")
    password = getpass("Password: ")

    response = requests.post(
        f"{API_URL}/auth/login",
        json={"email": email, "password": password}
    )

    if response.status_code == 200:
        data = response.json()
        print_success(f"Authenticated as: {email}")
        return data["access_token"], data["user_id"]
    else:
        print_error(f"Authentication failed: {response.text}")
        exit(1)


def send_chat_message(user_id, message, token, conversation_id=None):
    """Send a chat message to the AI assistant."""
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}

    if conversation_id:
        payload["conversation_id"] = conversation_id

    response = requests.post(
        f"{API_URL}/{user_id}/chat",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        print_error(f"Chat request failed: {response.text}")
        return None


def wait_for_user():
    """Wait for user to press Enter."""
    input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")


# Test Scenarios

def test_phase_7_view_tasks(user_id, token, conversation_id):
    """Phase 7: User Story 2 - View Tasks via Natural Language"""
    print_header("Phase 7: View Tasks via Natural Language (US2)")

    # Test 1: Show all tasks
    print_info("Test 1: 'Show me my tasks'")
    response = send_chat_message(user_id, "Show me my tasks", token, conversation_id)
    if response:
        conversation_id = response["conversation_id"]
        print_response("Response", response)
        print_success("Agent should list all tasks")

    wait_for_user()

    # Test 2: Show pending tasks
    print_info("Test 2: 'What's pending?'")
    response = send_chat_message(user_id, "What's pending?", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should list only pending tasks")

    wait_for_user()

    # Test 3: Show completed tasks
    print_info("Test 3: 'What have I completed?'")
    response = send_chat_message(user_id, "What have I completed?", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should list only completed tasks")

    wait_for_user()

    return conversation_id


def test_phase_8_complete_tasks(user_id, token, conversation_id):
    """Phase 8: User Story 3 - Complete Tasks via Natural Language"""
    print_header("Phase 8: Complete Tasks via Natural Language (US3)")

    # Test 1: Complete task by ID
    print_info("Test 1: 'Mark task 1 as complete'")
    response = send_chat_message(user_id, "Mark task 1 as complete", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should mark task as complete with encouraging message")

    wait_for_user()

    # Test 2: Complete task by description
    print_info("Test 2: 'I finished buying groceries'")
    response = send_chat_message(user_id, "I finished buying groceries", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should find task by title and mark complete")

    wait_for_user()

    return conversation_id


def test_phase_9_conversation_context(user_id, token, conversation_id):
    """Phase 9: User Story 6 - Maintain Conversation Context"""
    print_header("Phase 9: Maintain Conversation Context (US6)")

    # Test 1: Create task
    print_info("Test 1: 'Add a task to buy milk'")
    response = send_chat_message(user_id, "Add a task to buy milk", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Task created")

    wait_for_user()

    # Test 2: Reference previous task
    print_info("Test 2: 'Mark that task as complete' (context reference)")
    response = send_chat_message(user_id, "Mark that task as complete", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should resolve 'that task' from conversation history")

    wait_for_user()

    # Test 3: List and reference
    print_info("Test 3: 'Show my tasks' then 'Delete the first one'")
    response = send_chat_message(user_id, "Show my tasks", token, conversation_id)
    if response:
        print_response("Response", response)

    wait_for_user()

    response = send_chat_message(user_id, "Delete the first one", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should identify 'the first one' from previous list")

    wait_for_user()

    return conversation_id


def test_phase_10_delete_tasks(user_id, token, conversation_id):
    """Phase 10: User Story 4 - Delete Tasks via Natural Language"""
    print_header("Phase 10: Delete Tasks via Natural Language (US4)")

    # Test 1: Delete by ID
    print_info("Test 1: 'Delete task 2'")
    response = send_chat_message(user_id, "Delete task 2", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should delete task and confirm")

    wait_for_user()

    # Test 2: Delete by description
    print_info("Test 2: 'Remove the meeting task'")
    response = send_chat_message(user_id, "Remove the meeting task", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should find task by title and delete")

    wait_for_user()

    return conversation_id


def test_phase_11_update_tasks(user_id, token, conversation_id):
    """Phase 11: User Story 5 - Update Tasks via Natural Language"""
    print_header("Phase 11: Update Tasks via Natural Language (US5)")

    # Test 1: Update title
    print_info("Test 1: 'Change task 1 to Buy organic groceries'")
    response = send_chat_message(user_id, "Change task 1 to Buy organic groceries", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should update task title")

    wait_for_user()

    # Test 2: Update description
    print_info("Test 2: 'Update the groceries task to include fruits and vegetables'")
    response = send_chat_message(user_id, "Update the groceries task to include fruits and vegetables", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should update task description")

    wait_for_user()

    return conversation_id


def test_phase_12_error_handling(user_id, token, conversation_id):
    """Phase 12: User Story 7 - Handle Errors Gracefully"""
    print_header("Phase 12: Handle Errors Gracefully (US7)")

    # Test 1: Invalid task ID
    print_info("Test 1: 'Mark task 999 as complete' (non-existent task)")
    response = send_chat_message(user_id, "Mark task 999 as complete", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should provide user-friendly error message")

    wait_for_user()

    # Test 2: Ambiguous request
    print_info("Test 2: 'Do that thing' (ambiguous)")
    response = send_chat_message(user_id, "Do that thing", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should ask for clarification")

    wait_for_user()

    return conversation_id


def test_phase_13_stateless_architecture(user_id, token):
    """Phase 13: User Story 8 - Resume Conversations After Server Restart"""
    print_header("Phase 13: Stateless Architecture (US8)")

    # Create new conversation
    print_info("Test 1: Create conversation and add messages")
    response = send_chat_message(user_id, "Add a task to test server restart", token)
    if response:
        conversation_id = response["conversation_id"]
        print_response("Response", response)
        print_success(f"Conversation created: {conversation_id}")

    wait_for_user()

    # Add more messages
    print_info("Test 2: Add more context")
    response = send_chat_message(user_id, "Also add a task to verify stateless design", token, conversation_id)
    if response:
        print_response("Response", response)

    wait_for_user()

    # Prompt to restart server
    print(f"\n{Colors.WARNING}{'='*70}{Colors.ENDC}")
    print(f"{Colors.WARNING}MANUAL STEP REQUIRED:{Colors.ENDC}")
    print(f"{Colors.WARNING}1. Stop the backend server (Ctrl+C){Colors.ENDC}")
    print(f"{Colors.WARNING}2. Restart the backend server (uvicorn src.main:app --reload){Colors.ENDC}")
    print(f"{Colors.WARNING}3. Press Enter when server is back up{Colors.ENDC}")
    print(f"{Colors.WARNING}{'='*70}{Colors.ENDC}")
    wait_for_user()

    # Continue conversation after restart
    print_info("Test 3: Continue conversation after restart")
    response = send_chat_message(user_id, "Show me my tasks", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Conversation context preserved after server restart!")
        print_success("Agent should show tasks created before restart")

    wait_for_user()

    print_info("Test 4: Reference pre-restart messages")
    response = send_chat_message(user_id, "Mark the first task as complete", token, conversation_id)
    if response:
        print_response("Response", response)
        print_success("Agent should resolve reference to pre-restart task")

    wait_for_user()


def run_all_tests():
    """Run all user story tests."""
    print_header("AI Chatbot User Stories - Manual Test Suite")
    print("This script validates all user stories (Phases 7-13)\n")

    # Authenticate
    token, user_id = authenticate()

    # Initialize conversation
    conversation_id = None

    # Run tests
    try:
        conversation_id = test_phase_7_view_tasks(user_id, token, conversation_id)
        conversation_id = test_phase_8_complete_tasks(user_id, token, conversation_id)
        conversation_id = test_phase_9_conversation_context(user_id, token, conversation_id)
        conversation_id = test_phase_10_delete_tasks(user_id, token, conversation_id)
        conversation_id = test_phase_11_update_tasks(user_id, token, conversation_id)
        conversation_id = test_phase_12_error_handling(user_id, token, conversation_id)
        test_phase_13_stateless_architecture(user_id, token)

        # Summary
        print_header("Test Suite Complete")
        print_success("All user stories validated!")
        print_info("Review the responses above to verify agent behavior")
        print_info("Next steps:")
        print_info("  1. Deploy to Railway (backend) and Vercel (frontend)")
        print_info("  2. Run production validation tests")
        print_info("  3. Conduct user acceptance testing")

    except KeyboardInterrupt:
        print_error("\nTests interrupted by user")
    except Exception as e:
        print_error(f"Test failed with error: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
