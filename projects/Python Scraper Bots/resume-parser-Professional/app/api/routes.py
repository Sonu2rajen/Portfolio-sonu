import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.templates import templates
from app.core.database import get_db
from app.services.file_handler import extract_text
from app.services.parser import parse_resume
from app.services.storage import save_candidate
from app.services.query import get_all_candidates, get_candidate_by_id

router = APIRouter()


@router.post("/upload-resume")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    parsed_data = parse_resume(text)
    candidate = save_candidate(parsed_data, db)

    return {
        "message": "Resume processed successfully",
        "candidate_id": candidate.id
    }


@router.get("/candidates")
def list_candidates(request: Request, db: Session = Depends(get_db)):
    candidates = get_all_candidates(db)
    return templates.TemplateResponse(
        "candidates.html",
        {"request": request, "candidates": candidates}
    )


@router.get("/candidates/{candidate_id}")
def candidate_detail(candidate_id: int, request: Request, db: Session = Depends(get_db)):
    candidate = get_candidate_by_id(candidate_id, db)
    return templates.TemplateResponse(
        "candidate_detail.html",
        {"request": request, "candidate": candidate}
    )

@router.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )

@router.post("/upload")
def upload_resume_form(
    request: Request,
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join("uploads", resume.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    from app.services.file_handler import extract_text
    from app.services.parser import parse_resume
    from app.services.storage import save_candidate

    text = extract_text(file_path)
    parsed_data = parse_resume(text)
    save_candidate(parsed_data, db)

    return RedirectResponse(url="/candidates", status_code=303)

@router.get("/candidates/delete/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = get_candidate_by_id(candidate_id, db)

    if not candidate:
        return {"error": "Candidate not found"}

    db.delete(candidate)
    db.commit()

    return RedirectResponse(url="/candidates", status_code=303)