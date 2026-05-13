from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from ..core.database import get_db
from ..schemas import TutorProfileCreate, TutorProfileUpdate, TutorProfileResponse, SearchFilters, ReviewResponse
from ..services import TutorService, ai_matching_service
from ..models import User, TutorProfile
from .auth import get_current_user

router = APIRouter(prefix="/tutors", tags=["Tutors"])

@router.post("/profile", response_model=TutorProfileResponse)
async def create_profile(profile: TutorProfileCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "tutor":
        raise HTTPException(status_code=403, detail="Only tutors can create profiles")
    result = TutorService.create_tutor_profile(db, current_user.id, profile)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create profile")
    return result

@router.get("/profile", response_model=Optional[TutorProfileResponse])
async def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = TutorService.get_tutor_profile(db, current_user.id)
    return profile

@router.put("/profile", response_model=TutorProfileResponse)
async def update_profile(updates: TutorProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = TutorService.update_tutor_profile(db, current_user.id, updates.model_dump(exclude_unset=True))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/search")
async def search_tutors(
    query: Optional[str] = None,
    subjects: Optional[str] = Query(None),
    city: Optional[str] = None,
    min_rate: Optional[int] = None,
    max_rate: Optional[int] = None,
    mode: Optional[str] = Query(None),
    min_rating: Optional[float] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: Optional[float] = 10,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    subject_list = subjects.split(",") if subjects else None
    mode_list = mode.split(",") if mode else None

    results = ai_matching_service.match_tutors(
        db=db,
        query=query or "",
        subjects=subject_list,
        min_rate=min_rate,
        max_rate=max_rate,
        mode=mode_list,
        min_rating=min_rating,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km or 10,
        limit=limit
    )

    return {
        "total": len(results),
        "tutors": [
            {
                "id": str(r["tutor"].id),
                "user_id": str(r["tutor"].user_id),
                "headline": r["tutor"].headline,
                "bio": r["tutor"].bio,
                "subjects": r["tutor"].subjects,
                "grades": r["tutor"].grades,
                "teaching_mode": r["tutor"].teaching_mode,
                "hourly_rate": r["tutor"].hourly_rate,
                "years_experience": r["tutor"].years_experience,
                "qualification": r["tutor"].qualification,
                "verification_status": r["tutor"].verification_status,
                "total_rating": r["tutor"].total_rating,
                "review_count": r["tutor"].review_count,
                "is_featured": r["tutor"].is_featured,
                "score": r["score"],
                "match_factors": r["factors"],
                "user": {
                    "id": str(r["tutor"].user.id),
                    "full_name": r["tutor"].user.full_name,
                    "avatar_url": r["tutor"].user.avatar_url,
                    "city": r["tutor"].user.city
                }
            }
            for r in results
        ]
    }

@router.get("/{tutor_id}", response_model=TutorProfileResponse)
async def get_tutor(tutor_id: UUID, db: Session = Depends(get_db)):
    tutor = TutorService.get_tutor_by_id(db, tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return tutor

@router.get("/{tutor_id}/reviews", response_model=List[ReviewResponse])
async def get_tutor_reviews(tutor_id: UUID, db: Session = Depends(get_db)):
    from ..services import ReviewService
    reviews = ReviewService.get_tutor_reviews(db, tutor_id)
    return [
        {
            **ReviewResponse.model_validate(r).model_dump(),
            "student_name": r.student.full_name if r.student else None
        }
        for r in reviews
    ]