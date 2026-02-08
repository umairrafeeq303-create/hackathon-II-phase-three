'use client';

import { useRef, useState } from 'react';
import { ProtectedRoute } from "@/components/layout/ProtectedRoute";
import { Header } from "@/components/layout/Header";
import { TaskList, type TaskListRef } from "@/components/tasks/TaskList";
import { TaskForm } from "@/components/tasks/TaskForm";
import { TaskFilters } from "@/components/tasks/TaskFilters";
import { FloatingAIAssistant } from "@/components/chat/FloatingAIAssistant";
import type { TaskFilters as TaskFiltersType } from '@/types/task';

export default function DashboardPage() {
  const taskListRef = useRef<TaskListRef>(null);
  const [filters, setFilters] = useState<TaskFiltersType>({
    sort: 'created_at',
    order: 'desc',
  });

  const handleTaskCreated = () => {
    // Refresh the task list when a new task is created
    taskListRef.current?.refresh();
  };

  const handleFilterChange = (newFilters: TaskFiltersType) => {
    setFilters(newFilters);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
        {/* Animated Background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-violet-600/10 rounded-full blur-3xl animate-pulse [animation-delay:1.5s]"></div>
        </div>

        <Header />

        <main className="relative z-10 container-premium py-8 sm:py-12">
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="animate-fade-in-premium">
              <div className="flex items-center gap-5 mb-6">
                <div className="icon-gradient-primary w-16 h-16 animate-float">
                  <svg className="w-9 h-9 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-4xl sm:text-5xl font-bold gradient-text-primary text-shadow-premium">
                    My Tasks
                  </h1>
                  <p className="mt-2 text-lg text-slate-400 font-medium">
                    Organize, prioritize, and accomplish more
                  </p>
                </div>
              </div>

              {/* Stats Overview - Premium Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
                <div className="glass-card p-6 border-purple-500/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm font-semibold mb-1">Active Tasks</p>
                      <p className="text-3xl font-bold gradient-text-primary">-</p>
                    </div>
                    <div className="icon-gradient-primary w-12 h-12">
                      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="glass-card p-6 border-emerald-500/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm font-semibold mb-1">Completed</p>
                      <p className="text-3xl font-bold text-emerald-400">-</p>
                    </div>
                    <div className="icon-gradient-primary w-12 h-12 from-emerald-500 via-teal-600 to-emerald-700">
                      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div className="glass-card p-6 border-amber-500/20">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-slate-400 text-sm font-semibold mb-1">Productivity</p>
                      <p className="text-3xl font-bold gradient-text-gold">-</p>
                    </div>
                    <div className="icon-gradient-gold w-12 h-12">
                      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Create Task Form */}
            <div className="animate-slide-down-premium">
              <TaskForm onTaskCreated={handleTaskCreated} />
            </div>

            {/* Task Filters */}
            <div className="animate-slide-down-premium [animation-delay:0.1s]">
              <TaskFilters filters={filters} onFilterChange={handleFilterChange} />
            </div>

            {/* Task List */}
            <div className="animate-slide-up-premium [animation-delay:0.2s]">
              <div className="mb-6">
                <div className="flex items-center gap-3">
                  <div className="h-1 w-1 rounded-full bg-purple-500 animate-pulse"></div>
                  <h2 className="text-2xl font-bold text-slate-200">All Tasks</h2>
                  <div className="flex-1 h-px bg-gradient-to-r from-slate-700 to-transparent"></div>
                </div>
              </div>
              <TaskList ref={taskListRef} filters={filters} />
            </div>
          </div>
        </main>

        {/* Floating AI Assistant */}
        <FloatingAIAssistant />
      </div>
    </ProtectedRoute>
  );
}
