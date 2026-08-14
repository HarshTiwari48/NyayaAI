import fs from "fs";
import FormData from "form-data";
import axios from "axios";

import DocumentModel from "../models/document.model";
import ChatThread from "../models/chatThread.model";
import ChatMessage from "../models/chatMessage.model";

import ApiError from "../utils/ApiError";
import { env } from "../config/env";

export const analyzeDocument = async (
  userId: string | undefined,
  threadId: string,
  query: string,
  file: Express.Multer.File
) => {
  // Logged-in users must own the thread
  if (userId) {
    const thread = await ChatThread.findOne({
      threadId,
      userId,
    });

    if (!thread) {
      throw new ApiError(404, "Chat thread not found");
    }
  }

  const formData = new FormData();

  formData.append("query", query);
  formData.append("thread_id", threadId);

  formData.append(
    "file",
    fs.createReadStream(file.path),
    {
      filename: file.originalname,
      contentType: file.mimetype,
    }
  );

  try {
    const response = await axios.post(
      `${env.FASTAPI_URL}/analyze-with-document`,
      formData,
      {
        headers: {
          ...formData.getHeaders(),
        },
        timeout: 120000,
      }
    );

    // Save document and conversation history
    // only for logged-in users
    if (userId) {
      await DocumentModel.create({
        userId,
        threadId,
        fileName: file.originalname,
        fileType: file.mimetype,
      });

      await ChatMessage.create({
        threadId,
        role: "user",
        content: query,
      });

      await ChatMessage.create({
        threadId,
        role: "assistant",
        content: response.data.answer,
      });

      await ChatThread.findOneAndUpdate(
        {
          threadId,
          userId,
        },
        {
          lastMessage: response.data.answer,
        }
      );
    }

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error(
        "FastAPI document error:",
        error.response?.data
      );
    }

    throw new ApiError(
      502,
      "Unable to process document"
    );
  } finally {
    // Remove temporary Express file
    if (fs.existsSync(file.path)) {
      fs.unlinkSync(file.path);
    }
  }
};