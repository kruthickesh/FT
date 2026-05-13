-- Find My Tutor Database Setup
-- Run this in Supabase SQL Editor

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'student',
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Tutor profiles
CREATE TABLE IF NOT EXISTS tutor_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id),
    headline VARCHAR(255),
    bio TEXT,
    subjects TEXT[] DEFAULT '{}',
    grades TEXT[] DEFAULT '{}',
    teaching_mode TEXT[] DEFAULT '{"online", "offline"}',
    hourly_rate INTEGER DEFAULT 500,
    currency VARCHAR(10) DEFAULT 'INR',
    years_experience INTEGER DEFAULT 0,
    qualification VARCHAR(255),
    verification_status VARCHAR(20) DEFAULT 'pending',
    verification_documents JSONB DEFAULT '[]',
    embedding JSONB,
    total_sessions INTEGER DEFAULT 0,
    total_rating FLOAT DEFAULT 0.0,
    review_count INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT false,
    availability JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tutor_verification ON tutor_profiles(verification_status);
CREATE INDEX idx_tutor_subjects ON tutor_profiles USING GIN(subjects);
CREATE INDEX idx_tutor_rate ON tutor_profiles(hourly_rate);

-- Student profiles
CREATE TABLE IF NOT EXISTS student_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id),
    preferred_subjects TEXT[] DEFAULT '{}',
    preferred_grades TEXT[] DEFAULT '{}',
    preferred_budget_min INTEGER DEFAULT 0,
    preferred_budget_max INTEGER DEFAULT 5000,
    preferred_mode TEXT[] DEFAULT '{"online", "offline"}',
    learning_goals TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bookings
CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES users(id),
    tutor_id UUID NOT NULL REFERENCES tutor_profiles(id),
    subject VARCHAR(255) NOT NULL,
    scheduled_at TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    status VARCHAR(20) DEFAULT 'pending',
    notes TEXT,
    amount INTEGER NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending',
    razorpay_order_id VARCHAR(255),
    razorpay_payment_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_bookings_student ON bookings(student_id);
CREATE INDEX idx_bookings_tutor ON bookings(tutor_id);
CREATE INDEX idx_bookings_status ON bookings(status);

-- Reviews
CREATE TABLE IF NOT EXISTS reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id),
    tutor_id UUID NOT NULL REFERENCES tutor_profiles(id),
    student_id UUID NOT NULL REFERENCES users(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    is_approved BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reviews_tutor ON reviews(tutor_id);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID NOT NULL REFERENCES users(id),
    receiver_id UUID NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(sender_id, receiver_id);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50),
    is_read BOOLEAN DEFAULT false,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);

-- Subjects
CREATE TABLE IF NOT EXISTS subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default subjects
INSERT INTO subjects (name, category) VALUES
('Mathematics', 'Science'),
('Physics', 'Science'),
('Chemistry', 'Science'),
('Biology', 'Science'),
('English', 'Languages'),
('Hindi', 'Languages'),
('Computer Science', 'Technology'),
('Programming', 'Technology'),
('History', 'Humanities'),
('Geography', 'Humanities')
ON CONFLICT (name) DO NOTHING;

-- Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE tutor_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Public read for verified tutors
CREATE POLICY "Public read verified tutors" ON tutor_profiles
    FOR SELECT USING (verification_status = 'approved');

-- Users can read their own data
CREATE POLICY "Users read own" ON users
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own data
CREATE POLICY "Users update own" ON users
    FOR UPDATE USING (auth.uid() = id);