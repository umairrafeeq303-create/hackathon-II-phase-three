"use client";

/**
 * MessageList component - Displays chat messages with user/assistant differentiation
 */
import { useEffect, useRef } from 'react';
import type { ChatMessage } from '@/types/chat';

interface MessageListProps {
  messages: ChatMessage[];
  compact?: boolean;
}

export function MessageList({ messages, compact = false }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        <div className="text-center">
          <p className={compact ? "text-base font-medium" : "text-lg font-medium"}>Start a conversation</p>
          <p className={compact ? "text-xs mt-1" : "text-sm mt-2"}>
            Try: &quot;Add a task to buy groceries&quot;
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={compact ? "flex-1 overflow-y-auto p-3 space-y-2" : "flex-1 overflow-y-auto p-4 space-y-4"}>
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`${compact ? 'max-w-[85%] rounded-lg px-3 py-1.5 text-sm' : 'max-w-[80%] rounded-lg px-4 py-2'} ${
              message.role === 'user'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-900'
            }`}
          >
            <p className="whitespace-pre-wrap break-words">{message.content}</p>
            {message.timestamp && (
              <p
                className={`text-xs mt-1 ${
                  message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}
              >
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            )}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
