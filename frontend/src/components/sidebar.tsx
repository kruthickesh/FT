"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";
import { BookOpen, Users, Star, Calendar, MessageSquare, Settings, LayoutDashboard } from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();
  const { user } = useAuth();

  const studentLinks = [
    { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
    { href: "/", icon: BookOpen, label: "Find Tutors" },
    { href: "/bookings", icon: Calendar, label: "My Bookings" },
    { href: "/messages", icon: MessageSquare, label: "Messages" },
    { href: "/settings", icon: Settings, label: "Settings" },
  ];

  const tutorLinks = [
    { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
    { href: "/tutor/profile", icon: Users, label: "My Profile" },
    { href: "/bookings", icon: Calendar, label: "Bookings" },
    { href: "/messages", icon: MessageSquare, label: "Messages" },
    { href: "/settings", icon: Settings, label: "Settings" },
  ];

  const links = user?.role === "tutor" ? tutorLinks : studentLinks;

  return (
    <aside className="w-64 bg-white border-r min-h-screen hidden md:block">
      <div className="p-4">
        <h2 className="text-xl font-bold text-primary mb-4">Find My Tutor</h2>
        <nav className="space-y-1">
          {links.map((link) => (
            <Link key={link.href} href={link.href}>
              <div className={cn("flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors", pathname === link.href && "bg-primary/10 text-primary")}>
                <link.icon size={20} />
                <span>{link.label}</span>
              </div>
            </Link>
          ))}
        </nav>
      </div>
    </aside>
  );
}