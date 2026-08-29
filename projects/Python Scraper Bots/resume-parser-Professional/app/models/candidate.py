from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    location = Column(String)

    skills = relationship("Skill", back_populates="candidate", cascade="all, delete")
    educations = relationship("Education", back_populates="candidate", cascade="all, delete")
    experiences = relationship("Experience", back_populates="candidate", cascade="all, delete")
