"use client";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  ArrowUp,
  FileText,
  Loader2,
  Paperclip,
  X,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ChatInputProps {
  onSend?: (
    message: string,
    file?: File
  ) => void;

  disabled?: boolean;
}

export default function ChatInput({
  onSend,
  disabled = false,
}: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  const textareaRef =
    useRef<HTMLTextAreaElement>(null);

  const fileInputRef =
    useRef<HTMLInputElement>(null);

  const resizeTextarea = () => {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "auto";

    textarea.style.height = `${Math.min(
      textarea.scrollHeight,
      180
    )}px`;
  };

  useEffect(() => {
    resizeTextarea();
  }, [message]);

  /*
   * ============================================================
   * FILE SELECTION
   * ============================================================
   */

  const handleAttachmentClick = () => {
    if (disabled) return;

    fileInputRef.current?.click();
  };

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    const isPdf =
      file.type === "application/pdf" ||
      file.name.toLowerCase().endsWith(".pdf");

    if (!isPdf) {
      event.target.value = "";
      return;
    }

    setSelectedFile(file);
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  /*
   * ============================================================
   * SEND
   * ============================================================
   */

  const handleSend = () => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) return;

    onSend?.(
      trimmedMessage,
      selectedFile ?? undefined
    );

    setMessage("");
    setSelectedFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !disabled
    ) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div
      className={`rounded-2xl border bg-background p-3 shadow-sm transition-shadow focus-within:shadow-md ${
        disabled ? "opacity-80" : ""
      }`}
    >
      {/* Hidden PDF input */}

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
        hidden
      />

      {/* Selected file */}

      {selectedFile && (
        <div className="mb-3 flex items-center justify-between rounded-lg border bg-muted/50 px-3 py-2">
          <div className="flex min-w-0 items-center gap-2">
            <FileText className="size-4 shrink-0 text-muted-foreground" />

            <span className="truncate text-sm">
              {selectedFile.name}
            </span>
          </div>

          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={handleRemoveFile}
            disabled={disabled}
            className="size-7 shrink-0"
            aria-label="Remove document"
          >
            <X className="size-4" />
          </Button>
        </div>
      )}

      {/* Text input */}

      <Textarea
        ref={textareaRef}
        value={message}
        onChange={(event) =>
          setMessage(event.target.value)
        }
        onKeyDown={handleKeyDown}
        placeholder={
          disabled
            ? "NyayaAI is thinking..."
            : selectedFile
              ? "Ask a question about this document..."
              : "Ask NyayaAI anything..."
        }
        disabled={disabled}
        rows={1}
        className="min-h-10 resize-none border-0 px-2 py-2 shadow-none focus-visible:ring-0"
      />

      <div className="mt-2 flex items-center justify-between">
        {/* Attachment */}

        <Button
          type="button"
          variant="ghost"
          size="icon"
          onClick={handleAttachmentClick}
          disabled={disabled}
          aria-label="Upload document"
        >
          <Paperclip className="size-4" />
        </Button>

        {/* Send */}

        <Button
          type="button"
          size="icon"
          onClick={handleSend}
          disabled={!message.trim() || disabled}
          aria-label="Send message"
        >
          {disabled ? (
            <Loader2 className="size-4 animate-spin" />
          ) : (
            <ArrowUp className="size-4" />
          )}
        </Button>
      </div>
    </div>
  );
}