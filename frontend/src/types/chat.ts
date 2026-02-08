/**
 * Chat types for AI assistant interaction
 */

export interface ToolCall {
  tool: string;
  parameters: Record<string, any>;
  result: Record<string, any>;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
}
