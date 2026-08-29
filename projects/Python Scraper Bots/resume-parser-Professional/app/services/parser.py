from app.utils.regex_patterns import EMAIL_REGEX, PHONE_REGEX
from app.utils.skill_list import SKILLS


def clean_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def extract_email(text: str):
    match = EMAIL_REGEX.search(text)
    return match.group() if match else None


def extract_phone(text: str):
    match = PHONE_REGEX.search(text)
    return match.group() if match else None


def extract_name(text: str):
    for line in text.splitlines():
        if "@" in line:
            possible_name = line.split("|")[0].strip()
            if len(possible_name.split()) <= 4:
                return possible_name
    return "Unknown"



def extract_skills(text: str):
    skills = set()

    # existing keyword-based extraction (keep this)
    known_skills = [
        "python", "java", "c++", "sql", "excel", "power bi",
        "aws", "azure", "machine learning", "nlp"
    ]

    text_lower = text.lower()
    for skill in known_skills:
        if skill in text_lower:
            skills.add(skill.title())

    
    for line in text.splitlines():
        if line.strip().lower().startswith("skills"):
            if ":" in line:
                raw_skills = line.split(":", 1)[1]
                for s in raw_skills.split(","):
                    skills.add(s.strip())

    return list(skills)



def extract_education(text: str):
    education = []
    keywords = ["bachelor", "master", "b.tech", "m.tech", "b.sc", "m.sc", "mba"]

    for line in text.split("\n"):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                education.append({
                    "degree": line.strip(),
                    "institution": None,
                    "year": None
                })
                break

    return education


def extract_experience(text: str):
    experience = []
    lines = text.split("\n")

    for line in lines:
        if any(word in line.lower() for word in ["company", "engineer", "developer", "analyst"]):
            experience.append({
                "company": None,
                "role": line.strip(),
                "start_date": None,
                "end_date": None,
                "description": None
            })

    return experience


def parse_resume(text: str) -> dict:
    text = clean_text(text)

    return {
        "full_name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
