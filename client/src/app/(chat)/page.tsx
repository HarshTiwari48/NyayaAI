"use client";

import { useEffect, useRef } from "react";
import { Scale, LogOut, User } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import ChatInput from "@/components/chat/chat-input";
import { Button } from "@/components/ui/button";
import {
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";

import { useChat } from "@/components/providers/chat-provider";
import { useAuthStore } from "@/stores/auth.store";
import { logout } from "@/services/auth.service";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Home() {
  const router = useRouter();
  const { open } = useSidebar();

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const {
    messages,
    isLoading,
    status,
    hasMessages,
    sendMessage,
  } = useChat();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, isLoading]);

  const user = useAuthStore((state) => state.user);
  const authLoading = useAuthStore((state) => state.isLoading);
  const clearUser = useAuthStore((state) => state.clearUser);

  /*
   * ============================================================
   * USER INFORMATION
   * ============================================================
   */

  const userName =
    typeof user?.name === "string"
      ? user.name
      : "User";

  const userEmail =
    typeof user?.email === "string"
      ? user.email
      : "";

  const initials = userName
    .split(" ")
    .filter(Boolean)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  /*
   * ============================================================
   * LOGOUT
   * ============================================================
   */

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      clearUser();
      router.refresh();
    }
  };

  return (
    <main
      className={`relative h-svh min-h-0 flex-1 overflow-hidden transition-colors duration-500 ${
        hasMessages ? "bg-[#faf9f6]" : "bg-transparent"
      }`}
    >
      {/* ========================================================
          LANDING BACKGROUND
      ======================================================== */}

      {!hasMessages && (
        <div
          className="pointer-events-none absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: "url('/landing-bg.png')",
          }}
        />
      )}

      {/* ========================================================
          CHAT BACKGROUND
      ======================================================== */}

      {hasMessages && (
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div className="absolute left-1/2 top-0 h-125 w-200 -translate-x-1/2 rounded-full bg-[#e8dcc8]/20 blur-3xl" />
        </div>
      )}

      {/* ========================================================
          HEADER
      ======================================================== */}

      <header className="absolute inset-x-0 top-0 z-50 flex h-16 shrink-0 items-center justify-between px-6 sm:px-8">
        {/* Left side */}

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

        {/* ======================================================
            RIGHT SIDE
        ====================================================== */}

        {!authLoading && (
          <div className="flex items-center gap-2">
            {!user ? (
              <>
                <Link href="/login">
                  <Button variant="ghost">
                    Log in
                  </Button>
                </Link>

                <Link href="/register">
                  <Button>
                    Sign up
                  </Button>
                </Link>
              </>
            ) : (
              <div className="flex items-center gap-2">
                {/* User profile pill */}

                <div className="hidden items-center gap-2 rounded-lg border bg-background/80 px-2.5 py-1.5 backdrop-blur-sm sm:flex">
                  <div className="flex size-7 items-center justify-center rounded-full bg-neutral-900 text-[10px] font-medium text-white">
                    {initials || (
                      <User className="size-3.5" />
                    )}
                  </div>

                  <div className="max-w-32">
                    <p className="truncate text-sm font-medium">
                      {userName}
                    </p>

                    {userEmail && (
                      <p className="truncate text-[10px] text-muted-foreground">
                        {userEmail}
                      </p>
                    )}
                  </div>
                </div>

                {/* Mobile avatar */}

                <div className="flex size-9 items-center justify-center rounded-full bg-neutral-900 text-xs font-medium text-white sm:hidden">
                  {initials || (
                    <User className="size-4" />
                  )}
                </div>

                {/* Logout */}

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="gap-2"
                >
                  <LogOut className="size-4" />

                  <span className="hidden sm:inline">
                    Log out
                  </span>
                </Button>
              </div>
            )}
          </div>
        )}
      </header>

      {/* ========================================================
          MAIN CONTENT
      ======================================================== */}

      <div className="relative z-10 h-full min-h-0">

        {/* ======================================================
            LANDING
        ====================================================== */}

        {!hasMessages && (
          <div className="flex h-full items-center justify-center overflow-hidden px-6 pb-20 pt-16">
            <div className="w-full max-w-4xl">

              <div className="mb-10 text-center">
                <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
                  Understand Indian Law
                </h1>

                <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
                  Ask questions about Indian law, understand
                  legal situations, explore relevant provisions,
                  and analyze your legal documents with NyayaAI.
                </p>
              </div>

              <ChatInput
                onSend={sendMessage}
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
                NyayaAI provides informational assistance and is
                not a substitute for professional legal advice.
              </p>

            </div>
          </div>
        )}

        {/* ======================================================
            CHAT
        ====================================================== */}

        {hasMessages && (
          <div className="flex h-full min-h-0 flex-col">

            {/* Messages */}

            <div className="min-h-0 flex-1 overflow-y-auto">
              <div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-6 pb-10 pt-24">

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

                          <div className="prose prose-sm max-w-none">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                              {message.content}
                            </ReactMarkdown>
                          </div>
                        </>
                      )}
                    </div>
                  );
                })}

                {/* AI processing */}

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

                {/* Auto-scroll target */}

                <div ref={messagesEndRef} />

              </div>
            </div>

            {/* ==================================================
                COMPOSER
            ================================================== */}

            <div className="shrink-0 bg-linear-to-t from-[#faf9f6] via-[#faf9f6]/95 to-transparent px-6 pb-6 pt-6">
              <div className="mx-auto w-full max-w-3xl">

                <ChatInput
                  onSend={sendMessage}
                  onAttachment={() => {
                    console.log("Attachment clicked");
                  }}
                />

                <p className="mt-3 text-center text-[11px] text-muted-foreground">
                  NyayaAI provides informational assistance and
                  is not a substitute for professional legal advice.
                </p>

              </div>
            </div>

          </div>
        )}

      </div>
    </main>
  );
}