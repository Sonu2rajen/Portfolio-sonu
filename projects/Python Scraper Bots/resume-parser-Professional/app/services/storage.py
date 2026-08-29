from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.models.skill import Skill
from app.models.education import Education
from app.models.experience import Experience


def save_candidate(parsed_data: dict, db: Session) -> Candidate:
    email = parsed_data.get("email")

    # 🔴 CHECK IF CANDIDATE ALREADY EXISTS
    existing_candidate = db.query(Candidate).filter(Candidate.email == email).first()
    if existing_candidate:
        return existing_candidate

    candidate = Candidate(
        full_name=parsed_data.get("full_name") or "Unknown",
        email=email,
        phone=parsed_data.get("phone"),
        location=None
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # Skills
    for skill in parsed_data.get("skills", []):
        db.add(Skill(skill_name=skill, candidate_id=candidate.id))

    # Education
    for edu in parsed_data.get("education", []):
        db.add(Education(
            degree=edu.get("degree"),
            institution=edu.get("institution"),
            year=edu.get("year"),
            candidate_id=candidate.id
        ))

    # Experience
    for exp in parsed_data.get("experience", []):
        db.add(Experience(
            company=exp.get("company"),
            role=exp.get("role"),
            start_date=exp.get("start_date"),
            end_date=exp.get("end_date"),
            description=exp.get("description"),
            candidate_id=candidate.id
        ))

    db.commit()
    return candidate
