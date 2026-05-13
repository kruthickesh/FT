"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { TutorProfile } from "@/types";
import { Star, MapPin, CheckCircle } from "lucide-react";

export default function StudentSearchPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [tutors, setTutors] = useState<TutorProfile[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    if (!loading && !user) router.push("/auth");
  }, [user, loading, router]);

  useEffect(() => {
    handleSearch();
  }, []);

  const handleSearch = async () => {
    try {
      const params = new URLSearchParams();
      if (search) params.append("query", search);
      const data = await apiRequest(`/tutors/search?${params.toString()}`);
      setTutors(data.tutors || []);
    } catch {}
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6">Find Your Tutor</h1>
        <div className="flex gap-4 mb-8">
          <Input placeholder="Search by subject, name..." value={search} onChange={e => setSearch(e.target.value)} className="max-w-md" />
          <Button onClick={handleSearch}>Search</Button>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tutors.map((tutor) => (
            <Link key={tutor.id} href={`/tutors/${tutor.id}`}>
              <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                <CardContent className="p-6">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-2xl">
                      {tutor.user?.avatar_url ? <img src={tutor.user.avatar_url} className="w-full h-full rounded-full object-cover" /> : "👨‍🏫"}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold">{tutor.user?.full_name}</h3>
                        {tutor.verification_status === "approved" && <CheckCircle className="text-green-500" size={16} />}
                      </div>
                      {tutor.user?.city && <p className="text-sm text-gray-500 flex items-center gap-1"><MapPin size={14} /> {tutor.user.city}</p>}
                    </div>
                  </div>
                  {tutor.headline && <p className="text-sm text-gray-600 mb-3 line-clamp-2">{tutor.headline}</p>}
                  <div className="flex flex-wrap gap-1 mb-4">
                    {tutor.subjects?.slice(0, 3).map((s) => (<span key={s} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">{s}</span>))}
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1"><Star className="text-yellow-500 fill-yellow-500" size={16} /><span>{tutor.total_rating?.toFixed(1) || "0.0"}</span></div>
                    <span className="font-bold text-primary">₹{tutor.hourly_rate}/hr</span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
        {tutors.length === 0 && <p className="text-center text-gray-500 py-12">No tutors found. Try different search terms.</p>}
      </div>
    </div>
  );
}