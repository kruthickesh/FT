"use client";
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { TutorProfile, Review } from "@/types";
import { Star, MapPin, Clock, Award, CheckCircle, BookOpen } from "lucide-react";

export default function TutorProfilePage() {
  const params = useParams();
  const router = useRouter();
  const { user, loading } = useAuth();
  const [tutor, setTutor] = useState<TutorProfile | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [bookingForm, setBookingForm] = useState({ subject: "", date: "", time: "", notes: "" });
  const [bookingLoading, setBookingLoading] = useState(false);

  useEffect(() => {
    loadTutor();
  }, [params.id]);

  const loadTutor = async () => {
    try {
      const data = await apiRequest(`/tutors/${params.id}`);
      setTutor(data);
      const reviewsData = await apiRequest(`/tutors/${params.id}/reviews`);
      setReviews(reviewsData);
    } catch (err) { console.error(err); }
  };

  const handleBooking = async () => {
    if (!user) { router.push("/auth"); return; }
    setBookingLoading(true);
    try {
      const dateTime = new Date(`${bookingForm.date}T${bookingForm.time}`);
      await apiRequest("/bookings/", {
        method: "POST",
        body: JSON.stringify({
          tutor_id: params.id,
          subject: bookingForm.subject,
          scheduled_at: dateTime.toISOString(),
          duration_minutes: 60,
          notes: bookingForm.notes
        })
      });
      alert("Booking request sent!");
    } catch (err: any) { alert(err.message); }
    finally { setBookingLoading(false); }
  };

  if (!tutor) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <Card className="mb-6">
          <CardContent className="p-6">
            <div className="flex gap-6">
              <div className="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center text-4xl">
                {tutor.user?.avatar_url ? <img src={tutor.user.avatar_url} className="w-full h-full rounded-full object-cover" /> : "👨‍🏫"}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h1 className="text-2xl font-bold">{tutor.user?.full_name}</h1>
                  {tutor.verification_status === "approved" && <CheckCircle className="text-green-500" size={20} />}
                </div>
                {tutor.headline && <p className="text-gray-600 mt-1">{tutor.headline}</p>}
                <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                  {tutor.user?.city && <span className="flex items-center gap-1"><MapPin size={14} /> {tutor.user.city}</span>}
                  <span className="flex items-center gap-1"><Clock size={14} /> {tutor.years_experience} years exp</span>
                </div>
                <div className="flex items-center gap-2 mt-3">
                  <Star className="text-yellow-500 fill-yellow-500" size={20} />
                  <span className="font-semibold text-lg">{tutor.total_rating?.toFixed(1) || "0.0"}</span>
                  <span className="text-gray-500">({tutor.review_count} reviews)</span>
                  <span className="ml-4 text-2xl font-bold text-primary">₹{tutor.hourly_rate}/hr</span>
                </div>
                {tutor.is_featured && <div className="flex items-center gap-1 mt-2 text-yellow-600"><Award size={16} /> Featured Tutor</div>}
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            <Card>
              <CardContent className="p-6">
                <h2 className="text-xl font-semibold mb-4">About</h2>
                <p className="text-gray-600">{tutor.bio || "No bio available."}</p>
                <h3 className="text-lg font-semibold mt-6 mb-3">Subjects</h3>
                <div className="flex flex-wrap gap-2">
                  {tutor.subjects?.map((s) => (<span key={s} className="px-3 py-1 bg-primary/10 text-primary rounded-full">{s}</span>))}
                </div>
                <h3 className="text-lg font-semibold mt-6 mb-3">Grades</h3>
                <div className="flex flex-wrap gap-2">
                  {tutor.grades?.map((g) => (<span key={g} className="px-3 py-1 bg-gray-100 rounded-full">{g}</span>))}
                </div>
                <h3 className="text-lg font-semibold mt-6 mb-3">Teaching Mode</h3>
                <div className="flex gap-2">
                  {tutor.teaching_mode?.map((m) => (<span key={m} className="px-3 py-1 bg-green-100 text-green-700 rounded-full capitalize">{m}</span>))}
                </div>
                {tutor.qualification && (<><h3 className="text-lg font-semibold mt-6 mb-3">Qualification</h3><p className="text-gray-600">{tutor.qualification}</p></>)}
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <h2 className="text-xl font-semibold mb-4">Reviews ({reviews.length})</h2>
                {reviews.length === 0 ? (<p className="text-gray-500">No reviews yet.</p>) : (
                  <div className="space-y-4">
                    {reviews.map((r) => (
                      <div key={r.id} className="border-b pb-4">
                        <div className="flex items-center gap-2">
                          <Star className="text-yellow-500 fill-yellow-500" size={16} />
                          <span className="font-semibold">{r.rating}/5</span>
                          <span className="text-gray-400 text-sm">by {r.student_name || "Student"}</span>
                        </div>
                        {r.comment && <p className="mt-2 text-gray-600">{r.comment}</p>}
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          <div>
            <Card className="sticky top-4">
              <CardContent className="p-6">
                <h2 className="text-xl font-semibold mb-4">Book a Session</h2>
                <div className="space-y-4">
                  <Input placeholder="Subject to learn" value={bookingForm.subject} onChange={e => setBookingForm({...bookingForm, subject: e.target.value})} />
                  <Input type="date" value={bookingForm.date} onChange={e => setBookingForm({...bookingForm, date: e.target.value})} />
                  <Input type="time" value={bookingForm.time} onChange={e => setBookingForm({...bookingForm, time: e.target.value})} />
                  <Textarea placeholder="Notes (optional)" value={bookingForm.notes} onChange={e => setBookingForm({...bookingForm, notes: e.target.value})} />
                  <Button className="w-full" onClick={handleBooking} disabled={bookingLoading}>
                    {bookingLoading ? "Booking..." : "Request Booking"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}