'use client';

/**
 * TaskFilters component - filter and sort tasks
 */
import React from 'react';
import type { TaskFilters as TaskFiltersType } from '@/types/task';

interface TaskFiltersProps {
  filters: TaskFiltersType;
  onFilterChange: (filters: TaskFiltersType) => void;
}

export function TaskFilters({ filters, onFilterChange }: TaskFiltersProps) {
  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onFilterChange({
      ...filters,
      status: value === 'all' ? undefined : (value as 'pending' | 'completed'),
    });
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onFilterChange({
      ...filters,
      sort: value as 'created_at' | 'updated_at' | 'title',
    });
  };

  const handleOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onFilterChange({
      ...filters,
      order: value as 'asc' | 'desc',
    });
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-5">
        <div className="icon-gradient-primary w-10 h-10">
          <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
        </div>
        <h3 className="text-lg font-bold gradient-text-primary">Filter & Sort</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Status Filter */}
        <div className="transform transition-all duration-300 hover:scale-[1.02]">
          <label
            htmlFor="status-filter"
            className="block text-sm font-semibold text-slate-300 mb-2 flex items-center gap-2"
          >
            <span className="w-2 h-2 rounded-full bg-purple-500 animate-pulse"></span>
            Status
          </label>
          <select
            id="status-filter"
            value={filters.status || 'all'}
            onChange={handleStatusChange}
            className="w-full px-4 py-3 bg-slate-800/50 border-2 border-slate-700 rounded-xl text-slate-200 shadow-sm focus:outline-none focus:ring-4 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-300 cursor-pointer hover:border-purple-600 hover:bg-slate-800/70 backdrop-blur-sm"
          >
            <option value="all" className="bg-slate-900">All Tasks</option>
            <option value="pending" className="bg-slate-900">Pending</option>
            <option value="completed" className="bg-slate-900">Completed</option>
          </select>
        </div>

        {/* Sort By */}
        <div className="transform transition-all duration-300 hover:scale-[1.02]">
          <label
            htmlFor="sort-filter"
            className="block text-sm font-semibold text-slate-300 mb-2 flex items-center gap-2"
          >
            <span className="w-2 h-2 rounded-full bg-violet-500 animate-pulse [animation-delay:0.2s]"></span>
            Sort By
          </label>
          <select
            id="sort-filter"
            value={filters.sort || 'created_at'}
            onChange={handleSortChange}
            className="w-full px-4 py-3 bg-slate-800/50 border-2 border-slate-700 rounded-xl text-slate-200 shadow-sm focus:outline-none focus:ring-4 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-300 cursor-pointer hover:border-purple-600 hover:bg-slate-800/70 backdrop-blur-sm"
          >
            <option value="created_at" className="bg-slate-900">Created Date</option>
            <option value="updated_at" className="bg-slate-900">Updated Date</option>
            <option value="title" className="bg-slate-900">Title</option>
          </select>
        </div>

        {/* Sort Order */}
        <div className="transform transition-all duration-300 hover:scale-[1.02]">
          <label
            htmlFor="order-filter"
            className="block text-sm font-semibold text-slate-300 mb-2 flex items-center gap-2"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse [animation-delay:0.4s]"></span>
            Order
          </label>
          <select
            id="order-filter"
            value={filters.order || 'desc'}
            onChange={handleOrderChange}
            className="w-full px-4 py-3 bg-slate-800/50 border-2 border-slate-700 rounded-xl text-slate-200 shadow-sm focus:outline-none focus:ring-4 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-300 cursor-pointer hover:border-purple-600 hover:bg-slate-800/70 backdrop-blur-sm"
          >
            <option value="desc" className="bg-slate-900">Newest First</option>
            <option value="asc" className="bg-slate-900">Oldest First</option>
          </select>
        </div>
      </div>
    </div>
  );
}
