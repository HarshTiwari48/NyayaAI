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
  userId: string,
  page: number = 1,
  limit: number = 20
) => {
  const thread = await ChatThread.findOne({
    threadId,
    userId,
  });

  if (!thread) {
    throw new ApiError(404, "Chat thread not found");
  }

  const skip = (page - 1) * limit;

  const [messages, total] = await Promise.all([
    ChatMessage.find({ threadId })
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit),

    ChatMessage.countDocuments({ threadId }),
  ]);

  return {
    messages: messages.reverse(),
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  };
};