import ChatThread from "../models/chatThread.model";
import ApiError from "../utils/ApiError";
import { v4 as uuidv4 } from "uuid";

export const createThread = async (
  userId?: string,
  title?: string
) => {
  const threadId = uuidv4();

  // Guest user
  if (!userId) {
    return {
      threadId,
      title: title?.trim() || "New Chat",
      isGuest: true,
    };
  }

  // Logged-in user
  const thread = await ChatThread.create({
    userId,
    threadId,
    title: title?.trim() || "New Chat",
  });

  return {
    ...thread.toObject(),
    isGuest: false,
  };
};

export const getUserThreads = async (
  userId: string,
  page: number = 1,
  limit: number = 20
) => {
  const skip = (page - 1) * limit;

  const [threads, total] = await Promise.all([
    ChatThread.find({ userId })
      .sort({ updatedAt: -1 })
      .skip(skip)
      .limit(limit),

    ChatThread.countDocuments({ userId }),
  ]);

  return {
    threads,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  };
};

export const getThreadById = async (
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

  return thread;
};