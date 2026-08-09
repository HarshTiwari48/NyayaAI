import { Response } from "express";
import {
  createThread,
  getUserThreads,
  getThreadById,
} from "../services/chatThread.service";
import ApiResponse from "../utils/ApiResponse";
import AsyncHandler from "../utils/AsyncHandler";
import { OptionalAuthRequest } from "../middlewares/optionalAuth.middleware";
import ApiError from "../utils/ApiError";

export const createChatThread = AsyncHandler(
  async (req: OptionalAuthRequest, res: Response) => {
    const { title } = req.body;

    const thread = await createThread(req.userId, title);

    res
      .status(201)
      .json(
        new ApiResponse(
          201,
          thread,
          "Chat thread created successfully"
        )
      );
  }
);

export const getChatThreads = AsyncHandler(
  async (req: OptionalAuthRequest, res: Response) => {
    if (!req.userId) {
      throw new ApiError(
        401,
        "Login required to view chat history"
      );
    }

    const threads = await getUserThreads(req.userId);

    res
      .status(200)
      .json(
        new ApiResponse(
          200,
          threads,
          "Chat threads fetched successfully"
        )
      );
  }
);

export const getChatThread = AsyncHandler(
  async (req: OptionalAuthRequest, res: Response) => {
    if (!req.userId) {
      throw new ApiError(
        401,
        "Login required to view chat history"
      );
    }

    const threadId = req.params.threadId as string;

    const thread = await getThreadById(
      threadId,
      req.userId
    );

    res
      .status(200)
      .json(
        new ApiResponse(
          200,
          thread,
          "Chat thread fetched successfully"
        )
      );
  }
);