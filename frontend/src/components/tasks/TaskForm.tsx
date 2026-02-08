'use client';

/**
 * Premium TaskForm component - create new tasks with luxury styling
 */
import React, { useState } from 'react';
import { api } from '@/lib/api';
import type { ApiError } from '@/types/api';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';

interface TaskFormProps {
  onTaskCreated?: () => void;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
  });
  const [errors, setErrors] = useState<{
    title?: string;
    description?: string;
    general?: string;
  }>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: typeof errors = {};

    // Title validation
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title must be less than 200 characters';
    }

    // Description validation (optional but has length limit)
    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be less than 1000 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setShowSuccess(false);

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      await api.createTask({
        title: formData.title.trim(),
        description: formData.description.trim() || undefined,
      });

      // Show success message
      setShowSuccess(true);

      // Clear form
      setFormData({ title: '', description: '' });

      // Notify parent to refresh task list
      if (onTaskCreated) {
        onTaskCreated();
      }

      // Hide success message after 3 seconds
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      const apiError = error as ApiError;
      setErrors({
        general: apiError.detail || 'Failed to create task. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for this field when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  return (
    <Card className="border-slate-600/50">
      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Form Header */}
        <div className="flex items-center gap-4 pb-4 border-b border-slate-700/50">
          <div className="icon-gradient-primary w-12 h-12">
            <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <div>
            <h3 className="text-2xl font-bold gradient-text-primary">
              Create New Task
            </h3>
            <p className="text-sm text-slate-400 mt-0.5">Add a new task to your workflow</p>
          </div>
        </div>

        {/* Error Message */}
        {errors.general && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 backdrop-blur-sm animate-slide-down-premium">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-red-300 font-medium">{errors.general}</p>
            </div>
          </div>
        )}

        {/* Success Message */}
        {showSuccess && (
          <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4 backdrop-blur-sm animate-slide-down-premium">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-emerald-500 rounded-full flex items-center justify-center flex-shrink-0">
                <svg className="h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="text-sm text-emerald-300 font-semibold">Task created successfully!</span>
            </div>
          </div>
        )}

        {/* Title Field */}
        <div className="space-y-2">
          <label htmlFor="title" className="block text-sm font-semibold text-slate-300">
            Title *
          </label>
          <input
            id="title"
            name="title"
            type="text"
            value={formData.title}
            onChange={handleChange}
            className={`input-premium ${errors.title ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' : ''}`}
            placeholder="Enter task title"
            disabled={isLoading}
          />
          {errors.title && (
            <p className="mt-2 text-sm text-red-400 flex items-center gap-1.5 animate-slide-down-premium">
              <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {errors.title}
            </p>
          )}
        </div>

        {/* Description Field */}
        <div className="space-y-2">
          <label htmlFor="description" className="block text-sm font-semibold text-slate-300">
            Description (optional)
          </label>
          <textarea
            id="description"
            name="description"
            rows={3}
            value={formData.description}
            onChange={handleChange}
            className={`input-premium resize-none ${errors.description ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' : ''}`}
            placeholder="Add more details about this task (optional)"
            disabled={isLoading}
          />
          {errors.description && (
            <p className="mt-2 text-sm text-red-400 flex items-center gap-1.5 animate-slide-down-premium">
              <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {errors.description}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <Button
          type="submit"
          variant="primary"
          isLoading={isLoading}
          className="w-full"
        >
          Create Task
        </Button>
      </form>
    </Card>
  );
}
