import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "success";
  isLoading?: boolean;
}

/**
 * Premium Button component with luxury styling and smooth animations
 */
export function Button({
  children,
  variant = "primary",
  isLoading = false,
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  const variantStyles = {
    primary: "btn-premium-primary",
    secondary: "btn-premium-secondary",
    danger: "btn-premium-danger",
    success: "btn-premium-success",
  };

  return (
    <button
      className={`${variantStyles[variant]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {/* Shimmer effect overlay */}
      <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out"></span>

      {isLoading ? (
        <span className="flex items-center justify-center gap-2 relative z-10">
          {/* Premium spinner */}
          <svg
            className="animate-spin h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="3"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <span>Loading...</span>
        </span>
      ) : (
        <span className="relative z-10 flex items-center justify-center gap-2">
          {children}
        </span>
      )}
    </button>
  );
}
