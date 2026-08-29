from sqlalchemy.orm import Session
from app.models.candidate import Candidate

def get_all_candidates(db: Session):
    return db.query(Candidate).all()

def get_candidate_by_id(candidate_id: int, db: Session):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()
