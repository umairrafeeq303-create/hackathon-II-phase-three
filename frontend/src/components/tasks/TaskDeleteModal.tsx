'use client';

/**
 * TaskDeleteModal component - confirmation dialog for deleting tasks
 */
import React, { useState } from 'react';
import { Modal } from '@/components/ui/Modal';
import { Button } from '@/components/ui/Button';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { api } from '@/lib/api';
import type { Task } from '@/types/task';
import type { ApiError } from '@/types/api';

interface TaskDeleteModalProps {
  task: Task | null;
  isOpen: boolean;
  onClose: () => void;
  onTaskDeleted: () => void;
}

export function TaskDeleteModal({
  task,
  isOpen,
  onClose,
  onTaskDeleted,
}: TaskDeleteModalProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string>('');

  const handleDelete = async () => {
    if (!task) return;

    setIsDeleting(true);
    setError('');

    try {
      await api.deleteTask(task.id);

      // Notify parent to refresh list
      onTaskDeleted();

      // Close modal
      onClose();
    } catch (err) {
      const apiError = err as ApiError;
      setError(
        apiError.detail || 'Failed to delete task. Please try again.'
      );
    } finally {
      setIsDeleting(false);
    }
  };

  const handleClose = () => {
    setError('');
    onClose();
  };

  if (!task) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Delete Task"
      footer={
        <>
          <Button
            type="button"
            variant="secondary"
            onClick={handleClose}
            disabled={isDeleting}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="primary"
            onClick={handleDelete}
            isLoading={isDeleting}
            className="bg-red-600 hover:bg-red-700 focus:ring-red-500"
          >
            Delete
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        {error && <ErrorMessage message={error} />}

        <div className="text-sm text-gray-700">
          <p className="mb-2">
            Are you sure you want to delete this task? This action cannot be undone.
          </p>
          <div className="bg-gray-50 p-3 rounded-lg border border-gray-200">
            <p className="font-medium text-gray-900">{task.title}</p>
            {task.description && (
              <p className="mt-1 text-gray-600 text-sm">{task.description}</p>
            )}
          </div>
        </div>
      </div>
    </Modal>
  );
}
