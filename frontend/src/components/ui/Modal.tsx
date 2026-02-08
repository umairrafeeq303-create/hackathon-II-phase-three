/**
 * Premium Modal component with luxury dark theme and glass morphism
 */
import React, { useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children, footer }: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto animate-fade-in-premium">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Premium Backdrop */}
        <div
          className="fixed inset-0 bg-black/70 backdrop-blur-md transition-opacity animate-fade-in-premium"
          onClick={onClose}
        />

        {/* Modal */}
        <div className="relative glass-card max-w-md w-full animate-scale-in-premium border-slate-600/50">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-slate-700/50">
            <h3 className="text-2xl font-bold gradient-text-primary">
              {title}
            </h3>
            <button
              type="button"
              onClick={onClose}
              aria-label="Close modal"
              className="text-slate-400 hover:text-purple-400 hover:scale-110 transition-all duration-300 rounded-lg p-2 hover:bg-slate-700/50 group"
            >
              <svg
                className="h-6 w-6 group-hover:rotate-90 transition-transform duration-300"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </div>

          {/* Body */}
          <div className="p-6 text-slate-200">{children}</div>

          {/* Footer */}
          {footer && (
            <div className="flex items-center justify-end gap-3 p-6 border-t border-slate-700/50">
              {footer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
