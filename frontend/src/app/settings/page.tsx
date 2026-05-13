"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function SettingsPage() {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) router.push("/auth");
  }, [user, loading, router]);

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6">Settings</h1>
        <div className="bg-white rounded-lg border p-6">
          <h2 className="text-xl font-semibold mb-4">Profile Information</h2>
          <div className="space-y-4">
            <div><label className="block text-sm font-medium text-gray-700">Name</label><p className="mt-1">{user?.full_name}</p></div>
            <div><label className="block text-sm font-medium text-gray-700">Email</label><p className="mt-1">{user?.email}</p></div>
            <div><label className="block text-sm font-medium text-gray-700">Role</label><p className="mt-1 capitalize">{user?.role}</p></div>
          </div>
        </div>
      </div>
    </div>
  );
}