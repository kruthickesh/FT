from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..core.database import get_db
from ..schemas import StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse
from ..services import StudentService
from ..models import User
from .auth import get_current_user

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/profile", response_model=StudentProfileResponse)
async def create_profile(profile: StudentProfileCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = StudentService.create_student_profile(db, current_user.id, profile)
    return result

@router.get("/profile", response_model=StudentProfileResponse)
async def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = StudentService.get_student_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/profile", response_model=StudentProfileResponse)
async def update_profile(updates: StudentProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = StudentService.update_student_profile(db, current_user.id, updates.model_dump(exclude_unset=True))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile