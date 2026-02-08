/**
 * API client for backend communication
 */
import type {
  User,
  AuthResponse,
  SignupCredentials,
  SigninCredentials
} from '@/types/auth';
import type {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskFilters
} from '@/types/task';
import type { ApiError } from '@/types/api';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private getAuthToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  /**
   * Get current user ID from localStorage
   * The user object is stored when user signs in/signs up
   */
  private getCurrentUserId(): string | null {
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
   * Ensure user is authenticated and return user_id
   * Throws error if not authenticated
   */
  private ensureAuthenticated(): string {
    const userId = this.getCurrentUserId();
    if (!userId) {
      const error: ApiError = {
        detail: 'Not authenticated. Please log in.',
        status: 401,
      };
      throw error;
    }
    return userId;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getAuthToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

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
          // Simple string error (404, 403, etc.)
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

    // Handle 204 No Content responses
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  // Auth endpoints
  /**
   * Sign up a new user
   * Automatically stores token and user data in localStorage
   * @param data Signup credentials (name, email, password)
   * @returns Auth response with user and token
   */
  async signup(data: SignupCredentials): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    // Store token and user data
    if (typeof window !== 'undefined' && response.token && response.user) {
      localStorage.setItem('access_token', response.token);
      localStorage.setItem('current_user', JSON.stringify(response.user));
    }

    return response;
  }

  /**
   * Sign in an existing user
   * Automatically stores token and user data in localStorage
   * @param data Signin credentials (email, password)
   * @returns Auth response with user and token
   */
  async signin(data: SigninCredentials): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/signin', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    // Store token and user data
    if (typeof window !== 'undefined' && response.token && response.user) {
      localStorage.setItem('access_token', response.token);
      localStorage.setItem('current_user', JSON.stringify(response.user));
    }

    return response;
  }

  /**
   * Log out the current user
   * Clears token and user data from localStorage
   */
  async logout(): Promise<void> {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('current_user');
    }
  }

  /**
   * Get current user information from the backend
   * Useful for refreshing user data or verifying authentication
   * @returns Current user object
   */
  async getCurrentUser(): Promise<User> {
    return this.request<User>('/api/auth/me');
  }

  // Task endpoints
  /**
   * Get all tasks for the current user
   * @param filters Optional filters for status, sort, and order
   * @returns Array of tasks belonging to the current user
   */
  async getTasks(filters?: TaskFilters): Promise<Task[]> {
    const userId = this.ensureAuthenticated();

    const queryParams = new URLSearchParams();
    if (filters?.status) queryParams.append('status', filters.status);
    if (filters?.sort) queryParams.append('sort', filters.sort);
    if (filters?.order) queryParams.append('order', filters.order);

    const query = queryParams.toString();
    const endpoint = query ? `/api/${userId}/tasks?${query}` : `/api/${userId}/tasks`;

    return this.request<Task[]>(endpoint);
  }

  /**
   * Get a single task by ID
   * @param id Task ID
   * @returns Task object if found and belongs to current user
   */
  async getTask(id: string): Promise<Task> {
    const userId = this.ensureAuthenticated();
    return this.request<Task>(`/api/${userId}/tasks/${id}`);
  }

  /**
   * Create a new task
   * @param data Task creation data (title required, description optional)
   * @returns Created task object
   */
  async createTask(data: CreateTaskRequest): Promise<Task> {
    const userId = this.ensureAuthenticated();
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Update an existing task
   * @param id Task ID
   * @param data Task update data (title and/or description)
   * @returns Updated task object
   */
  async updateTask(id: string, data: UpdateTaskRequest): Promise<Task> {
    const userId = this.ensureAuthenticated();
    return this.request<Task>(`/api/${userId}/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Toggle task completion status
   * Uses dedicated PATCH endpoint that automatically toggles completed status
   * @param id Task ID
   * @returns Updated task with toggled completion status
   */
  async toggleTask(id: string): Promise<Task> {
    const userId = this.ensureAuthenticated();
    return this.request<Task>(`/api/${userId}/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }

  /**
   * Delete a task permanently
   * @param id Task ID
   */
  async deleteTask(id: string): Promise<void> {
    const userId = this.ensureAuthenticated();
    return this.request<void>(`/api/${userId}/tasks/${id}`, {
      method: 'DELETE',
    });
  }
}

export const api = new ApiClient(API_URL);
