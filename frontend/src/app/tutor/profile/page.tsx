"use client";
import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export default function TutorProfileEditPage() {
  const { user, loading } = useAuth();
  const [profile, setProfile] = useState({ headline: "", bio: "", subjects: "", grades: "", hourly_rate: 500, years_experience: 0, qualification: "" });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user?.role === "tutor") loadProfile();
  }, [user]);

  const loadProfile = async () => {
    try {
      const data = await apiRequest("/tutors/profile");
      if (data) {
        setProfile({
          headline: data.headline || "",
          bio: data.bio || "",
          subjects: (data.subjects || []).join(", "),
          grades: (data.grades || []).join(", "),
          hourly_rate: data.hourly_rate || 500,
          years_experience: data.years_experience || 0,
          qualification: data.qualification || ""
        });
      }
    } catch {}
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const payload = {
        headline: profile.headline,
        bio: profile.bio,
        subjects: profile.subjects.split(",").map(s => s.trim()).filter(Boolean),
        grades: profile.grades.split(",").map(s => s.trim()).filter(Boolean),
        hourly_rate: profile.hourly_rate,
        years_experience: profile.years_experience,
        qualification: profile.qualification
      };
      await apiRequest("/tutors/profile", { method: "PUT", body: JSON.stringify(payload) });
      alert("Profile updated!");
    } catch (err: any) { alert(err.message); }
    finally { setSaving(false); }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-6">Edit Tutor Profile</h1>
        <Card>
          <CardContent className="p-6 space-y-4">
            <div><label className="block text-sm font-medium mb-1">Headline</label><Input value={profile.headline} onChange={e => setProfile({...profile, headline: e.target.value})} placeholder="e.g., Expert Math Tutor with 5 years experience" /></div>
            <div><label className="block text-sm font-medium mb-1">Bio</label><Textarea value={profile.bio} onChange={e => setProfile({...profile, bio: e.target.value})} placeholder="Tell students about yourself..." rows={4} /></div>
            <div><label className="block text-sm font-medium mb-1">Subjects (comma-separated)</label><Input value={profile.subjects} onChange={e => setProfile({...profile, subjects: e.target.value})} placeholder="Mathematics, Physics, Chemistry" /></div>
            <div><label className="block text-sm font-medium mb-1">Grades (comma-separated)</label><Input value={profile.grades} onChange={e => setProfile({...profile, grades: e.target.value})} placeholder="Class 6-12, JEE, NEET" /></div>
            <div className="grid grid-cols-2 gap-4">
              <div><label className="block text-sm font-medium mb-1">Hourly Rate (₹)</label><Input type="number" value={profile.hourly_rate} onChange={e => setProfile({...profile, hourly_rate: parseInt(e.target.value)})} /></div>
              <div><label className="block text-sm font-medium mb-1">Years of Experience</label><Input type="number" value={profile.years_experience} onChange={e => setProfile({...profile, years_experience: parseInt(e.target.value)})} /></div>
            </div>
            <div><label className="block text-sm font-medium mb-1">Qualification</label><Input value={profile.qualification} onChange={e => setProfile({...profile, qualification: e.target.value})} placeholder="e.g., M.Sc. Mathematics, IIT Delhi" /></div>
            <Button onClick={handleSave} disabled={saving}>{saving ? "Saving..." : "Save Profile"}</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}