"use client";

import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

import { createThread } from "@/services/chatThread.service";
import { sendMessage as sendChatMessage } from "@/services/chat.service";

export type Message = {
  role: "user" | "assistant";
  content: string;
};

type ChatContextType = {
  messages: Message[];
  threadId: string | null;
  isLoading: boolean;
  status: string;
  hasMessages: boolean;
  sendMessage: (message: string) => Promise<void>;
  newChat: () => void;
};

const ChatContext = createContext<ChatContextType | undefined>(
  undefined
);

export function ChatProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [threadId, setThreadId] = useState<string | null>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState("");

  const hasMessages = messages.length > 0;

  const sendMessage = async (message: string) => {
    const userMessage = message.trim();

    if (!userMessage || isLoading) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setIsLoading(true);
    setStatus("Understanding your question...");

    let currentThreadId = threadId;

    try {
      /*
       * First message of this chat:
       * create the thread through the backend.
       */
      if (!currentThreadId) {
        const thread = await createThread();

        currentThreadId = thread.threadId;

        setThreadId(currentThreadId);
      }

      /*
       * Fake processing status while the actual
       * AI request is running.
       */
      let statusStep = 0;

      const statuses = [
        "Understanding your question...",
        "Looking through relevant legal provisions...",
        "Preparing your answer...",
      ];

      const statusTimer = window.setInterval(() => {
        statusStep = (statusStep + 1) % statuses.length;
        setStatus(statuses[statusStep]);
      }, 1800);

      try {
        const response = await sendChatMessage({
          threadId: currentThreadId,
          query: userMessage,
        });

        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content: response.answer,
          },
        ]);
      } finally {
        window.clearInterval(statusTimer);
      }

      setStatus("");
    } catch (error) {
      console.error("Chat request failed:", error);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't process that request right now. Please try again.",
        },
      ]);

      setStatus("");
    } finally {
      setIsLoading(false);
    }
  };

  const newChat = () => {
    /*
     * Don't create a backend thread here.
     *
     * The thread is created lazily when the first
     * message of the new conversation is sent.
     */
    if (isLoading) {
      return;
    }

    setMessages([]);
    setThreadId(null);
    setStatus("");
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        threadId,
        isLoading,
        status,
        hasMessages,
        sendMessage,
        newChat,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);

  if (!context) {
    throw new Error(
      "useChat must be used inside ChatProvider"
    );
  }

  return context;
}