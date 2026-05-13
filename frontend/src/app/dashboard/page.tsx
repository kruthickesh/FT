"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiRequest } from "@/lib/utils";
import { useState } from "react";
import { BookOpen, Users, Star, Calendar, MessageSquare, Settings } from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const { user, loading, logout } = useAuth();
  const [stats, setStats] = useState({ bookings: 0, reviews: 0 });

  useEffect(() => {
    if (!loading && !user) router.push("/auth");
    else if (user) {
      if (user.role === "tutor") loadTutorStats();
    }
  }, [user, loading, router]);

  const loadTutorStats = async () => {
    try {
      const bookings = await apiRequest("/bookings/my?as_tutor=true");
      setStats({ bookings: bookings.length || 0, reviews: 0 });
    } catch {}
  };

  if (loading) return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">Find My Tutor</h1>
          <nav className="flex gap-4 items-center">
            <Link href="/messages" className="text-gray-600 hover:text-primary flex items-center gap-1"><MessageSquare size={18} /> Messages</Link>
            <Link href="/settings" className="text-gray-600 hover:text-primary flex items-center gap-1"><Settings size={18} /> Settings</Link>
            <Button variant="outline" size="sm" onClick={logout}>Sign Out</Button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-2">Welcome, {user.full_name}!</h2>
        <p className="text-gray-500 mb-8 capitalize">{user.role} Dashboard</p>

        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card><CardContent className="p-6 text-center">
            <BookOpen className="mx-auto text-primary mb-2" size={32} />
            <p className="text-3xl font-bold">{stats.bookings}</p>
            <p className="text-gray-500">Bookings</p>
          </CardContent></Card>
          <Card><CardContent className="p-6 text-center">
            <Star className="mx-auto text-yellow-500 mb-2" size={32} />
            <p className="text-3xl font-bold">0</p>
            <p className="text-gray-500">Reviews</p>
          </CardContent></Card>
          {user.role === "tutor" ? (
            <>
              <Card><CardContent className="p-6 text-center">
                <Users className="mx-auto text-green-500 mb-2" size={32} />
                <p className="text-3xl font-bold">0</p>
                <p className="text-gray-500">Students</p>
              </CardContent></Card>
              <Card><CardContent className="p-6 text-center">
                <Calendar className="mx-auto text-purple-500 mb-2" size={32} />
                <p className="text-3xl font-bold">0</p>
                <p className="text-gray-500">Sessions</p>
              </CardContent></Card>
            </>
          ) : (
            <>
              <Card><CardContent className="p-6 text-center">
                <BookOpen className="mx-auto text-blue-500 mb-2" size={32} />
                <p className="text-3xl font-bold">0</p>
                <p className="text-gray-500">My Bookings</p>
              </CardContent></Card>
              <Card><CardContent className="p-6 text-center">
                <Users className="mx-auto text-indigo-500 mb-2" size={32} />
                <p className="text-3xl font-bold">0</p>
                <p className="text-gray-500">Favorite Tutors</p>
              </CardContent></Card>
            </>
          )}
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {user.role === "tutor" ? (
            <>
              <Card>
                <CardHeader><CardTitle>Quick Actions</CardTitle></CardHeader>
                <CardContent className="space-y-2">
                  <Link href="/tutor/profile"><Button className="w-full justify-start"><Settings className="mr-2" size={16} /> Edit Profile</Button></Link>
                  <Link href="/tutor/availability"><Button variant="outline" className="w-full justify-start"><Calendar className="mr-2" size={16} /> Set Availability</Button></Link>
                </CardContent>
              </Card>
            </>
          ) : (
            <>
              <Card>
                <CardHeader><CardTitle>Find a Tutor</CardTitle></CardHeader>
                <CardContent>
                  <p className="text-gray-500 mb-4">Search for tutors based on subject, location, and budget</p>
                  <Link href="/"><Button>Search Tutors</Button></Link>
                </CardContent>
              </Card>
            </>
          )}
          <Card>
            <CardHeader><CardTitle>Recent Messages</CardTitle></CardHeader>
            <CardContent>
              <p className="text-gray-500">No messages yet</p>
              <Link href="/messages"><Button variant="outline" className="mt-2">View Messages</Button></Link>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}