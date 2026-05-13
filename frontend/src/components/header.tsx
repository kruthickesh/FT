"use client";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { BookOpen, MessageSquare, Settings, LogOut } from "lucide-react";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold text-primary">
          <BookOpen size={24} />
          Find My Tutor
        </Link>
        {user ? (
          <nav className="flex items-center gap-4">
            <Link href="/messages" className="text-gray-600 hover:text-primary flex items-center gap-1">
              <MessageSquare size={18} />
              <span className="hidden sm:inline">Messages</span>
            </Link>
            <Link href="/settings" className="text-gray-600 hover:text-primary flex items-center gap-1">
              <Settings size={18} />
              <span className="hidden sm:inline">Settings</span>
            </Link>
            <Button variant="outline" size="sm" onClick={logout} className="flex items-center gap-1">
              <LogOut size={16} />
              Sign Out
            </Button>
          </nav>
        ) : (
          <nav className="flex items-center gap-4">
            <Link href="/auth"><Button size="sm">Sign In</Button></Link>
          </nav>
        )}
      </div>
    </header>
  );
}