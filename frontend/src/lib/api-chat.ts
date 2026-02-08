/**
 * Chat API client for AI assistant communication
 */
import type { ChatRequest, ChatResponse } from '@/types/chat';
import type { ApiError } from '@/types/api';
import type { User } from '@/types/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get current user ID from localStorage
 */
function getCurrentUserId(): string | null {
  if (typeof window === 'undefined') return null;
  const userStr = localStorage.getItem('current_user');
  if (!userStr) return null;

  try {
    const user = JSON.parse(userStr) as User;
    return user.id;
  } catch {
    return null;
  }
}

/**
 * Get authentication token from localStorage
 */
function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

/**
 * Send a chat message to the AI assistant
 *
 * @param message User message content (1-10000 characters)
 * @param conversationId Optional conversation ID to continue existing conversation
 * @returns ChatResponse with assistant response and conversation ID
 * @throws ApiError if request fails (400, 401, 403, 404, 500)
 */
export async function sendChatMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  // Validate authentication
  const userId = getCurrentUserId();
  if (!userId) {
    const error: ApiError = {
      detail: 'Not authenticated. Please log in.',
      status: 401,
    };
    throw error;
  }

  const token = getAuthToken();
  if (!token) {
    const error: ApiError = {
      detail: 'No authentication token found. Please log in.',
      status: 401,
    };
    throw error;
  }

  // Build request body
  const requestBody: ChatRequest = {
    message: message.trim(),
  };

  if (conversationId) {
    requestBody.conversation_id = conversationId;
  }

  // Make API request
  const response = await fetch(`${API_URL}/api/${userId}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(requestBody),
  });

  // Handle errors
  if (!response.ok) {
    let errorMessage = 'An error occurred';
    try {
      const errorData = await response.json();

      // Handle different error formats
      if (Array.isArray(errorData.detail)) {
        // Pydantic validation errors (422 status)
        errorMessage = errorData.detail
          .map((err: any) => err.msg || JSON.stringify(err))
          .join('; ');
      } else if (typeof errorData.detail === 'string') {
        // Simple string error (400, 401, 403, 404, 500)
        errorMessage = errorData.detail;
      } else if (errorData.detail) {
        // Object or other format
        errorMessage = JSON.stringify(errorData.detail);
      }
    } catch {
      // Failed to parse JSON, use statusText
      errorMessage = response.statusText || errorMessage;
    }

    const error: ApiError = {
      detail: errorMessage,
      status: response.status,
    };
    throw error;
  }

  // Parse and return response
  return response.json();
}
