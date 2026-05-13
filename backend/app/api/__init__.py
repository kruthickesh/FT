from fastapi import APIRouter
from .auth import router as auth_router
from .tutors import router as tutors_router
from .students import router as students_router
from .bookings import router as bookings_router
from .messages import router as messages_router
from .admin import router as admin_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(tutors_router)
api_router.include_router(students_router)
api_router.include_router(bookings_router)
api_router.include_router(messages_router)
api_router.include_router(admin_router)