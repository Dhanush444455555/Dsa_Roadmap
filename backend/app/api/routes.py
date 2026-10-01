import os
import json
from datetime import datetime, date, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database.session import get_db
from ..database.models import Problem, Roadmap, RoadmapItem, RevisionItem, UserSettings, DriveResource
from ..schemas.dsa_schemas import (
    ProblemResponse,
    ParsedDocumentResponse,
    ParsedProblemItem,
    RoadmapConfigRequest,
    RoadmapResponse,
    RoadmapItemStatusUpdate,
    ProgressResponse,
    TopicProgress,
    RecommendationResponse,
    RevisionItemResponse
)
from ..services.document_parser import DocumentParser
from ..services.problem_extractor import ProblemExtractor
from ..services.problem_classifier import ProblemClassifier
from ..services.similarity_engine import SimilarityEngine
from ..services.roadmap_generator import RoadmapGenerator
from ..services.recommendation_engine import RecommendationEngine
from ..services.revision_engine import RevisionEngine

router = APIRouter(prefix="/api")

# Lazy-loaded singletons
_extractor = None
_classifier = None

def get_services():
    global _extractor, _classifier
    if _classifier is None:
        _classifier = ProblemClassifier()
    if _extractor is None:
        _extractor = ProblemExtractor(_classifier.known_problems)
    return _extractor, _classifier

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "DSA Roadmap AI Backend"}

@router.get("/built-in-problems", response_model=List[Dict[str, Any]])
def get_built_in_problems():
    """
    Returns curated built-in DSA problems dataset.
    """
    _, classifier = get_services()
    return classifier.known_problems

