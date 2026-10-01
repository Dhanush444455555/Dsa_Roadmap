from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CheatSheet
from app.schemas import CheatSheetOut
from app.ai.vector_store import vector_store

router = APIRouter(prefix="/cheatsheets", tags=["cheatsheets"])

@router.get("/")
def list_cheatsheets(
    q: Optional[str] = Query(None, description="Search query across topic, keywords, or formulas"),
    db: Session = Depends(get_db)
):
    sheets = db.query(CheatSheet).all()
    results = []
    
    for cs in sheets:
        content = cs.content or {}
        topic = cs.topic
        when_to_use = content.get("when_to_use", [])
        core_idea = content.get("core_idea", "")
        formulas = content.get("formulas_and_identities", [])

        # Filter if search query provided
        if q:
            q_lower = q.lower()
            haystack = f"{topic} {' '.join(when_to_use)} {core_idea} {' '.join(formulas)}".lower()
            if q_lower not in haystack:
                continue

        results.append({
            "id": cs.id,
            "topic": cs.topic,
            "when_to_use": when_to_use,
            "core_idea": core_idea,
            "formulas_count": len(formulas),
            "common_mistakes_count": len(content.get("common_mistakes", [])),
            "quick_revision_points": content.get("quick_revision", [])[:3]
        })

    return results

@router.get("/{topic}")
def get_cheatsheet_by_topic(topic: str, db: Session = Depends(get_db)):
    # Normalize topic search
    clean_topic = topic.replace("-", " ").replace("_", " ").lower()
    
    all_sheets = db.query(CheatSheet).all()
    matched = None
    for cs in all_sheets:
        if cs.topic.lower() == clean_topic or clean_topic in cs.topic.lower():
            matched = cs
            break

    if not matched:
        # Fallback to vector_store memory
        cs_mem = vector_store.get_cheat_sheet(topic)
        if cs_mem:
            return {"topic": topic, "content": cs_mem}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cheat sheet for topic '{topic}' not found."
        )

    return {
        "id": matched.id,
        "topic": matched.topic,
        "content": matched.content,
        "created_at": matched.created_at,
        "updated_at": matched.updated_at
    }
