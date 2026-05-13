from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    TUTOR = "tutor"
    ADMIN = "admin"

class VerificationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    city: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserResponse(UserBase):
    id: UUID
    role: UserRole
    avatar_url: Optional[str]
    is_active: bool
    is_verified: bool
    city: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TutorProfileBase(BaseModel):
    headline: Optional[str] = None
    bio: Optional[str] = None
    subjects: List[str] = []
    grades: List[str] = []
    teaching_mode: List[str] = ["online", "offline"]
    hourly_rate: int = 500
    years_experience: int = 0
    qualification: Optional[str] = None

class TutorProfileCreate(TutorProfileBase):
    pass

class TutorProfileUpdate(BaseModel):
    headline: Optional[str] = None
    bio: Optional[str] = None
    subjects: Optional[List[str]] = None
    grades: Optional[List[str]] = None
    teaching_mode: Optional[List[str]] = None
    hourly_rate: Optional[int] = None
    years_experience: Optional[int] = None
    qualification: Optional[str] = None
    availability: Optional[dict] = None

class TutorProfileResponse(TutorProfileBase):
    id: UUID
    user_id: UUID
    verification_status: VerificationStatus
    total_sessions: int
    total_rating: float
    review_count: int
    is_featured: bool
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True

class StudentProfileBase(BaseModel):
    preferred_subjects: List[str] = []
    preferred_grades: List[str] = []
    preferred_budget_min: int = 0
    preferred_budget_max: int = 5000
    preferred_mode: List[str] = ["online", "offline"]
    learning_goals: Optional[str] = None

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileUpdate(BaseModel):
    preferred_subjects: Optional[List[str]] = None
    preferred_grades: Optional[List[str]] = None
    preferred_budget_min: Optional[int] = None
    preferred_budget_max: Optional[int] = None
    preferred_mode: Optional[List[str]] = None
    learning_goals: Optional[str] = None

class StudentProfileResponse(StudentProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    subject: str
    scheduled_at: datetime
    duration_minutes: int = 60
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    tutor_id: UUID

class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    notes: Optional[str] = None

class BookingResponse(BookingBase):
    id: UUID
    student_id: UUID
    tutor_id: UUID
    status: BookingStatus
    amount: int
    payment_status: str
    created_at: datetime
    tutor: Optional[TutorProfileResponse] = None

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    booking_id: UUID

class ReviewResponse(ReviewBase):
    id: UUID
    booking_id: UUID
    student_id: UUID
    created_at: datetime
    student_name: Optional[str] = None

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    receiver_id: UUID

class MessageResponse(MessageBase):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: UUID
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SubjectResponse(BaseModel):
    id: UUID
    name: str
    category: str
    description: Optional[str]

    class Config:
        from_attributes = True

class SearchFilters(BaseModel):
    query: Optional[str] = None
    subjects: Optional[List[str]] = None
    city: Optional[str] = None
    min_rate: Optional[int] = None
    max_rate: Optional[int] = None
    mode: Optional[List[str]] = None
    min_rating: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = 10
    limit: int = 20
    offset: int = 0