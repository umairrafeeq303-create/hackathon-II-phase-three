/**
 * TaskItem component - displays a single task with premium dark theme
 */
import { useState } from 'react';
import type { Task } from '@/types/task';
import type { ApiError } from '@/types/api';
import { api } from '@/lib/api';
import { TaskEditModal } from './TaskEditModal';
import { TaskDeleteModal } from './TaskDeleteModal';

interface TaskItemProps {
  task: Task;
  onTaskUpdated?: () => void;
}

export function TaskItem({ task, onTaskUpdated }: TaskItemProps) {
  const [isCompleted, setIsCompleted] = useState(task.status === 'completed');
  const [isToggling, setIsToggling] = useState(false);
  const [error, setError] = useState<string>('');
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    setError('');

    // Optimistic update
    setIsCompleted(!isCompleted);

    try {
      // Backend automatically toggles the completion status
      await api.toggleTask(task.id);

      // Notify parent to refresh list
      if (onTaskUpdated) {
        onTaskUpdated();
      }
    } catch (err) {
      // Revert optimistic update on error
      setIsCompleted(isCompleted);
      const apiError = err as ApiError;
      setError(apiError.detail || 'Failed to update task');
    } finally {
      setIsToggling(false);
    }
  };

  return (
    <div className="glass-card-hover p-6 animate-scale-in group">
      {error && (
        <div className="mb-4 bg-red-500/10 border border-red-500/30 text-red-300 px-4 py-3 rounded-xl backdrop-blur-sm animate-slide-down-premium">
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span className="text-sm font-medium">{error}</span>
          </div>
        </div>
      )}
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0 mt-1">
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              id={`task-checkbox-${task.id}`}
              type="checkbox"
              checked={isCompleted}
              onChange={handleToggle}
              disabled={isToggling}
              aria-label={`Mark task "${task.title}" as ${isCompleted ? 'incomplete' : 'complete'}`}
              className="sr-only peer"
            />
            <div className={`
              w-6 h-6 rounded-lg border-2 flex items-center justify-center
              transition-all duration-300 ease-in-out
              ${isCompleted
                ? 'bg-gradient-to-br from-emerald-500 to-teal-600 border-emerald-500 scale-110 shadow-lg shadow-emerald-500/30'
                : 'bg-slate-800/50 border-slate-600 hover:border-purple-500 peer-focus:ring-2 peer-focus:ring-purple-500/20'
              }
              ${isToggling ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-lg hover:shadow-purple-500/20'}
            `}>
              {isCompleted && (
                <svg className="w-4 h-4 text-white animate-scale-in" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              )}
            </div>
          </label>
        </div>

        <div className="flex-1 min-w-0">
          <h3
            className={`text-base font-semibold transition-all duration-300 ${
              isCompleted
                ? 'text-slate-500 line-through'
                : 'text-slate-200 group-hover:text-purple-300'
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`mt-2 text-sm leading-relaxed transition-all duration-300 ${
                isCompleted ? 'text-slate-600' : 'text-slate-400'
              }`}
            >
              {task.description}
            </p>
          )}
          <div className="mt-3 flex items-center gap-3 text-xs text-slate-500">
            <span className="flex items-center gap-1">
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {new Date(task.created_at).toLocaleDateString()}
            </span>
            {task.updated_at !== task.created_at && (
              <span className="flex items-center gap-1">
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {new Date(task.updated_at).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex-shrink-0 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          {/* Edit Button */}
          <button
            type="button"
            onClick={() => setIsEditModalOpen(true)}
            className="text-slate-500 hover:text-purple-400 hover:scale-110 transition-all duration-300 p-2 rounded-lg hover:bg-purple-500/10 shadow-sm hover:shadow-purple-500/20"
            title="Edit task"
            aria-label={`Edit task: ${task.title}`}
          >
            <svg
              className="h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>

          {/* Delete Button */}
          <button
            type="button"
            onClick={() => setIsDeleteModalOpen(true)}
            className="text-slate-500 hover:text-red-400 hover:scale-110 transition-all duration-300 p-2 rounded-lg hover:bg-red-500/10 shadow-sm hover:shadow-red-500/20"
            title="Delete task"
            aria-label={`Delete task: ${task.title}`}
          >
            <svg
              className="h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Edit Modal */}
      <TaskEditModal
        task={task}
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        onTaskUpdated={() => {
          if (onTaskUpdated) {
            onTaskUpdated();
          }
        }}
      />

      {/* Delete Modal */}
      <TaskDeleteModal
        task={task}
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onTaskDeleted={() => {
          if (onTaskUpdated) {
            onTaskUpdated();
          }
        }}
      />
    </div>
  );
}
