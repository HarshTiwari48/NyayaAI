"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  createThread,
  getThreads,
  type ChatThread,
} from "@/services/chatThread.service";

import {
  getThreadMessages,
  sendMessage as sendChatMessage,
  sendMessageWithDocument,
} from "@/services/chat.service";

import { useAuthStore } from "@/stores/auth.store";

export type Message = {
  role: "user" | "assistant";
  content: string;
};

type ChatContextType = {
  messages: Message[];
  threadId: string | null;
  threads: ChatThread[];

  isLoading: boolean;
  isLoadingThreads: boolean;
  isLoadingMessages: boolean;

  status: string;
  hasMessages: boolean;

  sendMessage: (
    message: string,
    file?: File
  ) => Promise<void>;

  newChat: () => void;
  selectThread: (threadId: string) => Promise<void>;
  refreshThreads: () => Promise<void>;
};

const ChatContext = createContext<ChatContextType | undefined>(
  undefined
);

export function ChatProvider({
  children,
}: {
  children: ReactNode;
}) {
  const user = useAuthStore((state) => state.user);

  const isAuthLoading = useAuthStore(
    (state) => state.isLoading
  );

  const [messages, setMessages] = useState<Message[]>([]);

  const [threadId, setThreadId] = useState<string | null>(
    null
  );

  const [threads, setThreads] = useState<ChatThread[]>([]);

  const [isLoading, setIsLoading] = useState(false);

  const [isLoadingThreads, setIsLoadingThreads] =
    useState(false);

  const [isLoadingMessages, setIsLoadingMessages] =
    useState(false);

  const [status, setStatus] = useState("");

  const hasMessages = messages.length > 0;

  /*
   * ============================================================
   * LOAD USER'S THREADS
   * ============================================================
   */

  const refreshThreads = async () => {
    if (!user) {
      setThreads([]);
      return;
    }

    try {
      setIsLoadingThreads(true);

      const response = await getThreads(1, 20);

      setThreads(response.threads);
    } catch (error) {
      console.error(
        "Failed to load chat threads:",
        error
      );
    } finally {
      setIsLoadingThreads(false);
    }
  };

  /*
   * ============================================================
   * LOAD THREADS WHEN AUTH IS READY
   * ============================================================
   */

  useEffect(() => {
    if (isAuthLoading) {
      return;
    }

    if (!user) {
      setThreads([]);
      return;
    }

    refreshThreads();
  }, [user, isAuthLoading]);

  /*
   * ============================================================
   * SELECT EXISTING THREAD
   * ============================================================
   */

  const selectThread = async (
    selectedThreadId: string
  ) => {
    if (
      isLoading ||
      isLoadingMessages ||
      selectedThreadId === threadId
    ) {
      return;
    }

    try {
      setIsLoadingMessages(true);
      setStatus("Loading conversation...");

      const response = await getThreadMessages(
        selectedThreadId,
        1,
        50
      );

      const loadedMessages: Message[] =
        response.messages.map((message) => ({
          role: message.role,
          content: message.content,
        }));

      setMessages(loadedMessages);
      setThreadId(selectedThreadId);
      setStatus("");
    } catch (error) {
      console.error(
        "Failed to load conversation:",
        error
      );

      setStatus("");
    } finally {
      setIsLoadingMessages(false);
    }
  };

  /*
   * ============================================================
   * SEND MESSAGE
   * ============================================================
   */

  const sendMessage = async (
    message: string,
    file?: File
  ) => {
    const userMessage = message.trim();

    if (!userMessage || isLoading) {
      return;
    }

    /*
     * Immediately show user's message.
     */

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setIsLoading(true);

    setStatus(
      file
        ? "Reading your document..."
        : "Understanding your question..."
    );

    let currentThreadId = threadId;

    try {
      /*
       * ========================================================
       * FIRST MESSAGE
       * ========================================================
       */

      if (!currentThreadId) {
        const thread = await createThread();

        currentThreadId = thread.threadId;

        setThreadId(currentThreadId);

        if (user && !thread.isGuest) {
          const newThread: ChatThread = {
            _id: "",
            userId: "",
            threadId: thread.threadId,
            title: thread.title,
            lastMessage: "",
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          };

          setThreads((current) => [
            newThread,
            ...current,
          ]);
        }
      }

      /*
       * ========================================================
       * PROCESSING STATUS
       * ========================================================
       */

      let statusStep = 0;

      const statuses = file
        ? [
            "Reading your document...",
            "Analyzing the document...",
            "Looking through relevant legal provisions...",
            "Preparing your answer...",
          ]
        : [
            "Understanding your question...",
            "Looking through relevant legal provisions...",
            "Preparing your answer...",
          ];

      const statusTimer = window.setInterval(() => {
        statusStep =
          (statusStep + 1) % statuses.length;

        setStatus(statuses[statusStep]);
      }, 1800);

      try {
        /*
         * ======================================================
         * SEND TO BACKEND
         * ======================================================
         */

        const response = file
          ? await sendMessageWithDocument(
              currentThreadId,
              userMessage,
              file
            )
          : await sendChatMessage({
              threadId: currentThreadId,
              query: userMessage,
            });

        /*
         * ======================================================
         * ADD AI RESPONSE
         * ======================================================
         */

        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content: response.answer,
          },
        ]);

        /*
         * ======================================================
         * UPDATE RECENT THREAD
         * ======================================================
         */

        if (user) {
          setThreads((current) =>
            current
              .map((thread) =>
                thread.threadId === currentThreadId
                  ? {
                      ...thread,
                      lastMessage:
                        response.answer.slice(0, 500),
                      updatedAt:
                        new Date().toISOString(),
                    }
                  : thread
              )
              .sort(
                (a, b) =>
                  new Date(b.updatedAt).getTime() -
                  new Date(a.updatedAt).getTime()
              )
          );
        }
      } finally {
        window.clearInterval(statusTimer);
      }

      setStatus("");
    } catch (error) {
      console.error(
        "Chat request failed:",
        error
      );

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

  /*
   * ============================================================
   * NEW CHAT
   * ============================================================
   */

  const newChat = () => {
    if (isLoading) {
      return;
    }

    setMessages([]);
    setThreadId(null);
    setStatus("");
  };

  /*
   * ============================================================
   * PROVIDER
   * ============================================================
   */

  return (
    <ChatContext.Provider
      value={{
        messages,
        threadId,
        threads,

        isLoading,
        isLoadingThreads,
        isLoadingMessages,

        status,
        hasMessages,

        sendMessage,
        newChat,
        selectThread,
        refreshThreads,
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