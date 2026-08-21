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

export interface ChatMessage {
  _id: string;
  threadId: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
}

export interface ThreadMessagesResponse {
  messages: ChatMessage[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export const sendMessage = async (
  data: SendMessageData
): Promise<AIResponse> => {
  const response = await api.post(
    "/api/chat/message",
    data
  );

  return response.data.data;
};

export const getThreadMessages = async (
  threadId: string,
  page: number = 1,
  limit: number = 50
): Promise<ThreadMessagesResponse> => {
  const response = await api.get(
    `/api/chat/${threadId}/messages`,
    {
      params: {
        page,
        limit,
      },
    }
  );

  return response.data.data;
};