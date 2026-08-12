console.log("🔥🔥🔥 AI SERVICE FILE LOADED");
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
  console.log("🔥🔥🔥 ANALYZE QUERY CALLED");

    console.log("🚀 Calling FastAPI...");
    console.log("URL:", `${env.FASTAPI_URL}/analyze`);
    console.log("threadId:", threadId);
    console.log("query:", query);
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
  console.log("🔥 AI SERVICE ERROR");
  console.log("URL:", `${env.FASTAPI_URL}/analyze`);
  console.log("ERROR:", error);

  if (axios.isAxiosError(error)) {
    console.log("CODE:", error.code);
    console.log("MESSAGE:", error.message);
    console.log("STATUS:", error.response?.status);
    console.log("RESPONSE:", error.response?.data);
  }

  throw new Error("Unable to connect to AI service");
}
};