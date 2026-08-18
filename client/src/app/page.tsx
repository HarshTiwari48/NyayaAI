"use client";

import { useState } from "react";
import { Scale } from "lucide-react";

import ChatInput from "@/components/chat/chat-input";
import { Button } from "@/components/ui/button";
import {
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const { open } = useSidebar();

  const [messages, setMessages] = useState<Message[]>([]);

  const hasMessages = messages.length > 0;

  const handleSend = (message: string) => {
    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: message,
      },
    ]);
  };

  return (
    <main
      className={`relative min-h-svh flex-1 overflow-hidden transition-colors duration-500 ${
        hasMessages ? "bg-[#faf9f6]" : "bg-transparent"
      }`}
    >
      {/* Landing page background */}
      {!hasMessages && (
        <div
          className="pointer-events-none absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: "url('/landing-bg.png')",
          }}
        />
      )}

      {/* Subtle chat background */}
      {hasMessages && (
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute left-1/2 top-0 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-[#e8dcc8]/20 blur-3xl" />
        </div>
      )}

      <div className="relative z-10 flex min-h-svh flex-col">
        {/* Header */}
        <header className="flex h-16 shrink-0 items-center justify-between px-6 sm:px-8">
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

          <div className="flex items-center gap-2">
            <Button variant="ghost">
              Log in
            </Button>

            <Button>
              Sign up
            </Button>
          </div>
        </header>

        {/* ================= LANDING STATE ================= */}
        {!hasMessages && (
          <div className="flex flex-1 items-center justify-center px-6 pb-20">
            <div className="w-full max-w-4xl">
              <div className="mb-10 text-center">
                <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
                  Understand Indian Law
                </h1>

                <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
                  Ask questions about Indian law, understand legal situations,
                  explore relevant provisions, and analyze your legal documents
                  with NyayaAI.
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
                NyayaAI provides informational assistance and is not a substitute
                for professional legal advice.
              </p>
            </div>
          </div>
        )}

        {/* ================= CHAT STATE ================= */}
        {hasMessages && (
          <div className="flex min-h-0 flex-1 flex-col">
            {/* Conversation */}
            <div className="flex-1 overflow-y-auto">
              <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-6 py-10">
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

                          {message.content}
                        </>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Composer */}
            <div className="sticky bottom-0 bg-gradient-to-t from-[#faf9f6] via-[#faf9f6]/95 to-transparent px-6 pb-6 pt-10">
              <div className="mx-auto w-full max-w-3xl">
                <ChatInput
                  onSend={handleSend}
                  onAttachment={() => {
                    console.log("Attachment clicked");
                  }}
                />

                <p className="mt-3 text-center text-[11px] text-muted-foreground">
                  NyayaAI provides informational assistance and is not a substitute
                  for professional legal advice.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}