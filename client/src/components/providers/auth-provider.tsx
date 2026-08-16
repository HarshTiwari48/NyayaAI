"use client";

import { useEffect } from "react";

import { getMe } from "@/services/auth.service";
import { useAuthStore } from "@/stores/auth.store";

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const setUser = useAuthStore((state) => state.setUser);
  const setLoading = useAuthStore((state) => state.setLoading);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const response = await getMe();

        setUser(response.data);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, [setUser, setLoading]);

  return children;
}