import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Roadmap, RoadmapItem, Problem, RevisionQueue, UploadedDocument
from app.schemas import RoadmapGenerateRequest, ProblemActionRequest, TodayViewOut, RoadmapOut
from app.services.auth import get_current_user
from app.ai.graph import generate_roadmap_plan
from app.ai.nodes import AdaptNode, HintNode
from app.ai.vector_store import vector_store

router = APIRouter(prefix="/roadmap", tags=["roadmap"])

@router.post("/generate")
def generate_roadmap(
    req: RoadmapGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Archive previous active roadmaps
    prev_active = db.query(Roadmap).filter(
        Roadmap.user_id == current_user.id,
        Roadmap.status == "active"
    ).all()
    for r in prev_active:
        r.status = "archived"

    # Update user settings with onboarding choices
    settings = current_user.settings
    if settings:
        settings.duration_months = req.duration_months
        settings.level = req.level
        settings.daily_count = req.daily_count
        settings.timezone = req.timezone
        settings.reminder_time = req.reminder_time
        settings.source_type = req.source_type

    # Load uploaded sheet if applicable
    uploaded_problems = None
    if req.source_type == "uploaded" and req.document_id:
        doc = db.query(UploadedDocument).filter(
            UploadedDocument.id == req.document_id,
            UploadedDocument.user_id == current_user.id
        ).first()
        if doc and doc.parsed_problems:
            uploaded_problems = doc.parsed_problems

    # Run LangGraph pipeline
    planned_days = generate_roadmap_plan(
        duration_months=req.duration_months,
        level=req.level,
        daily_count=req.daily_count,
        uploaded_problems=uploaded_problems
    )

    # Create new Roadmap in DB
    new_roadmap = Roadmap(
        user_id=current_user.id,
        duration_months=req.duration_months,
        level=req.level,
        daily_count=req.daily_count,
        status="active",
        current_day_index=1,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(new_roadmap)
    db.flush()

    # Pre-fetch problems from DB for ID linking
    all_db_problems = {p.number: p for p in db.query(Problem).all()}

    now = datetime.datetime.utcnow()
    roadmap_items_to_add = []

    for item in planned_days:
        prob_dict = item["problem"]
        prob_num = prob_dict["number"]
        db_prob = all_db_problems.get(prob_num)

        if not db_prob:
            # Create problem record if it came from custom upload
            db_prob = Problem(
                number=prob_num,
                title=prob_dict["title"],
                difficulty=prob_dict.get("difficulty", "Medium"),
                topic=prob_dict.get("topic", "Arrays & Strings"),
                pattern=prob_dict.get("pattern", ""),
                similar_to=prob_dict.get("similar_to", ""),
                url=prob_dict.get("url", f"https://leetcode.com/problems/{prob_dict['title'].lower().replace(' ', '-')}/")
            )
            db.add(db_prob)
            db.flush()
            all_db_problems[prob_num] = db_prob

        # Set unlock time for day 1 to now; future days unlock after 24-hr cycle
        day_idx = item["day_index"]
        unlock_time = now if day_idx == 1 else None

        roadmap_items_to_add.append(
            RoadmapItem(
                roadmap_id=new_roadmap.id,
                day_index=day_idx,
                problem_id=db_prob.id,
                is_revision=item.get("is_revision", False),
                status="pending",
                assigned_at=now,
                unlock_at=unlock_time,
                tip=item.get("tip")
            )
        )

    db.bulk_save_objects(roadmap_items_to_add)
    db.commit()
    db.refresh(new_roadmap)

    return {
        "id": new_roadmap.id,
        "message": f"Successfully generated {req.duration_months}-month DSA roadmap with {len(planned_days)} items.",
        "duration_months": new_roadmap.duration_months,
        "level": new_roadmap.level,
        "daily_count": new_roadmap.daily_count,
        "status": new_roadmap.status,
        "current_day": 1,
        "total_days": req.duration_months * 30
    }

@router.get("/current")
def get_current_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = db.query(Roadmap).filter(
        Roadmap.user_id == current_user.id,
        Roadmap.status == "active"
    ).order_by(Roadmap.created_at.desc()).first()

    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active roadmap found. Please complete the setup."
        )

    items = db.query(RoadmapItem).filter(
        RoadmapItem.roadmap_id == roadmap.id
    ).order_by(RoadmapItem.day_index, RoadmapItem.id).all()

    # Format items with exact UI specifications
    formatted_items = []
    completed_count = 0
    for it in items:
        if it.status in ["done", "easy"]:
            completed_count += 1
        p = it.problem
        display = HintNode.format_problem_display({
            "number": p.number,
            "title": p.title,
            "difficulty": p.difficulty,
            "topic": p.topic,
            "pattern": p.pattern,
            "similar_to": p.similar_to,
            "url": p.url
        })
        formatted_items.append({
            "id": it.id,
            "day_index": it.day_index,
            "is_revision": it.is_revision,
            "status": it.status,
            "assigned_at": it.assigned_at,
            "completed_at": it.completed_at,
            "unlock_at": it.unlock_at,
            "tip": it.tip or display["tip"],
            "problem": {
                "id": p.id,
                "number": p.number,
                "title": p.title,
                "difficulty": p.difficulty,
                "topic": p.topic,
                "pattern": p.pattern,
                "similar_to": p.similar_to,
                "url": p.url,
                "display_header": display["display_header"],
                "display_hint": display["display_hint"]
            }
        })

    return {
        "id": roadmap.id,
        "duration_months": roadmap.duration_months,
        "level": roadmap.level,
        "daily_count": roadmap.daily_count,
        "status": roadmap.status,
        "current_day_index": roadmap.current_day_index,
        "total_days": roadmap.duration_months * 30,
        "completed_count": completed_count,
        "total_count": len(items),
        "items": formatted_items
    }

@router.get("/today")
def get_today_view(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns today's problem(s) with 24-hour cycle rule enforcement.
    Server-side time only: do not trust client clocks.
    """
    roadmap = db.query(Roadmap).filter(
        Roadmap.user_id == current_user.id,
        Roadmap.status == "active"
    ).order_by(Roadmap.created_at.desc()).first()

    if not roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active roadmap found. Please complete the setup."
        )

    now = datetime.datetime.utcnow()
    current_day = roadmap.current_day_index

    # Fetch items for current day
    today_items = db.query(RoadmapItem).filter(
        RoadmapItem.roadmap_id == roadmap.id,
        RoadmapItem.day_index == current_day
    ).all()

    # Check if all items today are completed
    all_done = len(today_items) > 0 and all(it.status in ["done", "easy", "hard", "skipped"] for it in today_items)

    # 24-Hour Rule: Next day unlocks 24 hours after completion of today's problems
    can_advance = False
    next_unlock_at = None

    if all_done and roadmap.last_response_at:
        unlock_threshold = roadmap.last_response_at + datetime.timedelta(hours=24)
        next_unlock_at = unlock_threshold
        if now >= unlock_threshold:
            can_advance = True
            # Automatically advance current_day_index if 24 hours elapsed
            total_days = roadmap.duration_months * 30
            if current_day < total_days:
                roadmap.current_day_index += 1
                db.commit()
                # Reload for next day
                current_day = roadmap.current_day_index
                today_items = db.query(RoadmapItem).filter(
                    RoadmapItem.roadmap_id == roadmap.id,
                    RoadmapItem.day_index == current_day
                ).all()
                all_done = False
                can_advance = False
                next_unlock_at = None

    # Format today's items
    formatted_items = []
    for it in today_items:
        p = it.problem
        display = HintNode.format_problem_display({
            "number": p.number,
            "title": p.title,
            "difficulty": p.difficulty,
            "topic": p.topic,
            "pattern": p.pattern,
            "similar_to": p.similar_to,
            "url": p.url
        })
        formatted_items.append({
            "id": it.id,
            "day_index": it.day_index,
            "is_revision": it.is_revision,
            "status": it.status,
            "assigned_at": it.assigned_at,
            "completed_at": it.completed_at,
            "unlock_at": it.unlock_at,
            "tip": it.tip or display["tip"],
            "problem": {
                "id": p.id,
                "number": p.number,
                "title": p.title,
                "difficulty": p.difficulty,
                "topic": p.topic,
                "pattern": p.pattern,
                "similar_to": p.similar_to,
                "url": p.url,
                "display_header": display["display_header"],
                "display_hint": display["display_hint"]
            }
        })

    # Count pending revision queue items
    revision_count = db.query(RevisionQueue).filter(
        RevisionQueue.user_id == current_user.id,
        RevisionQueue.resolved == False
    ).count()

    return {
        "current_day": current_day,
        "total_days": roadmap.duration_months * 30,
        "items": formatted_items,
        "can_advance": can_advance,
        "next_unlock_at": next_unlock_at,
        "revision_count": revision_count,
        "all_done_today": all_done,
        "server_time": now
    }

@router.post("/action")
def submit_problem_action(
    req: ProblemActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Handles user action on today's problem:
    - Done: mark complete, unlock next problem after 24-hr cycle.
    - Too Hard: replace upcoming problems of topic with easier/prerequisite problems, push to revision queue.
    - Too Easy: swap upcoming problems of topic for harder ones or next topic.
    - Skip: reschedule problem later in roadmap keeping total days invariant.
    """
    valid_actions = {"done", "hard", "easy", "skip"}
    if req.action not in valid_actions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action: '{req.action}'. Allowed: done, hard, easy, skip."
        )

    item = db.query(RoadmapItem).filter(RoadmapItem.id == req.roadmap_item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap item not found.")

    roadmap = db.query(Roadmap).filter(
        Roadmap.id == item.roadmap_id,
        Roadmap.user_id == current_user.id
    ).first()
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access to this roadmap item.")

    now = datetime.datetime.utcnow()
    item.completed_at = now
    roadmap.last_response_at = now

    all_items = db.query(RoadmapItem).filter(
        RoadmapItem.roadmap_id == roadmap.id
    ).order_by(RoadmapItem.day_index, RoadmapItem.id).all()

    # Prepare data for AdaptNode
    serialized_items = []
    for it in all_items:
        serialized_items.append({
            "id": it.id,
            "day_index": it.day_index,
            "status": it.status,
            "is_revision": it.is_revision,
            "problem": {
                "id": it.problem.id,
                "number": it.problem.number,
                "title": it.problem.title,
                "difficulty": it.problem.difficulty,
                "topic": it.problem.topic,
                "pattern": it.problem.pattern,
                "similar_to": it.problem.similar_to,
                "url": it.problem.url
            },
            "tip": it.tip
        })

    adapt_result = AdaptNode.run(
        current_roadmap_items=serialized_items,
        target_item_id=item.id,
        action=req.action,
        all_problems_pool=vector_store.problems
    )

    # Save action status on the target item
    item.status = req.action if req.action != "hard" else "hard"
    if req.action == "done":
        item.status = "done"

    # Add to RevisionQueue if Too Hard
    if req.action == "hard":
        rev_item = RevisionQueue(
            user_id=current_user.id,
            problem_id=item.problem_id,
            reason="too_hard",
            added_at=now,
            resolved=False
        )
        db.add(rev_item)

    # Apply re-planned upcoming problems if adapted
    if req.action in ["hard", "easy", "skip"]:
        all_db_problems = {p.number: p for p in db.query(Problem).all()}
        item_map = {it.id: it for it in all_items}
        
        for adapted_it in adapt_result.get("updated_items", []):
            db_item = item_map.get(adapted_it["id"])
            if db_item and db_item.status == "pending":
                prob_data = adapted_it["problem"]
                prob_num = prob_data["number"]
                db_p = all_db_problems.get(prob_num)
                if not db_p:
                    db_p = Problem(
                        number=prob_num,
                        title=prob_data["title"],
                        difficulty=prob_data.get("difficulty", "Medium"),
                        topic=prob_data.get("topic", "Arrays & Strings"),
                        pattern=prob_data.get("pattern", ""),
                        similar_to=prob_data.get("similar_to", ""),
                        url=prob_data.get("url", f"https://leetcode.com/problems/{prob_data['title'].lower().replace(' ', '-')}/")
                    )
                    db.add(db_p)
                    db.flush()
                    all_db_problems[prob_num] = db_p

                db_item.problem_id = db_p.id
                db_item.tip = adapted_it.get("tip")

    db.commit()

    return {
        "success": True,
        "action": req.action,
        "message": f"Recorded '{req.action}' for problem #{item.problem.number}.",
        "completed_at": item.completed_at
    }
