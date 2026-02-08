'use client';

/**
 * Chat page - AI assistant interface for natural language task management
 */
import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import { Header } from '@/components/layout/Header';
import { MessageList } from '@/components/chat/MessageList';
import { ChatInput } from '@/components/chat/ChatInput';
import { useChat } from '@/hooks/useChat';

export default function ChatPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { messages, isLoading, error, conversationId, sendMessage, clearError, resetConversation } = useChat();

  // Load conversation ID from URL on mount
  useEffect(() => {
    const urlConversationId = searchParams.get('conversation');
    if (urlConversationId && !conversationId) {
      // Note: In a full implementation, you would load conversation history here
      // For now, we just set the conversation ID for continuing the conversation
    }
  }, [searchParams, conversationId]);

  // Update URL when conversation ID changes
  useEffect(() => {
    if (conversationId) {
      const url = new URL(window.location.href);
      url.searchParams.set('conversation', conversationId);
      router.replace(url.pathname + url.search, { scroll: false });
    }
  }, [conversationId, router]);

  const handleSendMessage = async (message: string) => {
    await sendMessage(message);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Header />

        <main className="flex-1 flex flex-col max-w-7xl w-full mx-auto">
          {/* Page Header */}
          <div className="px-6 py-6 bg-white border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AI Assistant</h1>
                <p className="mt-1 text-sm text-gray-600">
                  Manage your tasks with natural language
                </p>
              </div>
              {conversationId && (
                <button
                  onClick={resetConversation}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                >
                  New Conversation
                </button>
              )}
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mx-6 mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex items-start">
                  <svg
                    className="h-5 w-5 text-red-400 mt-0.5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                    <p className="mt-1 text-sm text-red-700">{error}</p>
                  </div>
                </div>
                <button
                  onClick={clearError}
                  className="ml-3 text-red-400 hover:text-red-600"
                >
                  <svg
                    className="h-5 w-5"
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
            </div>
          )}

          {/* Chat Messages */}
          <div className="flex-1 flex flex-col bg-white mx-6 my-4 rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <MessageList messages={messages} />
            <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
