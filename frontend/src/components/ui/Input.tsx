import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ label, error, className = "", ...props }: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-semibold text-gray-700 mb-2 transition-colors duration-200">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          className={`
            w-full px-4 py-3 border-2 rounded-lg shadow-sm
            transition-all duration-300 ease-in-out
            focus:outline-none focus:ring-2 focus:ring-offset-1
            transform focus:scale-[1.02]
            ${error
              ? "border-red-400 focus:border-red-500 focus:ring-red-500/20 bg-red-50"
              : "border-gray-300 focus:border-indigo-500 focus:ring-indigo-500/20 bg-white hover:border-gray-400"
            }
            ${props.disabled
              ? "bg-gray-100 cursor-not-allowed opacity-60"
              : ""
            }
            ${className}
          `}
          {...props}
        />
        {/* Focus indicator line */}
        {!error && (
          <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-500 to-purple-600 transform scale-x-0 transition-transform duration-300 origin-left peer-focus:scale-x-100"></div>
        )}
      </div>
      {error && (
        <p className="mt-2 text-sm text-red-600 flex items-center gap-1 animate-slide-down">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}
    </div>
  );
}
