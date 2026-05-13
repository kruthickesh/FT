from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..core.database import get_db
from ..models import User, TutorProfile, Booking, Review
from .auth import get_current_user, get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 50,
    role: str = None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.offset(skip).limit(limit).all()
    return {"total": query.count(), "users": users}

@router.get("/tutors/pending")
async def get_pending_tutors(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    tutors = db.query(TutorProfile).filter(TutorProfile.verification_status == "pending").all()
    return tutors

@router.put("/tutors/{tutor_id}/verify")
async def verify_tutor(tutor_id: UUID, status: str, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    from ..services import TutorService
    result = TutorService.verify_tutor(db, tutor_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return {"message": f"Tutor {status}", "tutor_id": str(tutor_id)}

@router.get("/reviews/pending")
async def get_pending_reviews(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.is_approved == False).all()
    return reviews

@router.put("/reviews/{review_id}/moderate")
async def moderate_review(review_id: UUID, approved: bool, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.is_approved = approved
    db.commit()
    return {"message": "Review moderated", "approved": approved}

@router.get("/stats")
async def get_stats(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_tutors = db.query(TutorProfile).count()
    total_bookings = db.query(Booking).count()
    total_reviews = db.query(Review).count()

    return {
        "total_users": total_users,
        "total_tutors": total_tutors,
        "total_bookings": total_bookings,
        "total_reviews": total_reviews
    }