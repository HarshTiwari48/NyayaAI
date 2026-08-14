import { z } from "zod";

export const chatMessageSchema = z.object({
  threadId: z.string().uuid("Invalid thread ID"),
  query: z
    .string()
    .trim()
    .min(1, "Query is required")
    .max(5000, "Query is too long"),
});