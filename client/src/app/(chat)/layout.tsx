"use client";

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";

import AppSidebar from "@/components/sidebar/app-sidebar";
import { ChatProvider } from "@/components/providers/chat-provider";

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ChatProvider>
      <SidebarProvider defaultOpen={false}>
        <AppSidebar />

        <SidebarInset className="h-svh min-w-0 overflow-hidden">
          {children}
        </SidebarInset>
      </SidebarProvider>
    </ChatProvider>
  );
}