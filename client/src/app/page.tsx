"use client";

import { useState } from "react";
import { Scale } from "lucide-react";

import ChatInput from "@/components/chat/chat-input";
import { Button } from "@/components/ui/button";
import {
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";

import { createThread } from "@/services/chatThread.service";
import { sendMessage } from "@/services/chat.service";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const { open } = useSidebar();

  const [messages, setMessages] = useState<Message[]>([]);
  const [threadId, setThreadId] = useState<string | null>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState("");

  const hasMessages = messages.length > 0;
  const handleNewChat = () => {
  if (isLoading) {
    return;
  }

  setMessages([]);
  setThreadId(null);
  setStatus("");
};

  const handleSend = async (message: string) => {
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
       * Create a thread automatically for the first message.
       */
      if (!currentThreadId) {
        const thread = await createThread();

        currentThreadId = thread.threadId;
        setThreadId(currentThreadId);
      }

      /*
       * Fake processing status while AI is working.
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
        const response = await sendMessage({
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

  return (
    <main
      className={`relative h-svh min-h-0 flex-1 overflow-hidden transition-colors duration-500 ${
        hasMessages ? "bg-[#faf9f6]" : "bg-transparent"
      }`}
    >
      {/* =========================================================
          BACKGROUND
      ========================================================= */}

      {!hasMessages && (
        <div
          className="pointer-events-none absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: "url('/landing-bg.png')",
          }}
        />
      )}

      {hasMessages && (
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div className="absolute left-1/2 top-0 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-[#e8dcc8]/20 blur-3xl" />
        </div>
      )}

      {/* =========================================================
          FIXED APP HEADER
      ========================================================= */}

      <header className="absolute inset-x-0 top-0 z-50 flex h-16 shrink-0 items-center justify-between px-6 sm:px-8">
        <div className="flex items-center gap-2">
          {!open && <SidebarTrigger />}

          {!open && (
            <>
              <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                <Scale className="size-4" />
              </div>

              <span className="text-lg font-semibold tracking-tight">
                NyayaAI
              </span>
            </>
          )}
        </div>

        {/* These now stay fixed because the header is absolute */}
        <div className="flex items-center gap-2">
          <Button variant="ghost">
            Log in
          </Button>

          <Button>
            Sign up
          </Button>
        </div>
      </header>

      {/* =========================================================
          CONTENT
      ========================================================= */}

      <div className="relative z-10 h-full min-h-0">
        {/* =======================================================
            LANDING STATE
        ======================================================= */}

        {!hasMessages && (
          <div className="flex h-full items-center justify-center overflow-hidden px-6 pb-20 pt-16">
            <div className="w-full max-w-4xl">
              <div className="mb-10 text-center">
                <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
                  Understand Indian Law
                </h1>

                <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
                  Ask questions about Indian law, understand legal situations,
                  explore relevant provisions, and analyze your legal
                  documents with NyayaAI.
                </p>
              </div>

              <ChatInput
                onSend={handleSend}
                onAttachment={() => {
                  console.log("Attachment clicked");
                }}
              />

              <div className="mt-4 flex justify-center gap-3 text-xs text-muted-foreground">
                <span>Indian law</span>
                <span>•</span>
                <span>Case law</span>
                <span>•</span>
                <span>Legal documents</span>
              </div>

              <p className="mt-6 text-center text-xs text-muted-foreground">
                NyayaAI provides informational assistance and is not a
                substitute for professional legal advice.
              </p>
            </div>
          </div>
        )}

        {/* =======================================================
            CHAT STATE
        ======================================================= */}

        {hasMessages && (
          <div className="flex h-full min-h-0 flex-col">
            {/* =================================================
                SCROLLABLE MESSAGE AREA

                IMPORTANT:
                This is now the ONLY thing that scrolls.
            ================================================= */}

            <div className="min-h-0 flex-1 overflow-y-auto">
              <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-6 pb-44 pt-24">
                {messages.map((message, index) => {
                  const isUser = message.role === "user";

                  return (
                    <div
                      key={index}
                      className={
                        isUser
                          ? "ml-auto max-w-[75%] rounded-2xl bg-neutral-900 px-5 py-3.5 text-sm leading-6 text-white shadow-sm"
                          : "max-w-[85%] text-[15px] leading-7 text-foreground"
                      }
                    >
                      {isUser ? (
                        message.content
                      ) : (
                        <>
                          <div className="mb-2 flex items-center gap-2 text-sm font-medium">
                            <div className="flex size-6 items-center justify-center rounded-md bg-neutral-900 text-white">
                              <Scale className="size-3" />
                            </div>

                            <span>NyayaAI</span>
                          </div>

                          <div className="whitespace-pre-wrap">
                            {message.content}
                          </div>
                        </>
                      )}
                    </div>
                  );
                })}

                {/* =================================================
                    AI PROCESSING
                ================================================= */}

                {isLoading && (
                  <div className="max-w-[85%] text-[14px] text-muted-foreground">
                    <div className="mb-2 flex items-center gap-2 text-sm font-medium text-foreground">
                      <div className="flex size-6 items-center justify-center rounded-md bg-neutral-900 text-white">
                        <Scale className="size-3" />
                      </div>

                      <span>NyayaAI</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span>{status}</span>

                      <span className="flex gap-1">
                        <span className="size-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.3s]" />
                        <span className="size-1.5 animate-bounce rounded-full bg-muted-foreground [animation-delay:-0.15s]" />
                        <span className="size-1.5 animate-bounce rounded-full bg-muted-foreground" />
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* =================================================
                FIXED COMPOSER AREA

                Since the parent is h-full and the messages
                are the flex-1 scroll container, this remains
                at the bottom.
            ================================================= */}

            <div className="shrink-0 bg-gradient-to-t from-[#faf9f6] via-[#faf9f6]/95 to-transparent px-6 pb-6 pt-6">
              <div className="mx-auto w-full max-w-3xl">
                <ChatInput
                  onSend={handleSend}
                  onAttachment={() => {
                    console.log("Attachment clicked");
                  }}
                />

                <p className="mt-3 text-center text-[11px] text-muted-foreground">
                  NyayaAI provides informational assistance and is not a
                  substitute for professional legal advice.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}