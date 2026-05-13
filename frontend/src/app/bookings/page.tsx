"use client";
import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function BookingsPage() {
  const { user, loading } = useAuth();
  const [bookings, setBookings] = useState<any[]>([]);
  const [asTutor, setAsTutor] = useState(false);

  useEffect(() => {
    if (user) loadBookings();
  }, [user, asTutor]);

  const loadBookings = async () => {
    try {
      const data = await apiRequest(`/bookings/my?as_tutor=${asTutor}`);
      setBookings(data);
    } catch {}
  };

  const updateStatus = async (id: string, status: string) => {
    try {
      await apiRequest(`/bookings/${id}/status?status=${status}`, { method: "PUT" });
      loadBookings();
    } catch (err: any) { alert(err.message); }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6">My Bookings</h1>
        <div className="flex gap-2 mb-6">
          <Button variant={!asTutor ? "default" : "outline"} onClick={() => setAsTutor(false)}>As Student</Button>
          <Button variant={asTutor ? "default" : "outline"} onClick={() => setAsTutor(true)}>As Tutor</Button>
        </div>
        {bookings.length === 0 ? (<Card><CardContent className="p-6 text-center text-gray-500">No bookings found</CardContent></Card>) : (
          <div className="space-y-4">
            {bookings.map((b) => (
              <Card key={b.id}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-lg">{b.subject}</h3>
                      <p className="text-gray-500">Scheduled: {new Date(b.scheduled_at).toLocaleString()}</p>
                      <p className="text-gray-500">Duration: {b.duration_minutes} minutes</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-3 py-1 rounded-full text-sm ${b.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : b.status === 'confirmed' ? 'bg-green-100 text-green-700' : b.status === 'completed' ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-700'}`}>{b.status}</span>
                      <p className="text-lg font-bold mt-2">₹{b.amount}</p>
                    </div>
                  </div>
                  {asTutor && b.status === "pending" && (
                    <div className="mt-4 flex gap-2">
                      <Button size="sm" onClick={() => updateStatus(b.id, "confirmed")}>Accept</Button>
                      <Button size="sm" variant="outline" onClick={() => updateStatus(b.id, "cancelled")}>Decline</Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}