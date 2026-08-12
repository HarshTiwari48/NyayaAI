import { Response } from "express";
import { sendMessage } from "../services/chat.service";
import ApiResponse from "../utils/ApiResponse";
import AsyncHandler from "../utils/AsyncHandler";
import { OptionalAuthRequest } from "../middlewares/optionalAuth.middleware";
import ApiError from "../utils/ApiError";

export const sendChatMessage = AsyncHandler(
  async (req: OptionalAuthRequest, res: Response) => {
    console.log("🔥🔥 CHAT CONTROLLER CALLED");
    const { threadId, query } = req.body;

    if (!threadId || !query) {
      throw new ApiError(400, "threadId and query are required");
    }

    const result = await sendMessage(
      threadId,
      query,
      req.userId
    );

    res
      .status(200)
      .json(
        new ApiResponse(
          200,
          result,
          "Message processed successfully"
        )
      );
  }
);