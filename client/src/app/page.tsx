"use client";

import ChatInput from "@/components/chat/chat-input";

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto flex min-h-screen max-w-4xl flex-col items-center justify-center px-6">
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">
            Understand Indian Law
          </h1>

          <p className="mt-4 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
            Ask questions about Indian law, understand legal situations,
            explore relevant provisions, and analyze your legal documents
            with NyayaAI.
          </p>
        </div>

        <div className="w-full max-w-3xl">
          <ChatInput
            onSend={(message) => {
              console.log("Message:", message);
            }}
            onAttachment={() => {
              console.log("Attachment clicked");
            }}
          />

          <p className="mt-3 text-center text-xs text-muted-foreground">
            NyayaAI provides informational assistance and is not a substitute
            for professional legal advice.
          </p>
        </div>
      </div>
    </main>
  );
}