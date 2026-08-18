"use client";

import { Scale } from "lucide-react";

import ChatInput from "@/components/chat/chat-input";
import { Button } from "@/components/ui/button";
import {
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";

export default function Home() {
  const { open } = useSidebar();

  return (
    <main
      className="min-h-svh flex-1 bg-cover bg-center bg-no-repeat"
      style={{
        backgroundImage: "url('/landing-bg.png')",
      }}
    >
      {/* Top bar */}
      <header className="flex h-16 items-center justify-between px-6 sm:px-8">
        <div className="flex items-center gap-2">
          <SidebarTrigger />

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

      {/* Main content */}
      <div className="flex min-h-[calc(100svh-4rem)] w-full items-center justify-center px-6 pb-20">
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
            onSend={(message) => {
              console.log("Message:", message);
            }}
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
    </main>
  );
}