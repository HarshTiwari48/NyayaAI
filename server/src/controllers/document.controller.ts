import { Response } from "express";
import { analyzeDocument, deleteDocument, getThreadDocuments } from "../services/document.service";
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

export const getThreadDocumentsController = AsyncHandler(
  async (req: OptionalAuthRequest, res: Response) => {
    if (!req.userId) {
      throw new ApiError(
        401,
        "Login required to view documents"
      );
    }

    const threadId = req.params.threadId as string;

    const documents = await getThreadDocuments(
      req.userId,
      threadId
    );

    res.status(200).json(
      new ApiResponse(
        200,
        documents,
        "Documents fetched successfully"
      )
    );
  }
);

export const deleteDocumentController = AsyncHandler(
  async (req: OptionalAuthRequest, res: Response) => {
    if (!req.userId) {
      throw new ApiError(
        401,
        "Login required to delete documents"
      );
    }

    const documentId = req.params.documentId as string;

    const document = await deleteDocument(
      req.userId,
      documentId
    );

    res.status(200).json(
      new ApiResponse(
        200,
        document,
        "Document deleted successfully"
      )
    );
  }
);