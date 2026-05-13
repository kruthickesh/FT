from sqlalchemy.orm import Session
from uuid import UUID
from ..models import User, TutorProfile, StudentProfile, UserRole
from ..schemas import UserCreate, UserUpdate, TutorProfileCreate, StudentProfileCreate
from ..core.security import get_password_hash, verify_password

class AuthService:
    @staticmethod
    def create_user(db: Session, user: UserCreate, role: UserRole = UserRole.STUDENT) -> User:
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password),
            full_name=user.full_name,
            phone=user.phone,
            role=role,
            city=user.city
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def update_user(db: Session, user_id: UUID, updates: UserUpdate) -> User:
        user = AuthService.get_user_by_id(db, user_id)
        if not user:
            return None
        update_data = updates.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

class TutorService:
    @staticmethod
    def create_tutor_profile(db: Session, user_id: UUID, profile: TutorProfileCreate) -> TutorProfile:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.role != UserRole.TUTOR:
            return None
        existing = db.query(TutorProfile).filter(TutorProfile.user_id == user_id).first()
        if existing:
            return existing
        db_profile = TutorProfile(user_id=user_id, **profile.model_dump())
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    def get_tutor_profile(db: Session, user_id: UUID) -> TutorProfile:
        return db.query(TutorProfile).filter(TutorProfile.user_id == user_id).first()

    @staticmethod
    def get_tutor_by_id(db: Session, tutor_id: UUID) -> TutorProfile:
        return db.query(TutorProfile).filter(TutorProfile.id == tutor_id).first()

    @staticmethod
    def update_tutor_profile(db: Session, user_id: UUID, updates: dict) -> TutorProfile:
        profile = TutorService.get_tutor_profile(db, user_id)
        if not profile:
            return None
        for field, value in updates.items():
            if value is not None:
                setattr(profile, field, value)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def verify_tutor(db: Session, tutor_id: UUID, status: str) -> TutorProfile:
        profile = TutorService.get_tutor_by_id(db, tutor_id)
        if profile:
            profile.verification_status = status
            profile.user.is_verified = status == "approved"
            db.commit()
            db.refresh(profile)
        return profile

class StudentService:
    @staticmethod
    def create_student_profile(db: Session, user_id: UUID, profile: StudentProfileCreate) -> StudentProfile:
        existing = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
        if existing:
            return existing
        db_profile = StudentProfile(user_id=user_id, **profile.model_dump())
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    def get_student_profile(db: Session, user_id: UUID) -> StudentProfile:
        return db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()

    @staticmethod
    def update_student_profile(db: Session, user_id: UUID, updates: dict) -> StudentProfile:
        profile = StudentService.get_student_profile(db, user_id)
        if not profile:
            return None
        for field, value in updates.items():
            if value is not None:
                setattr(profile, field, value)
        db.commit()
        db.refresh(profile)
        return profile