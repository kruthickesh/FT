"use client";
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { apiRequest } from "./utils";
import { User } from "@/types";

interface AuthContextType { user: User | null; loading: boolean; login: (email: string, password: string) => Promise<void>; register: (email: string, password: string, full_name: string, role: string) => Promise<void>; logout: () => void; }

const AuthContext = createContext<AuthContextType>({ user: null, loading: true, login: async () => {}, register: async () => {}, logout: () => {} });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      apiRequest("/auth/me")
        .then(setUser)
        .catch(() => localStorage.removeItem("token"))
        .finally(() => setLoading(false));
    } else setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: formData });
    if (!res.ok) throw new Error("Login failed");
    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    const userData = await apiRequest("/auth/me");
    setUser(userData);
  };

  const register = async (email: string, password: string, full_name: string, role: string) => {
    const data = await apiRequest("/auth/register", { method: "POST", body: JSON.stringify({ email, password, full_name, role }) });
    localStorage.setItem("token", data.access_token);
    const userData = await apiRequest("/auth/me");
    setUser(userData);
  };

  const logout = () => { localStorage.removeItem("token"); setUser(null); };

  return <AuthContext.Provider value={{ user, loading, login, register, logout }}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);