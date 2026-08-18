import {
  FileText,
  LogIn,
  MessageSquarePlus,
  Scale,
} from "lucide-react";

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

export default function AppSidebar() {
  return (
    <Sidebar variant="floating" collapsible="offcanvas">
      {/* Logo */}
      <SidebarHeader className="px-3 py-4">
  <div className="flex items-center justify-between px-2">
    <div className="flex items-center gap-2">
      <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
        <Scale className="size-4" />
      </div>

      <span className="text-base font-semibold tracking-tight">
        NyayaAI
      </span>
    </div>

    <SidebarTrigger />
  </div>
</SidebarHeader>

      {/* Sidebar content */}
      <SidebarContent className="px-2">
        {/* New Chat */}
        <SidebarGroup className="py-2">
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  className="h-10 rounded-lg"
                  tooltip="New chat"
                >
                  <MessageSquarePlus className="size-4" />
                  <span>New chat</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        {/* Recent chats */}
        <SidebarGroup className="pt-2">
          <SidebarGroupLabel className="px-2 text-xs font-medium text-muted-foreground">
            Recent
          </SidebarGroupLabel>

          <SidebarGroupContent>
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
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      {/* Guest footer */}
      <SidebarFooter className="p-3">
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
              <SidebarMenuButton className="h-9 rounded-lg bg-background">
                <LogIn className="size-4" />
                <span>Log in</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}