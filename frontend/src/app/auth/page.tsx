"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useAuth } from "@/lib/auth";

export default function AuthPage() {
  const router = useRouter();
  const { login, register } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ email: "", password: "", full_name: "", role: "student" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isLogin) await login(form.email, form.password);
      else await register(form.email, form.password, form.full_name, form.role);
      router.push("/dashboard");
    } catch (err: any) {
      alert(err.message);
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">{isLogin ? "Welcome Back" : "Create Account"}</CardTitle>
          <p className="text-gray-500 mt-2">{isLogin ? "Sign in to your account" : "Join Find My Tutor"}</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && <Input placeholder="Full Name" value={form.full_name} onChange={e => setForm({...form, full_name: e.target.value})} required />}
            <Input type="email" placeholder="Email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
            <Input type="password" placeholder="Password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} required />
            {!isLogin && (
              <select value={form.role} onChange={e => setForm({...form, role: e.target.value})} className="w-full h-10 border rounded-md px-3">
                <option value="student">I am a Student/Parent</option>
                <option value="tutor">I am a Tutor</option>
              </select>
            )}
            <Button type="submit" className="w-full" disabled={loading}>{loading ? "Please wait..." : (isLogin ? "Sign In" : "Sign Up")}</Button>
          </form>
          <div className="mt-4 text-center text-sm">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button onClick={() => setIsLogin(!isLogin)} className="text-primary hover:underline">{isLogin ? "Sign Up" : "Sign In"}</button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}