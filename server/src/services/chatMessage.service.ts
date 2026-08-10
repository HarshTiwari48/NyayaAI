import ChatMessage from "../models/chatMessage.model";
import ChatThread from "../models/chatThread.model";
import ApiError from "../utils/ApiError";

export const saveMessage = async (
  threadId: string,
  role: "user" | "assistant",
  content: string
) => {
  const message = await ChatMessage.create({
    threadId,
    role,
    content,
  });

  return message;
};

export const getThreadMessages = async (
  threadId: string,
  userId: string
) => {
  const thread = await ChatThread.findOne({
    threadId,
    userId,
  });

  if (!thread) {
    throw new ApiError(404, "Chat thread not found");
  }

  return ChatMessage.find({ threadId }).sort({
    createdAt: 1,
  });
};