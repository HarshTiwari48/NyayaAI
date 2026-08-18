import api from "@/lib/api";

export interface SendMessageData {
  threadId: string;
  query: string;
}

export interface AIResponse {
  answer: string;
  facts: string[];
  legal_issues: string[];
  verified: boolean;
}

export const sendMessage = async (
  data: SendMessageData
): Promise<AIResponse> => {
  const response = await api.post("/api/chat/message", data);

  return response.data.data;
};