from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from ..models import Booking, Review, TutorProfile, BookingStatus
from ..schemas import BookingCreate, ReviewCreate

class BookingService:
    @staticmethod
    def create_booking(db: Session, student_id: UUID, booking: BookingCreate) -> Booking:
        tutor = db.query(TutorProfile).filter(TutorProfile.id == booking.tutor_id).first()
        if not tutor:
            return None

        amount = (booking.duration_minutes / 60) * tutor.hourly_rate

        db_booking = Booking(
            student_id=student_id,
            tutor_id=booking.tutor_id,
            subject=booking.subject,
            scheduled_at=booking.scheduled_at,
            duration_minutes=booking.duration_minutes,
            notes=booking.notes,
            amount=int(amount)
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking

    @staticmethod
    def get_student_bookings(db: Session, student_id: UUID, status: str = None) -> list:
        query = db.query(Booking).filter(Booking.student_id == student_id)
        if status:
            query = query.filter(Booking.status == status)
        return query.order_by(Booking.scheduled_at.desc()).all()

    @staticmethod
    def get_tutor_bookings(db: Session, tutor_id: UUID, status: str = None) -> list:
        query = db.query(Booking).filter(Booking.tutor_id == tutor_id)
        if status:
            query = query.filter(Booking.status == status)
        return query.order_by(Booking.scheduled_at.desc()).all()

    @staticmethod
    def update_booking_status(db: Session, booking_id: UUID, status: BookingStatus) -> Booking:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            booking.status = status
            if status == BookingStatus.COMPLETED:
                tutor = db.query(TutorProfile).filter(TutorProfile.id == booking.tutor_id).first()
                if tutor:
                    tutor.total_sessions += 1
            db.commit()
            db.refresh(booking)
        return booking

    @staticmethod
    def cancel_booking(db: Session, booking_id: UUID) -> Booking:
        return BookingService.update_booking_status(db, booking_id, BookingStatus.CANCELLED)

class ReviewService:
    @staticmethod
    def create_review(db: Session, review: ReviewCreate, student_id: UUID) -> Review:
        booking = db.query(Booking).filter(Booking.id == review.booking_id).first()
        if not booking or booking.student_id != student_id:
            return None
        if booking.status != BookingStatus.COMPLETED:
            return None

        existing = db.query(Review).filter(
            Review.booking_id == review.booking_id,
            Review.student_id == student_id
        ).first()
        if existing:
            return existing

        db_review = Review(
            booking_id=review.booking_id,
            tutor_id=booking.tutor_id,
            student_id=student_id,
            rating=review.rating,
            comment=review.comment
        )
        db.add(db_review)

        tutor = db.query(TutorProfile).filter(TutorProfile.id == booking.tutor_id).first()
        if tutor:
            new_count = tutor.review_count + 1
            tutor.total_rating = ((tutor.total_rating * tutor.review_count) + review.rating) / new_count
            tutor.review_count = new_count

        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def get_tutor_reviews(db: Session, tutor_id: UUID) -> list:
        return db.query(Review).filter(
            Review.tutor_id == tutor_id,
            Review.is_approved == True
        ).order_by(Review.created_at.desc()).all()