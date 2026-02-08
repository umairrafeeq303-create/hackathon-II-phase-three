"use client";

/**
 * Custom hook for chat state management and AI assistant interaction
 */
import { useState, useCallback } from 'react';
import { sendChatMessage } from '@/lib/api-chat';
import type { ChatMessage } from '@/types/chat';
import type { ApiError } from '@/types/api';

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  conversationId: string | null;
  sendMessage: (message: string) => Promise<void>;
  clearError: () => void;
  resetConversation: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (message: string) => {
      // Validate message
      const trimmedMessage = message.trim();
      if (!trimmedMessage) {
        setError('Message cannot be empty');
        return;
      }

      if (trimmedMessage.length > 10000) {
        setError('Message is too long (maximum 10,000 characters)');
        return;
      }

      // Clear previous error
      setError(null);
      setIsLoading(true);

      // Optimistic UI update: add user message immediately
      const userMessage: ChatMessage = {
        role: 'user',
        content: trimmedMessage,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      try {
        // Call API
        const response = await sendChatMessage(trimmedMessage, conversationId || undefined);

        // Update conversation ID (for new conversations)
        if (!conversationId) {
          setConversationId(response.conversation_id);
        }

        // Add assistant response to messages
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.response,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        // Handle API errors
        const apiError = err as ApiError;
        const errorMessage = apiError.detail || 'Failed to send message. Please try again.';
        setError(errorMessage);

        // Remove optimistic user message on error
        setMessages((prev) => prev.slice(0, -1));
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId]
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const resetConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
    setIsLoading(false);
  }, []);

  return {
    messages,
    isLoading,
    error,
    conversationId,
    sendMessage,
    clearError,
    resetConversation,
  };
}
