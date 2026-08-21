import api from "@/lib/api";

export interface ChatThread {
  _id: string;
  userId: string;
  threadId: string;
  title: string;
  lastMessage?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateThreadResponse {
  threadId: string;
  title: string;
  isGuest: boolean;
}

export interface GetThreadsResponse {
  threads: ChatThread[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export const createThread = async (
  title?: string
): Promise<CreateThreadResponse> => {
  const response = await api.post("/api/threads", {
    title,
  });

  return response.data.data;
};

export const getThreads = async (
  page: number = 1,
  limit: number = 20
): Promise<GetThreadsResponse> => {
  const response = await api.get("/api/threads", {
    params: {
      page,
      limit,
    },
  });

  return response.data.data;
};