# Frontend - Authentication & User Management System

Next.js 16+ frontend for the Todo Application with Better Auth integration.

## Prerequisites

- Node.js 20+
- npm 10+
- Running backend API (see `../backend/README.md`)

## Project Structure

```
frontend/
├── src/
│   ├── app/                # Next.js App Router pages
│   │   ├── auth/
│   │   │   ├── signup/    # Signup page
│   │   │   └── signin/    # Signin page
│   │   └── layout.tsx     # Root layout
│   ├── lib/               # Core utilities
│   │   ├── api.ts         # API client
│   │   └── auth.ts        # Better Auth configuration
│   ├── components/        # React components
│   │   └── auth/          # Authentication components
│   ├── hooks/             # Custom React hooks
│   ├── context/           # React context providers
│   └── types/             # TypeScript type definitions
├── package.json
├── tsconfig.json          # TypeScript configuration
├── tailwind.config.ts     # Tailwind CSS configuration
├── next.config.js         # Next.js configuration
├── .env.local.example     # Environment variable template
└── README.md              # This file
```

## Setup Instructions

### Step 1: Install Dependencies

```bash
npm install
```

**Key Dependencies**:
- Next.js 16+ - React framework with App Router
- React 19 - UI library
- TypeScript 5.3+ - Type safety
- Tailwind CSS 3.4+ - Utility-first CSS
- Better Auth 1.0+ - Authentication library

### Step 2: Configure Environment Variables

Create `.env.local` file by copying the example:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` with your values:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Secret (MUST match backend BETTER_AUTH_SECRET exactly)
BETTER_AUTH_SECRET=your-super-secret-key-minimum-32-characters-long
```

**CRITICAL**: Use the EXACT same `BETTER_AUTH_SECRET` as the backend.

Generate a secure secret:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64url'))"
```

### Step 3: Run Development Server

```bash
npm run dev
```

Application will be available at:
- Frontend: http://localhost:3000

### Step 4: Build for Production

```bash
npm run build
npm start
```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build production bundle
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Pages

### Authentication Pages

- `/auth/signup` - User registration
- `/auth/signin` - User login
- `/` - Home page / Dashboard (protected)

## Features

### User Registration (Signup)
- Name, email, and password inputs
- Client-side validation
- Password strength requirements
- Error handling with user-friendly messages
- Automatic JWT token storage
- Redirect to dashboard after successful signup

### User Login (Signin)
- Email and password inputs
- Client-side validation
- Error handling for invalid credentials
- Automatic JWT token storage
- Redirect to dashboard after successful login
- Link to signup page

### Protected Routes
- Automatic JWT token validation
- Redirect to signin for unauthenticated users
- Authorization header in API requests
- Token expiry handling

### User Session Management
- Logout functionality
- Token removal from localStorage
- Redirect to signin after logout

## API Integration

The frontend communicates with the backend API through `src/lib/api.ts`:

### API Client Functions

- `signup(name, email, password)` - Create new user account
- `signin(email, password)` - Sign in existing user
- `getCurrentUser()` - Get current user information
- `logout()` - Clear authentication token

### Error Handling

The API client includes custom error handling:
- `AuthError` class for authentication errors
- HTTP status code exposure
- User-friendly error messages

## Testing

### Manual Testing Checklist

#### Signup Flow
- [ ] Create account with valid inputs
- [ ] Try duplicate email (should show error)
- [ ] Try weak password (should show error)
- [ ] Try invalid email format (should show error)
- [ ] Verify JWT token stored in localStorage
- [ ] Verify redirect to dashboard

#### Signin Flow
- [ ] Sign in with correct credentials
- [ ] Try wrong password (should show error)
- [ ] Try non-existent email (should show error)
- [ ] Verify JWT token stored in localStorage
- [ ] Verify redirect to dashboard

#### Protected Routes
- [ ] Access protected page with valid token
- [ ] Access protected page without token (should redirect to signin)
- [ ] Access protected page with expired token (should redirect to signin)

#### Logout Flow
- [ ] Click logout button
- [ ] Verify token removed from localStorage
- [ ] Verify redirect to signin page
- [ ] Try to access protected route (should redirect to signin)

## Common Issues

### Module Not Found

**Error**: `Module not found: Can't resolve 'better-auth'`

