import { Response } from "express";
import { analyzeDocument } from "../services/document.service";
import AsyncHandler from "../utils/AsyncHandler";
import ApiResponse from "../utils/ApiResponse";
import ApiError from "../utils/ApiError";
import { OptionalAuthRequest } from "../middlewares/optionalAuth.middleware";

export const analyzeDocumentController = AsyncHandler(
  async (req: OptionalAuthRequest, res: Response) => {
    const { threadId, query } = req.body;

    if (!threadId || !query) {
      throw new ApiError(
        400,
        "threadId and query are required"
      );
    }

    if (!req.file) {
      throw new ApiError(400, "PDF file is required");
    }

    const result = await analyzeDocument(
      req.userId,
      threadId,
      query,
      req.file
    );

    res.status(200).json(
      new ApiResponse(
        200,
        result,
        "Document analyzed successfully"
      )
    );
  }
);