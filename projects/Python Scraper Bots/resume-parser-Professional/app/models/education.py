from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    degree = Column(String)
    institution = Column(String)
    year = Column(String)

    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    candidate = relationship("Candidate", back_populates="educations")
