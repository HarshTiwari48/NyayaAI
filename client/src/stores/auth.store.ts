import { create } from "zustand";

interface AuthState {
  user: Record<string, unknown> | null;
  isLoading: boolean;
  setUser: (user: Record<string, unknown> | null) => void;
  setLoading: (loading: boolean) => void;
  clearUser: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,

  setUser: (user) => set({ user }),

  setLoading: (isLoading) => set({ isLoading }),

  clearUser: () => set({ user: null }),
}));