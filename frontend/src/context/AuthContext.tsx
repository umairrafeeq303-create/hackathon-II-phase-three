"use client";

/**
 * Authentication Context Provider
 * Manages global authentication state and provides auth methods to components.
 */
import React, { createContext, useState, useEffect, useCallback } from "react";
import type { User, AuthContextType } from "@/types/auth";
import { api } from "@/lib/api";
import { getAuthToken, setAuthToken, removeAuthToken, getCurrentUser as getStoredUser, setCurrentUser } from "@/lib/auth";

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initAuth = () => {
      const storedToken = getAuthToken();
      const storedUser = getStoredUser();

      if (storedToken && storedUser) {
        setUser(storedUser);
        setToken(storedToken);
      }

      setIsLoading(false);
    };

    initAuth();
  }, []);

  const signin = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await api.signin({ email, password });
      setUser(response.user);
      setToken(response.token);
      setAuthToken(response.token);
      setCurrentUser(response.user);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const signup = useCallback(
    async (name: string, email: string, password: string) => {
      setIsLoading(true);
      try {
        const response = await api.signup({ name, email, password });
        setUser(response.user);
        setToken(response.token);
        setAuthToken(response.token);
        setCurrentUser(response.user);
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    removeAuthToken();
    api.logout();
  }, []);

  const refreshUser = useCallback(async () => {
    if (!token) return;

    try {
      const userData = await api.getCurrentUser();
      setUser(userData);
      setCurrentUser(userData);
    } catch (error) {
      // Token is invalid, logout
      logout();
    }
  }, [token, logout]);

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!user,
    isLoading,
    signin,
    signup,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
