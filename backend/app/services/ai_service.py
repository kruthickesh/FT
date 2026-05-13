from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
import numpy as np
from typing import List, Optional
from ..models import TutorProfile, User

class AIMatchingService:
    def __init__(self):
        self.model = None
        self.embedding_cache = {}

    def get_embedding_model(self):
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model

    def generate_embedding(self, text: str) -> List[float]:
        model = self.get_embedding_model()
        embedding = model.encode(text)
        return embedding.tolist()

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def create_tutor_text(self, tutor: TutorProfile) -> str:
        parts = [
            tutor.headline or "",
            tutor.bio or "",
            tutor.qualification or "",
            " ".join(tutor.subjects) if tutor.subjects else "",
            " ".join(tutor.grades) if tutor.grades else "",
            f"{tutor.years_experience} years experience"
        ]
        return " | ".join([p for p in parts if p])

    def compute_tutor_embeddings(self, db: Session):
        tutors = db.query(TutorProfile).all()
        for tutor in tutors:
            if not tutor.embedding:
                text = self.create_tutor_text(tutor)
                if text:
                    tutor.embedding = self.generate_embedding(text)
        db.commit()

    def match_tutors(
        self,
        db: Session,
        query: str,
        subjects: Optional[List[str]] = None,
        min_rate: Optional[int] = None,
        max_rate: Optional[int] = None,
        mode: Optional[List[str]] = None,
        min_rating: Optional[float] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius_km: float = 10,
        limit: int = 20
    ) -> List[dict]:
        tutors = db.query(TutorProfile).join(User).filter(
            User.is_active == True,
            TutorProfile.verification_status == "approved"
        ).all()

        query_embedding = self.generate_embedding(query) if query else None
        results = []

        for tutor in tutors:
            score = 0
            factors = []

            if query_embedding and tutor.embedding:
                semantic_score = self.cosine_similarity(query_embedding, tutor.embedding)
                score += semantic_score * 30
                factors.append(f"semantic: {semantic_score:.2f}")

            if subjects:
                tutor_subjects = set(t.lower() for t in tutor.subjects)
                subject_match = len(set(s.lower() for s in subjects) & tutor_subjects)
                if subject_match > 0:
                    score += (subject_match / len(subjects)) * 25
                    factors.append(f"subjects: {subject_match}/{len(subjects)}")

            if min_rate and tutor.hourly_rate >= min_rate:
                score += 10
            if max_rate and tutor.hourly_rate <= max_rate:
                score += 10

            if mode:
                mode_match = any(m in tutor.teaching_mode for m in mode)
                if mode_match:
                    score += 15
                    factors.append("mode match")

            if min_rating and tutor.total_rating >= min_rating:
                score += 15
                factors.append(f"rating: {tutor.total_rating}")

            if latitude and longitude and tutor.user.latitude and tutor.user.longitude:
                distance = self.haversine_distance(
                    latitude, longitude,
                    tutor.user.latitude, tutor.user.longitude
                )
                if distance <= radius_km:
                    score += (1 - distance / radius_km) * 20
                    factors.append(f"distance: {distance:.1f}km")

            if tutor.is_featured:
                score += 10

            results.append({
                "tutor": tutor,
                "score": score,
                "factors": factors
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        return R * c

    def get_similar_tutors(self, db: Session, tutor_id: UUID, limit: int = 5) -> List[TutorProfile]:
        tutor = db.query(TutorProfile).filter(TutorProfile.id == tutor_id).first()
        if not tutor or not tutor.embedding:
            return []

        tutors = db.query(TutorProfile).filter(
            TutorProfile.id != tutor_id,
            TutorProfile.verification_status == "approved"
        ).all()

        similarities = []
        for t in tutors:
            if t.embedding:
                sim = self.cosine_similarity(tutor.embedding, t.embedding)
                similarities.append((t, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return [t[0] for t in similarities[:limit]]

ai_matching_service = AIMatchingService()