**Solution**:
- Run `npm install` in frontend directory
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Verify you're using Node.js 20+

### API Connection Failed

**Error**: Network request failed or CORS error

**Solution**:
- Verify backend is running at `http://localhost:8000`
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend CORS configuration includes frontend URL
- Check browser console for detailed error messages

### JWT Token Invalid

**Error**: 401 Unauthorized

**Solution**:
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check that secret is at least 32 characters
- Clear localStorage and sign in again
- Check token hasn't expired (7-day expiry)

### Build Errors

**Error**: TypeScript compilation errors

**Solution**:
- Run `npm run type-check` to see all type errors
- Ensure all dependencies are installed
- Check `tsconfig.json` configuration

## Debugging

### Browser DevTools

1. Press F12 to open DevTools
2. Check Console tab for JavaScript errors
3. Check Network tab for API requests
4. Check Application tab → Local Storage for `auth_token`

### React DevTools

Install React DevTools browser extension for component inspection and state debugging.

### Hot Reload

Next.js automatically reloads on file changes in development mode.

## Styling

The application uses Tailwind CSS for styling:

- Utility-first CSS classes
- Responsive design with breakpoints
- Custom color palette in `tailwind.config.ts`
- Dark mode support (can be enabled)

## Type Safety

TypeScript is configured with strict mode:

- All code must be properly typed
- No implicit `any` types
- Strict null checks enabled
- Type definitions in `src/types/`

## Security

- JWT tokens stored in localStorage
- Automatic token inclusion in API requests
- Protected routes with authentication checks
- CSRF protection via Better Auth
- XSS protection via React's built-in escaping
- Password validation on client and server

## Deployment

### Vercel (Recommended)

1. Push code to GitHub repository
2. Connect repository to Vercel
3. Configure environment variables:
   - `NEXT_PUBLIC_API_URL` - Your backend URL (Railway)
   - `BETTER_AUTH_SECRET` - Same as backend
4. Deploy

Vercel will automatically:
- Detect Next.js configuration
- Install dependencies
- Build production bundle
- Deploy to global CDN

### Manual Deployment

```bash
# Build production bundle
npm run build

# Start production server
npm start
```

## Phase III: AI Chatbot Interface

The AI Chatbot feature provides a conversational interface for managing tasks using natural language. Users can create, view, complete, delete, and update tasks through chat messages.

### Chat Interface Features

- **Natural Language Input**: Type messages like "Add a task to buy milk"
- **Conversation History**: See full chat history with the AI assistant
- **Real-Time Responses**: Get instant feedback from the AI
- **Context Awareness**: AI remembers previous messages
- **Tool Call Transparency**: Optional display of tool invocations
- **Error Handling**: User-friendly error messages

### Setup

The chat interface requires:
1. Backend server running with OpenAI API configured
2. User authentication (automatic via existing auth system)
3. No additional frontend configuration needed

### Using the Chat Interface

#### Accessing the Chat

1. Sign in to your account
2. Navigate to `/chat` route
3. Start typing messages to the AI assistant

#### Example Interactions

**Create Tasks**:
```
You: Add a task to buy milk
AI: Got it! I've added 'Buy milk' to your task list.

You: I need to remember to call mom tonight
AI: Got it! I've added 'Call mom tonight' to your task list.
```

**View Tasks**:
```
You: Show me my tasks
AI: You have 3 pending tasks:
    1. Buy milk
    2. Call mom tonight
    3. Project deadline

You: What's pending?
AI: You have 2 pending tasks:
    1. Buy milk
    2. Call mom tonight
```

**Complete Tasks**:
```
You: Mark task 1 as complete
AI: Great job! I've marked 'Buy milk' as complete.

You: I finished the groceries
AI: Awesome! I've marked 'Buy milk' as complete.
```

**Delete Tasks**:
```
You: Delete task 2
AI: I've deleted task 2 from your list.

You: Remove the meeting task
AI: I've deleted 'Team meeting' from your list.
```

**Update Tasks**:
```
You: Change task 1 to 'Buy organic milk'
AI: I've updated task 1 to 'Buy organic milk'.

You: Update the groceries task to include fruits
AI: I've updated 'Buy groceries' to include fruits.
```

