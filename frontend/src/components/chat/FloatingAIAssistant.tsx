'use client';

/**
 * Floating AI Assistant - Professional floating chat widget
 * Inspired by modern apps like Intercom, Drift, etc.
 */
import { useState, useEffect } from 'react';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { useChat } from '@/hooks/useChat';

export function FloatingAIAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const { messages, isLoading, error, sendMessage, clearError } = useChat();

  const handleSendMessage = async (message: string) => {
    await sendMessage(message);
  };

  const toggleChat = () => {
    if (isOpen && !isMinimized) {
      setIsMinimized(true);
    } else if (isMinimized) {
      setIsMinimized(false);
    } else {
      setIsOpen(true);
    }
  };

  const closeChat = () => {
    setIsOpen(false);
    setIsMinimized(false);
  };

  return (
    <>
      {/* Floating Button - Always visible */}
      {(!isOpen || isMinimized) && (
        <button
          type="button"
          onClick={toggleChat}
          className="fixed bottom-6 right-6 z-50 group"
          aria-label="Open AI Assistant"
        >
          {/* Pulse animation ring */}
          <span className="absolute inset-0 rounded-full bg-purple-500 animate-ping opacity-20"></span>

          {/* Main button */}
          <div className="relative flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-600 via-violet-600 to-purple-700 rounded-full shadow-2xl transform transition-all duration-300 hover:scale-110 hover:shadow-purple-500/50 group-hover:from-purple-700 group-hover:to-violet-700">
            {/* AI Sparkle Icon */}
            <svg
              className="w-8 h-8 text-white transform transition-transform duration-300 group-hover:rotate-12"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
              />
            </svg>

            {/* Notification badge */}
            {messages.length > 0 && (
              <span className="absolute -top-1 -right-1 flex h-5 w-5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-5 w-5 bg-red-500 text-white text-xs items-center justify-center font-bold">
                  {messages.length}
                </span>
              </span>
            )}
          </div>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && !isMinimized && (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col w-96 h-[600px] glass-card rounded-2xl shadow-2xl animate-slide-up-premium border border-slate-700/50">
          {/* Header */}
          <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-600 to-violet-600 rounded-t-2xl">
            <div className="flex items-center space-x-3">
              {/* AI Avatar */}
              <div className="w-10 h-10 bg-white/20 backdrop-blur rounded-full flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold text-base">AI Assistant</h3>
                <p className="text-purple-100 text-xs">Always here to help</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2">
              <button
                type="button"
                onClick={() => setIsMinimized(true)}
                className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/20 transition-colors"
                aria-label="Minimize"
              >
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <button
                type="button"
                onClick={closeChat}
                className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/20 transition-colors"
                aria-label="Close"
              >
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mx-4 mt-4 bg-red-500/10 border border-red-500/30 rounded-lg p-3 animate-slide-down-premium">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-2">
                  <svg className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <p className="text-sm text-red-400">{error}</p>
                </div>
                <button type="button" onClick={clearError} aria-label="Dismiss error" className="text-red-400 hover:text-red-300 flex-shrink-0 transition-colors">
                  <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-hidden bg-gradient-to-b from-slate-900 to-slate-800">
            <MessageList messages={messages} compact />
          </div>

          {/* Input */}
          <div className="border-t border-slate-700 bg-slate-800/50 rounded-b-2xl">
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} compact />
          </div>
        </div>
      )}
    </>
  );
}
