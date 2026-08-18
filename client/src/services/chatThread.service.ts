import api from "@/lib/api";

export interface CreateThreadResponse {
  threadId: string;
  title: string;
  isGuest: boolean;
}

export const createThread = async (
  title?: string
): Promise<CreateThreadResponse> => {
  const response = await api.post("/api/threads", {
    title,
  });

  return response.data.data;
};