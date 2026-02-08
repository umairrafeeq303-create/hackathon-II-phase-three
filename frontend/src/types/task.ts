// Task type definitions for todo management

export type TaskStatus = 'pending' | 'completed';

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: TaskStatus;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: TaskStatus;
}

export interface TaskFilters {
  status?: TaskStatus;
  sort?: 'created_at' | 'updated_at' | 'title';
  order?: 'asc' | 'desc';
}
