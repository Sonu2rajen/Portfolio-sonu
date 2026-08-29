from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    role = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(String)

    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    candidate = relationship("Candidate", back_populates="experiences")
