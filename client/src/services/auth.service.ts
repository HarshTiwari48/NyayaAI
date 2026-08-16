import api from "@/lib/api";

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export const login = async (data: LoginData) => {
  const response = await api.post("/api/auth/login", data);
  return response.data;
};

export const register = async (data: RegisterData) => {
  const response = await api.post("/api/auth/register", data);
  return response.data;
};

export const getMe = async () => {
  const response = await api.get("/api/auth/me");
  return response.data;
};

export const refresh = async () => {
  const response = await api.post("/api/auth/refresh");
  return response.data;
};

export const logout = async () => {
  const response = await api.post("/api/auth/logout");
  return response.data;
};