**Using Context**:
```
You: Add a task to buy milk
AI: Got it! I've added 'Buy milk' to your task list.

You: Mark that task as complete  ← References previous message
AI: Great job! I've marked 'Buy milk' as complete.

You: Show my tasks
AI: You have 2 tasks: 1. Call mom, 2. Project deadline

You: Delete the first one  ← References task from list
AI: I've deleted 'Call mom' from your list.
```

### Chat Components

The chat interface consists of:

#### 1. Chat Page (`/chat`)

**Location**: `src/app/chat/page.tsx`

**Features**:
- Full-screen chat interface
- Message history display
- Input box with send button
- Loading indicators
- Error messages
- Conversation persistence

#### 2. Message List Component

**Location**: `src/components/chat/MessageList.tsx`

**Features**:
- Displays all messages in conversation
- User messages (aligned right, blue background)
- Assistant messages (aligned left, gray background)
- Auto-scroll to newest message
- Timestamps (optional)
- Tool call details (optional)

#### 3. Chat Input Component

**Location**: `src/components/chat/ChatInput.tsx`

**Features**:
- Multi-line textarea input
- Send button (disabled when empty or loading)
- Enter to send (Shift+Enter for new line)
- Input clearing after send
- Character counter (optional)
- "AI is typing..." indicator

### Custom Hook: useChat

**Location**: `src/hooks/useChat.ts`

**State Management**:
```typescript
const {
  messages,          // Array of conversation messages
  isLoading,        // Loading state during API call
  error,            // Error message if request fails
  conversationId,   // Current conversation ID
  sendMessage       // Function to send new message
} = useChat();
```

**Usage Example**:
```tsx
import { useChat } from '@/hooks/useChat';

export default function ChatPage() {
  const { messages, isLoading, sendMessage } = useChat();

  const handleSend = (text: string) => {
    sendMessage(text);
  };

  return (
    <div>
      <MessageList messages={messages} />
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
}
```

### API Integration

**Location**: `src/lib/api-chat.ts`

**Function**:
```typescript
sendChatMessage(
  userId: string,
  message: string,
  conversationId?: string
): Promise<ChatResponse>
```

**Request Format**:
```json
POST /api/{user_id}/chat
Authorization: Bearer <jwt-token>

{
  "message": "Add a task to buy milk",
  "conversation_id": "uuid-here" // Optional for existing conversation
}
```

**Response Format**:
```json
{
  "conversation_id": "uuid-here",
  "response": "Got it! I've added 'Buy milk' to your task list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {"user_id": "...", "title": "Buy milk"},
      "result": {"task_id": 1, "status": "created", "title": "Buy milk"}
    }
  ]
}
```

### Conversation Persistence

**Local Storage**:
- Conversation ID stored in `localStorage.getItem('current_conversation_id')`
- Automatically loaded on page refresh
- Can start new conversation by clearing ID

**URL Parameter** (Alternative):
```
/chat?conversation=uuid-here
```

### TypeScript Types

**Location**: `src/types/chat.ts`

```typescript
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolCalls?: ToolCall[];
}

interface ToolCall {
  tool: string;
  parameters: Record<string, any>;
  result: Record<string, any>;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
}
```

### Error Handling

**Connection Errors**:
```
AI: I'm having trouble connecting right now. Please check your internet connection.
[Retry button available]
```

**Invalid Requests**:
```
AI: Please provide a task title (max 200 characters).
```

**Server Errors**:
```
AI: Something went wrong. Please try again in a moment.
[Retry button available]
```

### UI/UX Features

**Loading States**:
- "AI is typing..." indicator while waiting for response
- Skeleton loading for message history
- Disabled input during request

**Empty States**:
- Welcome message when starting new conversation
- Suggested prompts for first-time users
- Quick action buttons (optional)

**Accessibility**:
- Keyboard navigation (Tab, Enter)
- ARIA labels for screen readers
- Focus management
- High contrast mode support

### Testing the Chat Interface

#### Manual Testing Checklist

**Basic Functionality**:
- [ ] Open `/chat` page (requires authentication)
- [ ] Send message "Add a task to test"
- [ ] Verify AI response appears
- [ ] Verify task created in backend
- [ ] Refresh page - conversation persists