@router.get("/sample-files/{filename}")
def download_sample_file(filename: str):
    """
    Allows user to download sample DSA sheets (txt, csv, docx).
    """
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    file_path = os.path.join(upload_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Sample file {filename} not found.")
    return FileResponse(file_path, filename=filename)

@router.post("/upload", response_model=ParsedDocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a document (PDF, DOCX, TXT, CSV) and extracts LeetCode problems.
    """
    # Max file size 10MB
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 10MB.")

    filename = file.filename or "uploaded_sheet.txt"
    raw_text, file_type, tabular_rows = DocumentParser.extract_text_from_bytes(contents, filename)
    
    extractor, classifier = get_services()
    
    # Extract problems from tabular rows if available, else raw text
    if tabular_rows:
        raw_items = extractor.extract_from_tabular(tabular_rows)
    else:
        raw_items = extractor.extract_from_raw_text(raw_text)

    # If no problems detected, provide informative warning
    warnings = []
    if not raw_items:
        warnings.append("No standard LeetCode problems could be automatically detected from the file structure. You can paste lines or use the Built-in problem set.")

    # Classify & enrich every extracted item
    enriched_problems = []
    for item in raw_items:
        classified = classifier.classify_problem(item)
        enriched_problems.append(ParsedProblemItem(
            leetcode_number=classified.get("leetcode_number"),
            title=classified.get("title"),
            difficulty=classified.get("difficulty", "Medium"),
            topics=classified.get("topics", ["Arrays"]),
            subtopics=classified.get("subtopics", []),
            similar_concept=classified.get("similar_concept"),
            prerequisites=classified.get("prerequisites", []),
            source="uploaded_document",
            raw_text=item.get("raw_text")
        ))

    return ParsedDocumentResponse(
        filename=filename,
        file_type=file_type,
        total_problems_detected=len(enriched_problems),
        problems=enriched_problems,
        warnings=warnings
    )

@router.post("/parse-document", response_model=ParsedDocumentResponse)
async def parse_document_text(payload: Dict[str, str]):
    """
    Directly extracts problems from raw text input.
    """
    raw_text = payload.get("text", "")
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided.")

    extractor, classifier = get_services()
    raw_items = extractor.extract_from_raw_text(raw_text)

    enriched_problems = []
    for item in raw_items:
        classified = classifier.classify_problem(item)
        enriched_problems.append(ParsedProblemItem(
            leetcode_number=classified.get("leetcode_number"),
            title=classified.get("title"),
            difficulty=classified.get("difficulty", "Medium"),
            topics=classified.get("topics", ["Arrays"]),
            subtopics=classified.get("subtopics", []),
            similar_concept=classified.get("similar_concept"),
            prerequisites=classified.get("prerequisites", []),
            source="uploaded_document",
            raw_text=item.get("raw_text")
        ))

    return ParsedDocumentResponse(
        filename="manual_input.txt",
        file_type="txt",
        total_problems_detected=len(enriched_problems),
        problems=enriched_problems,
        warnings=[] if enriched_problems else ["No LeetCode problems recognized from text."]
    )

@router.post("/analyze-problems")
def analyze_problems(payload: Dict[str, Any]):
    """
    Analyzes topics, difficulty breakdown, and prerequisite flow of a problem set.
    """
    problems = payload.get("problems", [])
    if not problems:
        return {"total": 0, "topics": {}, "difficulties": {}, "prerequisites": []}

    topic_counts = {}
    diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    
    for p in problems:
        diff = p.get("difficulty", "Medium").capitalize()
        diff_counts[diff] = diff_counts.get(diff, 0) + 1
        
        topics = p.get("topics", ["General"])
        for t in topics:
            topic_counts[t] = topic_counts.get(t, 0) + 1

    return {
        "total": len(problems),
        "topics": topic_counts,
        "difficulties": diff_counts
    }

@router.post("/generate-roadmap", response_model=RoadmapResponse)
def generate_roadmap(config: RoadmapConfigRequest, db: Session = Depends(get_db)):
    """
    Generates a personalized, prerequisite-ordered, interleaved DSA preparation roadmap.
    Saves to SQLite database and returns the structured plan.
    """
    extractor, classifier = get_services()
    
    # 1. Choose problem pool
    problem_pool = []
    if config.problems and len(config.problems) > 0 and not config.use_built_in:
        for p in config.problems:
            classified = classifier.classify_problem(p)
            problem_pool.append(classified)
    else:
        # Use built-in problem pool
        problem_pool = classifier.known_problems

    if not problem_pool:
        raise HTTPException(status_code=400, detail="No problems available to generate roadmap.")

    # 2. Run roadmap generator
    roadmap_dict = RoadmapGenerator.generate_roadmap(
        problems=problem_pool,
        user_level=config.user_level,
        duration_months=config.duration_months,
        target_problem_count=config.target_problem_count,
        title=config.title or f"{config.user_level} {config.duration_months}-Month Roadmap"
    )

    # 3. Save roadmap to Database
    # Deactivate previous active roadmaps
    db.query(Roadmap).update({"is_active": False})
    db.commit()

    db_roadmap = Roadmap(
        id=roadmap_dict["id"],
        title=roadmap_dict["title"],
        user_level=roadmap_dict["user_level"],
        duration_months=roadmap_dict["duration_months"],
        target_problem_count=roadmap_dict["target_problem_count"],
        total_problems=roadmap_dict["total_problems"],
        total_weeks=roadmap_dict["total_weeks"],
        is_active=True,
        roadmap_data=json.dumps(roadmap_dict)
    )
    db.add(db_roadmap)
    db.commit()

    # Save individual roadmap items for database queries
    for week in roadmap_dict["weeks"]:
        w_num = week["week"]
        for day in week["days"]:
            d_num = day["day"]
            for idx, prob in enumerate(day["problems"], start=1):
                item = RoadmapItem(
                    roadmap_id=roadmap_dict["id"],
                    problem_id=prob.get("id"),
                    leetcode_number=prob.get("leetcode_number"),
                    title=prob.get("title"),
                    slug=prob.get("slug"),
                    difficulty=prob.get("difficulty"),
                    topic=prob.get("topic"),
                    similar_concept=prob.get("similar_concept"),
                    week_number=w_num,
                    day_number=d_num,
                    order_in_day=idx,
                    status="Not Started",
                    notes=""
                )
                db.add(item)
    db.commit()

    return roadmap_dict

@router.get("/roadmap/active/current")
def get_current_roadmap(db: Session = Depends(get_db)):
    """
    Returns the currently active roadmap.
    """
    active = db.query(Roadmap).filter(Roadmap.is_active == True).order_by(Roadmap.created_at.desc()).first()
    if not active:
        # If no active roadmap, generate one with default settings
        _, classifier = get_services()
        roadmap_dict = RoadmapGenerator.generate_roadmap(
            problems=classifier.known_problems,
            user_level="Average",
            duration_months=6,
            target_problem_count=150,
            title="6-Month DSA Mastery Roadmap"
        )
        active = Roadmap(
            id=roadmap_dict["id"],
            title=roadmap_dict["title"],
            user_level="Average",
            duration_months=6,
            target_problem_count=150,
            total_problems=roadmap_dict["total_problems"],
            total_weeks=roadmap_dict["total_weeks"],
            is_active=True,
            roadmap_data=json.dumps(roadmap_dict)
        )
        db.add(active)
        db.commit()

        # Save items
        for week in roadmap_dict["weeks"]:
            w_num = week["week"]
            for day in week["days"]:
                d_num = day["day"]
                for idx, prob in enumerate(day["problems"], start=1):
                    item = RoadmapItem(
                        roadmap_id=roadmap_dict["id"],
                        problem_id=prob.get("id"),
                        leetcode_number=prob.get("leetcode_number"),
                        title=prob.get("title"),
                        slug=prob.get("slug"),
                        difficulty=prob.get("difficulty"),
                        topic=prob.get("topic"),
                        similar_concept=prob.get("similar_concept"),
                        week_number=w_num,
                        day_number=d_num,
                        order_in_day=idx,
                        status="Not Started",
                        notes=""
                    )
                    db.add(item)
        db.commit()

    # Merge dynamic status from RoadmapItem table
    data = json.loads(active.roadmap_data)
    items_map = {}
    db_items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == active.id).all()
    for it in db_items:
        key = f"{it.week_number}_{it.day_number}_{it.order_in_day}"
        items_map[key] = it

    for week in data.get("weeks", []):
        w_num = week["week"]
        for day in week.get("days", []):
            d_num = day["day"]
            for idx, prob in enumerate(day.get("problems", []), start=1):
                key = f"{w_num}_{d_num}_{idx}"
                if key in items_map:
                    it = items_map[key]
                    prob["roadmap_item_id"] = it.id
                    prob["status"] = it.status
                    prob["notes"] = it.notes

    return data

@router.get("/roadmap/{roadmap_id}")
def get_roadmap_by_id(roadmap_id: str, db: Session = Depends(get_db)):
    rm = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not rm:
        raise HTTPException(status_code=404, detail="Roadmap not found.")
    return json.loads(rm.roadmap_data)

@router.get("/problems")
def get_problems(
    search: Optional[str] = None,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Returns problems from the curated dataset with filtering.
    """
    _, classifier = get_services()
    results = classifier.known_problems

    if search:
        s = search.lower()
        results = [p for p in results if s in p.get("title", "").lower() or str(p.get("leetcode_number", "")) == s or s in p.get("similar_concept", "").lower()]

    if topic and topic != "All":
        results = [p for p in results if topic.lower() in [t.lower() for t in p.get("topics", [])]]

    if difficulty and difficulty != "All":
        results = [p for p in results if p.get("difficulty", "").lower() == difficulty.lower()]

    return {
        "total": len(results),
        "problems": results[offset:offset+limit]
    }

@router.patch("/problems/{item_id}/status")
@router.patch("/roadmap/item/{item_id}/status")
def update_problem_status(item_id: int, payload: RoadmapItemStatusUpdate, db: Session = Depends(get_db)):
    """
    Updates the completion status of a roadmap item.
    When completed, automatically schedules spaced repetition intervals (2, 7, 21 days).
    """
    item = db.query(RoadmapItem).filter(RoadmapItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap item not found.")

    old_status = item.status
    item.status = payload.status
    if payload.notes is not None:
        item.notes = payload.notes

    if payload.status == "Completed" and old_status != "Completed":
        item.completed_at = datetime.now(timezone.utc)
        # Schedule revision items
        revisions = RevisionEngine.schedule_revisions_for_completed_problem(
            problem_id=item.problem_id or item.id,
            leetcode_number=item.leetcode_number,
            title=item.title,
            topic=item.topic,
            difficulty=item.difficulty,
            similar_concept=item.similar_concept,
            roadmap_id=item.roadmap_id
        )
        for rev in revisions:
            # Check if revision already exists
            exists = db.query(RevisionItem).filter(
                RevisionItem.roadmap_id == rev["roadmap_id"],
                RevisionItem.problem_id == rev["problem_id"],
                RevisionItem.interval_day == rev["interval_day"]
            ).first()
            if not exists:
                db_rev = RevisionItem(**rev)
                db.add(db_rev)
    elif payload.status != "Completed":
        item.completed_at = None

    db.commit()
    db.refresh(item)
    return item.to_dict()

@router.get("/today")
def get_today_problems(db: Session = Depends(get_db)):
    """
    Returns today's designated problems from the active roadmap.
    Finds the first day with incomplete problems.
    """
    active = db.query(Roadmap).filter(Roadmap.is_active == True).order_by(Roadmap.created_at.desc()).first()
    if not active:
        return {"week": 1, "day": 1, "focus_topic": "Arrays", "problems": [], "completed_count": 0}

    # Find earliest day with uncompleted problems
    all_items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == active.id).order_by(RoadmapItem.week_number, RoadmapItem.day_number, RoadmapItem.order_in_day).all()
    
    target_week = 1
    target_day = 1
    unsolved_items = [it for it in all_items if it.status != "Completed"]
    
    if unsolved_items:
        target_week = unsolved_items[0].week_number
        target_day = unsolved_items[0].day_number

    today_items = [it for it in all_items if it.week_number == target_week and it.day_number == target_day]
    
    # Calculate streak (consecutive days with completed items)
    completed_items = [it for it in all_items if it.status == "Completed"]

    return {
        "roadmap_id": active.id,
        "week": target_week,
        "day": target_day,
        "focus_topic": today_items[0].topic if today_items else "General Review",
        "total_today": len(today_items),
        "problems": [it.to_dict() for it in today_items],
        "completed_today": len([it for it in today_items if it.status == "Completed"]),
        "overall_completed": len(completed_items),
        "overall_total": len(all_items)
    }

@router.get("/progress", response_model=ProgressResponse)
def get_progress(db: Session = Depends(get_db)):
    """
    Computes comprehensive progress statistics, topic mastery breakdown, and weak topic alerts.
    """
    active = db.query(Roadmap).filter(Roadmap.is_active == True).order_by(Roadmap.created_at.desc()).first()
    if not active:
        return ProgressResponse(
            roadmap_id="",
            total_problems=0,
            completed=0,
            in_progress=0,
            not_started=0,
            skipped=0,
            completion_percentage=0.0,
            current_streak=0,
            estimated_hours_left=0.0,
            topic_breakdown=[],
            difficulty_breakdown={"Easy": {"total": 0, "completed": 0}, "Medium": {"total": 0, "completed": 0}, "Hard": {"total": 0, "completed": 0}},
            weak_topics=[]
        )

    items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == active.id).all()
    total = len(items)
    completed = len([i for i in items if i.status == "Completed"])
    in_progress = len([i for i in items if i.status == "In Progress"])
    skipped = len([i for i in items if i.status == "Skipped"])
    not_started = total - completed - in_progress - skipped

    pct = round((completed / total * 100.0), 1) if total > 0 else 0.0

    # Topic breakdown
    topic_map = {}
    diff_map = {
        "Easy": {"total": 0, "completed": 0},
        "Medium": {"total": 0, "completed": 0},
        "Hard": {"total": 0, "completed": 0}
    }

    for it in items:
        # Topic
        t = it.topic or "General"
        if t not in topic_map:
            topic_map[t] = {"total": 0, "completed": 0}
        topic_map[t]["total"] += 1
        if it.status == "Completed":
            topic_map[t]["completed"] += 1

        # Difficulty
        d = it.difficulty or "Medium"
        if d in diff_map:
            diff_map[d]["total"] += 1
            if it.status == "Completed":
                diff_map[d]["completed"] += 1

    topic_breakdown = []
    weak_topics_list = []
    for t, stat in topic_map.items():
        t_pct = round((stat["completed"] / stat["total"] * 100.0), 1) if stat["total"] > 0 else 0.0
        is_weak = (t_pct < 50.0 and stat["total"] >= 2)
        if is_weak:
            weak_topics_list.append(t)
        topic_breakdown.append(TopicProgress(
            topic=t,
            total=stat["total"],
            completed=stat["completed"],
            percentage=t_pct,
            is_weak=is_weak
        ))

    # Sort topics by total count descending
    topic_breakdown.sort(key=lambda x: x.total, reverse=True)

    # Estimate streak: minimum 1 if completed >= 1
    streak = 1 if completed > 0 else 0

    # Estimated hours left (avg 35 min per uncompleted problem)
    hours_left = round((total - completed) * 0.58, 1)

    return ProgressResponse(
        roadmap_id=active.id,
        total_problems=total,
        completed=completed,
        in_progress=in_progress,
        not_started=not_started,
        skipped=skipped,
        completion_percentage=pct,
        current_streak=streak,
        estimated_hours_left=hours_left,
        topic_breakdown=topic_breakdown,
        difficulty_breakdown=diff_map,
        weak_topics=weak_topics_list
    )

@router.get("/recommendations", response_model=RecommendationResponse)
def get_recommendations(db: Session = Depends(get_db)):
    """
    Detects weak topics and recommends additional problems from the pool.
    """
    progress = get_progress(db)
    weak_topics = progress.weak_topics

    if not weak_topics and progress.topic_breakdown:
        # Fallback to topic with lowest percentage
        sorted_by_pct = sorted(progress.topic_breakdown, key=lambda x: x.percentage)
        if sorted_by_pct:
            weak_topics = [sorted_by_pct[0].topic]

    active = db.query(Roadmap).filter(Roadmap.is_active == True).first()
    completed_ids = set()
    if active:
        completed_items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == active.id, RoadmapItem.status == "Completed").all()
        for c in completed_items:
            if c.leetcode_number:
                completed_ids.add(c.leetcode_number)
            if c.problem_id:
                completed_ids.add(c.problem_id)

    _, classifier = get_services()
    recs_data = []
    
    for wt in weak_topics[:3]:
        found = 0
        for p in classifier.known_problems:
            p_id = p.get("leetcode_number") or p.get("id")
            if p_id in completed_ids:
                continue
            topics = [t.lower() for t in p.get("topics", [])]
            if wt.lower() in topics:
                recs_data.append({
                    "id": p.get("id"),
                    "leetcode_number": p.get("leetcode_number"),
                    "title": p.get("title"),
                    "slug": p.get("slug"),
                    "difficulty": p.get("difficulty"),
                    "topic": wt,
                    "similar_concept": p.get("similar_concept"),
                    "reason": f"Your {wt} performance is currently lower than other topics. Practice this {p.get('difficulty')} problem to master this pattern."
                })
                found += 1
                if found >= 3:
                    break

    message = f"Identified {len(weak_topics)} topic(s) that need reinforcement: {', '.join(weak_topics)}" if weak_topics else "Great progress! All topics are well balanced."

    return RecommendationResponse(
        weak_topics=weak_topics,
        message=message,
        recommendations=recs_data
    )

