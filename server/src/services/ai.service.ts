import axios from "axios";
import { env } from "../config/env";

interface AIResponse {
  answer: string;
  facts: string[];
  legal_issues: string[];
  verified: boolean;
}

export const analyzeQuery = async (
  threadId: string,
  query: string
): Promise<AIResponse> => {
  try {
    const response = await axios.post<AIResponse>(
      `${env.FASTAPI_URL}/analyze`,
      {
        query,
      },
      {
        params: {
          thread_id: threadId,
        },
        timeout: 120000,
      }
    );

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.code === "ECONNABORTED") {
        throw new Error("AI service request timed out");
      }

      if (error.response) {
        throw new Error(
          `AI service error: ${error.response.status}`
        );
      }
    }

    throw new Error("Unable to connect to AI service");
  }
};