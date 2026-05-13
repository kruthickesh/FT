import type { Metadata } from "next";
import { AuthProvider } from "@/lib/auth";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "Find My Tutor - AI-Powered Tutoring Marketplace",
  description: "Connect with verified tutors near you using intelligent AI matching",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}