@router.get("/revision", response_model=List[RevisionItemResponse])
def get_revisions(status: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Returns spaced repetition revision items.
    """
    query = db.query(RevisionItem)
    if status and status != "All":
        query = query.filter(RevisionItem.status == status)

    items = query.order_by(RevisionItem.due_date.asc()).all()
    today_date = date.today()

    response = []
    for it in items:
        is_today = (it.due_date == today_date)
        is_over = (it.due_date < today_date)
        response.append(RevisionItemResponse(
            id=it.id,
            roadmap_id=it.roadmap_id,
            problem_id=it.problem_id,
            leetcode_number=it.leetcode_number,
            title=it.title,
            topic=it.topic,
            difficulty=it.difficulty,
            similar_concept=it.similar_concept,
            interval_day=it.interval_day,
            due_date=it.due_date.isoformat(),
            status=it.status,
            is_due_today=is_today,
            is_overdue=is_over
        ))
    return response

@router.patch("/revision/{rev_id}/status")
def update_revision_status(rev_id: int, payload: Dict[str, str], db: Session = Depends(get_db)):
    rev = db.query(RevisionItem).filter(RevisionItem.id == rev_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Revision item not found.")
    
    new_status = payload.get("status", "Completed")
    rev.status = new_status
    if new_status == "Completed":
        rev.completed_at = datetime.now(timezone.utc)
    db.commit()
    return rev.to_dict()

# ==========================================
# Google Drive Links & Formula Doc Endpoints
# ==========================================

@router.get("/drive-links")
def get_drive_links(db: Session = Depends(get_db)):
    """
    Returns all shared Google Drive resource links.
    Seeds default community links if table is empty.
    """
    links = db.query(DriveResource).order_by(DriveResource.created_at.desc()).all()
    if not links:
        # Seed initial shared resources
        defaults = [
            DriveResource(
                title="Community DSA Master Formula & Notes Drive",
                drive_url="https://drive.google.com/drive/folders/1DSA-Community-Master-Formulas-Shareable",
                contributor="DSA Roadmap AI",
                category="Formula Sheet & Notes",
                description="Central community Google Drive folder containing all master formulas, tricks, templates, and interview cheatsheets."
            ),
            DriveResource(
                title="Pattern-Wise LeetCode Solutions & Visual Notes",
                drive_url="https://drive.google.com/drive/folders/1LeetCode-Patterns-Visual-Notes",
                contributor="Interview Prep Community",
                category="Code Templates & Patterns",
                description="Shared Google Drive folder with handwritten intuition, recursion trees, and dynamic programming state transitions."
            )
        ]
        db.add_all(defaults)
        db.commit()
        links = db.query(DriveResource).order_by(DriveResource.created_at.desc()).all()

    return [l.to_dict() for l in links]

@router.post("/drive-links")
def add_drive_link(payload: Dict[str, str], db: Session = Depends(get_db)):
    """
    Allows any user to upload / share a Google Drive folder or document link.
    """
    title = payload.get("title", "").strip()
    drive_url = payload.get("drive_url", "").strip()
    contributor = payload.get("contributor", "Community Member").strip()
    description = payload.get("description", "").strip()
    category = payload.get("category", "Formula Sheet & Notes").strip()

    if not drive_url:
        raise HTTPException(status_code=400, detail="Google Drive URL is required.")

    if not title:
        title = "Community Shared DSA Folder"

    resource = DriveResource(
        title=title,
        drive_url=drive_url,
        contributor=contributor or "Community Member",
        description=description,
        category=category
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource.to_dict()

@router.get("/formula-doc")
def get_formula_doc():
    """
    Returns the full Markdown content of the DSA Formulas & Tricks Master Document for in-app viewing.
    """
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    md_path = os.path.join(uploads_dir, "DSA_Formulas_and_Tricks_Master.md")
    if not os.path.exists(md_path):
        from generate_formula_doc import create_dsa_formulas_doc
        create_dsa_formulas_doc()

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "title": "DSA Formulas, Patterns & Tricks Master Document",
        "format": "markdown",
        "content": content
    }

@router.get("/download-formula-doc")
def download_formula_doc():
    """
    Downloads the pre-generated Word (.docx) document containing all formulas and tricks,
    ready to be uploaded directly to Google Drive.
    """
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    docx_path = os.path.join(uploads_dir, "DSA_Formulas_and_Tricks_Master.docx")
    if not os.path.exists(docx_path):
        from generate_formula_doc import create_dsa_formulas_doc
        create_dsa_formulas_doc()

    return FileResponse(
        docx_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="DSA_Formulas_and_Tricks_Master.docx"
    )

