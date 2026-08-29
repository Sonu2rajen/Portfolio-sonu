from sqlalchemy.orm import declarative_base

Base = declarative_base()

# IMPORTANT: import all models so SQLAlchemy registers them
from app.models.candidate import Candidate
from app.models.skill import Skill
from app.models.education import Education
from app.models.experience import Experience
