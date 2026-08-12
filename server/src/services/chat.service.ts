import ChatThread from "../models/chatThread.model";
import ChatMessage from "../models/chatMessage.model";
import ApiError from "../utils/ApiError";
import { analyzeQuery } from "./ai.service";

export const sendMessage = async (
  threadId: string,
  query: string,
  userId?: string
) => {
  console.log("🔥🔥 SEND MESSAGE CALLED");
  // Logged-in user → verify thread ownership
  if (userId) {
    const thread = await ChatThread.findOne({
      threadId,
      userId,
    });

    if (!thread) {
      throw new ApiError(404, "Chat thread not found");
    }
  }

  // Save user message only for logged-in users
  if (userId) {
    await ChatMessage.create({
      threadId,
      role: "user",
      content: query,
    });
  }

  // Send query to FastAPI
  const aiResponse = await analyzeQuery(
    threadId,
    query
  );

  // Save AI response only for logged-in users
  if (userId) {
    await ChatMessage.create({
      threadId,
      role: "assistant",
      content: aiResponse.answer,
    });

    await ChatThread.findOneAndUpdate(
      { threadId, userId },
      {
        lastMessage: aiResponse.answer,
      }
    );
  }

  return aiResponse;
};