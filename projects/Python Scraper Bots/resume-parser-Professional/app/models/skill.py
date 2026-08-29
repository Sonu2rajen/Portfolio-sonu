from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, nullable=False)

    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    candidate = relationship("Candidate", back_populates="skills")
