'use client';

/**
 * TaskList component - fetches and displays all tasks
 */
import React, { useEffect, useState, useImperativeHandle, forwardRef } from 'react';
import { api } from '@/lib/api';
import type { Task, TaskFilters } from '@/types/task';
import type { ApiError } from '@/types/api';
import { TaskItem } from './TaskItem';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ErrorMessage } from '@/components/ui/ErrorMessage';

export interface TaskListRef {
  refresh: () => void;
}

interface TaskListProps {
  filters?: TaskFilters;
}

export const TaskList = forwardRef<TaskListRef, TaskListProps>(({ filters }, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetchTasks();
  }, [filters]); // Re-fetch when filters change

  const fetchTasks = async () => {
    setIsLoading(true);
    setError('');

    try {
      const data = await api.getTasks(filters);
      setTasks(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(apiError.detail || 'Failed to load tasks. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Expose refresh method to parent
  useImperativeHandle(ref, () => ({
    refresh: fetchTasks,
  }));

  if (isLoading) {
    return (
      <div className="flex justify-center py-16">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin"></div>
          <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-violet-500 rounded-full animate-spin [animation-delay:0.15s]"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-8">
        <div className="glass-card p-8 border-red-500/30">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center">
                <svg className="w-6 h-6 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-red-400 mb-1">Error Loading Tasks</h3>
              <p className="text-sm text-slate-400">{error}</p>
              <button
                type="button"
                onClick={fetchTasks}
                className="mt-4 text-sm text-purple-400 hover:text-purple-300 font-semibold transition-colors duration-300 flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Try again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="glass-card p-12 text-center animate-fade-in-premium">
        <div className="icon-gradient-primary w-20 h-20 mx-auto mb-6">
          <svg
            className="w-11 h-11 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-slate-200 mb-2">No tasks yet</h3>
        <p className="text-sm text-slate-400 max-w-sm mx-auto">
          Get started by creating your first task above. Your productivity journey begins here!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} onTaskUpdated={fetchTasks} />
      ))}
    </div>
  );
});

TaskList.displayName = 'TaskList';
