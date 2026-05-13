from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..schemas import BookingCreate, BookingUpdate, BookingResponse, ReviewCreate, ReviewResponse
from ..services import BookingService, ReviewService
from ..models import User, TutorProfile
from .auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = BookingService.create_booking(db, current_user.id, booking)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create booking")
    return result

@router.get("/my", response_model=List[BookingResponse])
async def get_my_bookings(
    status: Optional[str] = None,
    as_tutor: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if as_tutor:
        tutor_profile = db.query(TutorProfile).filter(TutorProfile.user_id == current_user.id).first()
        if not tutor_profile:
            raise HTTPException(status_code=404, detail="Tutor profile not found")
        bookings = BookingService.get_tutor_bookings(db, tutor_profile.id, status)
    else:
        bookings = BookingService.get_student_bookings(db, current_user.id, status)
    
    return [BookingResponse.model_validate(b) for b in bookings]

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from ..models import Booking
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    tutor_profile = db.query(TutorProfile).filter(TutorProfile.user_id == current_user.id).first()
    if booking.student_id != current_user.id and (not tutor_profile or booking.tutor_id != tutor_profile.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return booking

@router.put("/{booking_id}/status")
async def update_booking_status(
    booking_id: UUID,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from ..models import BookingStatus
    booking = BookingService.update_booking_status(db, booking_id, BookingStatus(status))
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Status updated", "status": status}

@router.post("/reviews", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = ReviewService.create_review(db, review, current_user.id)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create review")
    return result