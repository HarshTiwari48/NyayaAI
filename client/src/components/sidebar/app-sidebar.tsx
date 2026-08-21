"use client";

import {
  FileText,
  LogIn,
  LogOut,
  MessageSquarePlus,
  Scale,
  User,
} from "lucide-react";
import Link from "next/link";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
} from "@/components/ui/sidebar";

import { useChat } from "@/components/providers/chat-provider";
import { useAuthStore } from "@/stores/auth.store";
import { logout } from "@/services/auth.service";

export default function AppSidebar() {
  const user = useAuthStore((state) => state.user);
  const isLoading = useAuthStore((state) => state.isLoading);
  const clearUser = useAuthStore((state) => state.clearUser);

  const {
    threads,
    selectThread,
    newChat,
    isLoadingThreads,
  } = useChat();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      clearUser();
    }
  };

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
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <Sidebar
      variant="floating"
      collapsible="offcanvas"
      className="z-[60]"
    >
      {/* =====================================================
          HEADER
      ===================================================== */}

      <SidebarHeader className="shrink-0 px-3 py-4">
        <div className="flex items-center justify-between px-2">
          <div className="flex items-center gap-2">
            <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Scale className="size-4" />
            </div>

            <span className="text-base font-semibold tracking-tight">
              NyayaAI
            </span>
          </div>

          <SidebarTrigger className="size-8 shrink-0" />
        </div>
      </SidebarHeader>

      {/* =====================================================
          CONTENT
      ===================================================== */}

      <SidebarContent className="min-h-0 px-2">
        {/* New Chat */}

        <SidebarGroup className="py-2">
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  className="h-10 rounded-lg"
                  tooltip="New chat"
                  onClick={newChat}
                >
                  <MessageSquarePlus className="size-4" />

                  <span>New chat</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        {/* Recent Chats */}

        <SidebarGroup className="pt-2">
          <SidebarGroupLabel className="px-2 text-xs font-medium text-muted-foreground">
            Recent
          </SidebarGroupLabel>

          <SidebarGroupContent>
            {isLoadingThreads ? (
              <div className="space-y-2 px-2 py-2">
                <div className="h-9 animate-pulse rounded-lg bg-muted" />
                <div className="h-9 animate-pulse rounded-lg bg-muted" />
                <div className="h-9 animate-pulse rounded-lg bg-muted" />
              </div>
            ) : threads.length === 0 ? (
              <div className="flex min-h-48 flex-col items-center justify-center px-4 text-center">
                <div className="mb-3 flex size-9 items-center justify-center rounded-full bg-muted">
                  <FileText className="size-4 text-muted-foreground" />
                </div>

                <p className="text-sm font-medium">
                  No conversations yet
                </p>

                <p className="mt-1 max-w-48 text-xs leading-5 text-muted-foreground">
                  Start a conversation and your chats will appear here.
                </p>
              </div>
            ) : (
              <SidebarMenu>
                {threads.map((thread) => (
                  <SidebarMenuItem key={thread.threadId}>
                    <SidebarMenuButton
                      className="h-10 rounded-lg"
                      tooltip={thread.title}
                      onClick={() =>
                        selectThread(thread.threadId)
                      }
                    >
                      <MessageSquarePlus className="size-4 shrink-0" />

                      <span className="truncate">
                        {thread.title}
                      </span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            )}
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      {/* =====================================================
          FOOTER
      ===================================================== */}

      <SidebarFooter className="shrink-0 p-3">
        {isLoading ? (
          <div className="rounded-xl border bg-muted/40 p-3">
            <div className="h-10 animate-pulse rounded-lg bg-muted" />
          </div>
        ) : user ? (
          /* ================= LOGGED IN ================= */

          <div className="rounded-xl border bg-muted/40 p-3">
            <div className="flex items-center gap-3">
              <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-neutral-900 text-xs font-medium text-white">
                {initials || (
                  <User className="size-4" />
                )}
              </div>

              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium">
                  {userName}
                </p>

                <p className="truncate text-xs text-muted-foreground">
                  {userEmail}
                </p>
              </div>
            </div>

            <SidebarMenu className="mt-3">
              <SidebarMenuItem>
                <SidebarMenuButton
                  className="h-9 rounded-lg bg-background"
                  onClick={handleLogout}
                >
                  <LogOut className="size-4" />

                  <span>Log out</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </div>
        ) : (
          /* ================= GUEST ================= */

          <div className="rounded-xl border bg-muted/40 p-3">
            <div className="flex items-start gap-3">
              <div className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-lg bg-background">
                <LogIn className="size-4 text-muted-foreground" />
              </div>

              <div className="min-w-0">
                <p className="text-sm font-medium">
                  You're browsing as a guest
                </p>

                <p className="mt-1 text-xs leading-5 text-muted-foreground">
                  Log in to save and access your conversations.
                </p>
              </div>
            </div>

            <SidebarMenu className="mt-3">
              <SidebarMenuItem>
                <Link
                  href="/login"
                  className="flex h-9 w-full items-center gap-2 rounded-lg bg-background px-2 text-sm"
                >
                  <LogIn className="size-4" />

                  <span>Log in</span>
                </Link>
              </SidebarMenuItem>
            </SidebarMenu>
          </div>
        )}
      </SidebarFooter>
    </Sidebar>
  );
}