**Create Tasks**:
- [ ] "Add a task to buy milk" → Task created
- [ ] "I need to call mom" → Task created
- [ ] "Create tasks: milk, eggs, bread" → 3 tasks created

**View Tasks**:
- [ ] "Show me my tasks" → Lists all tasks
- [ ] "What's pending?" → Lists pending only
- [ ] "What have I completed?" → Lists completed only

**Complete Tasks**:
- [ ] "Mark task 1 as complete" → Task completed
- [ ] "I finished buying milk" → Task found and completed

**Delete Tasks**:
- [ ] "Delete task 2" → Task deleted
- [ ] "Remove the meeting task" → Task found and deleted

**Update Tasks**:
- [ ] "Change task 1 to new title" → Task updated
- [ ] "Add details to task 2" → Description updated

**Context Awareness**:
- [ ] Create task, then "mark that as complete" → Works
- [ ] List tasks, then "delete the first one" → Works
- [ ] Multi-turn conversation maintains context

**Error Handling**:
- [ ] "Mark task 999 as complete" → Friendly error
- [ ] Send message while offline → Connection error
- [ ] Ambiguous request → AI asks for clarification

### Customization

#### Styling

Modify Tailwind classes in components:

```tsx
// User message (blue background)
<div className="bg-blue-500 text-white rounded-lg p-3 max-w-md ml-auto">
  {message.content}
</div>

// Assistant message (gray background)
<div className="bg-gray-100 text-gray-900 rounded-lg p-3 max-w-md mr-auto">
  {message.content}
</div>
```

#### Message Formatting

Add markdown support (optional):

```bash
npm install react-markdown
```

```tsx
import ReactMarkdown from 'react-markdown';

<ReactMarkdown>{message.content}</ReactMarkdown>
```

#### Quick Actions

Add quick action buttons:

```tsx
const quickActions = [
  "Show me my tasks",
  "What's pending?",
  "Add a new task"
];

{messages.length === 0 && quickActions.map(action => (
  <button onClick={() => sendMessage(action)}>
    {action}
  </button>
))}
```

### Performance

**Optimistic UI Updates**:
```typescript
const sendMessage = async (text: string) => {
  // Add user message immediately
  setMessages(prev => [...prev, { role: 'user', content: text }]);

  // Send API request
  const response = await sendChatMessage(userId, text);

  // Add assistant response
  setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
};
```

**Message Virtualization** (for long conversations):
```bash
npm install react-window
```

### Troubleshooting

**Chat Not Loading**:
1. Check backend is running: `curl http://localhost:8000/docs`
2. Verify OpenAI API key configured in backend `.env`
3. Check browser console for errors
4. Verify user is authenticated

**AI Not Responding**:
1. Check network tab - API request successful?
2. Check backend logs for OpenAI API errors
3. Verify OPENAI_API_KEY is valid
4. Check rate limits on OpenAI account

**Context Not Preserved**:
1. Check conversation_id in localStorage
2. Verify conversation_id sent in API request
3. Check backend conversation loading logic
4. Clear localStorage and start new conversation

**Slow Responses**:
1. OpenAI API typically responds in 1-2 seconds
2. Check network speed
3. Check backend logs for retry attempts
4. Consider upgrading OpenAI plan for higher rate limits

### Security

**Data Privacy**:
- Conversations stored per user (isolated)
- Cannot access other users' conversations
- JWT token required for all requests

**Input Validation**:
- Maximum message length: 10,000 characters
- XSS protection via React escaping
- SQL injection protection (backend ORM)

**Cross-User Protection**:
- Agent validates user_id ownership
- Cannot view/modify other users' tasks
- Social engineering attempts blocked

## Reference Documentation

- Specification: `../specs/001-auth/spec.md`
- Data Model: `../specs/001-auth/data-model.md`
- API Contracts: `../specs/001-auth/contracts/`
- Implementation Plan: `../specs/001-auth/plan.md`
- Quickstart Guide: `../specs/001-auth/quickstart.md`
- AI Chatbot Spec: `../specs/004-ai-chatbot/spec.md`
- AI Chatbot Plan: `../specs/004-ai-chatbot/plan.md`

## External Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Better Auth Documentation](https://better-auth.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
