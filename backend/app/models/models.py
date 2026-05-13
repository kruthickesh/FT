from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, Enum, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..core.database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    TUTOR = "tutor"
    ADMIN = "admin"

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    city = Column(String(100), nullable=True)
    country = Column(String(100), default="India")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    tutor_profile = relationship("TutorProfile", back_populates="user", uselist=False)
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    messages_sent = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")

class TutorProfile(Base):
    __tablename__ = "tutor_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    headline = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    subjects = Column(ARRAY(String), default=[])
    grades = Column(ARRAY(String), default=[])
    teaching_mode = Column(ARRAY(String), default=["online", "offline"])
    hourly_rate = Column(Integer, default=500)
    currency = Column(String(10), default="INR")
    years_experience = Column(Integer, default=0)
    qualification = Column(String(255), nullable=True)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    verification_documents = Column(JSON, default=[])
    embedding = Column(JSON, nullable=True)
    total_sessions = Column(Integer, default=0)
    total_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    availability = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="tutor_profile")
    bookings = relationship("Booking", back_populates="tutor")
    reviews = relationship("Review", back_populates="tutor")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    preferred_subjects = Column(ARRAY(String), default=[])
    preferred_grades = Column(ARRAY(String), default=[])
    preferred_budget_min = Column(Integer, default=0)
    preferred_budget_max = Column(Integer, default=5000)
    preferred_mode = Column(ARRAY(String), default=["online", "offline"])
    learning_goals = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="student_profile")
    bookings = relationship("Booking", back_populates="student")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutor_profiles.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    notes = Column(Text, nullable=True)
    amount = Column(Integer, nullable=False)
    payment_status = Column(String(50), default="pending")
    razorpay_order_id = Column(String(255), nullable=True)
    razorpay_payment_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    student = relationship("StudentProfile", back_populates="bookings")
    tutor = relationship("TutorProfile", back_populates="bookings")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutor_profiles.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    tutor = relationship("TutorProfile", back_populates="reviews")
    booking = relationship("Booking")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())