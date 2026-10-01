import os
import shutil
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UploadedDocument, Problem
from app.services.auth import get_current_user
from app.services.document_parser import parse_uploaded_file
from app.config import settings

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_EXTENSIONS = {"pdf", "docx", "csv", "xlsx", "xls"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename = file.filename or "uploaded_sheet.pdf"
    ext = filename.lower().split(".")[-1]

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: .{ext}. Allowed formats: PDF, DOCX, CSV, XLSX."
        )

    # Read and validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 50 MB."
        )

    # Save to disk
    user_upload_dir = os.path.join(settings.UPLOAD_DIR, f"user_{current_user.id}")
    os.makedirs(user_upload_dir, exist_ok=True)
    saved_path = os.path.join(user_upload_dir, filename)

    with open(saved_path, "wb") as f:
        f.write(content)

    # Load problem bank lookup
    problems = db.query(Problem).all()
    problem_lookup = {str(p.number): {
        "number": p.number,
        "title": p.title,
        "difficulty": p.difficulty,
        "topic": p.topic,
        "pattern": p.pattern,
        "similar_to": p.similar_to,
        "url": p.url
    } for p in problems}

    # Parse problems
    extracted_problems = parse_uploaded_file(saved_path, filename, problem_lookup)

    # Save to DB
    doc = UploadedDocument(
        user_id=current_user.id,
        filename=filename,
        file_path=saved_path,
        file_type=ext,
        parsed_problems=extracted_problems
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "id": doc.id,
        "filename": doc.filename,
        "file_type": doc.file_type,
        "problem_count": len(extracted_problems),
        "problems": extracted_problems,
        "message": f"Successfully extracted {len(extracted_problems)} problems from {filename}."
    }

@router.get("/")
def get_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    docs = db.query(UploadedDocument).filter(UploadedDocument.user_id == current_user.id).order_by(UploadedDocument.created_at.desc()).all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "problem_count": len(d.parsed_problems) if d.parsed_problems else 0,
            "created_at": d.created_at
        }
        for d in docs
    ]

@router.get("/{document_id}")
def get_document_details(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(UploadedDocument).filter(
        UploadedDocument.id == document_id,
        UploadedDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    return {
        "id": doc.id,
        "filename": doc.filename,
        "file_type": doc.file_type,
        "problem_count": len(doc.parsed_problems) if doc.parsed_problems else 0,
        "problems": doc.parsed_problems or [],
        "created_at": doc.created_at
    }
