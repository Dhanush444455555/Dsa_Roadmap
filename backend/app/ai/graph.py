import logging
from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from app.ai.nodes import (
    DocIngestNode,
    ProfileNode,
    RetrieverNode,
    PlannerNode,
    ValidatorNode,
    AdaptNode,
    HintNode
)

logger = logging.getLogger(__name__)

class RoadmapState(TypedDict):
    duration_months: int
    level: str
    daily_count: int
    uploaded_problems: Optional[List[Dict[str, Any]]]
    profile: Dict[str, Any]
    pool_problems: List[Dict[str, Any]]
    categorized: Dict[str, Any]
    roadmap_days: List[Dict[str, Any]]
    is_valid: bool
    validation_errors: List[str]
    retry_count: int

def profile_step(state: RoadmapState) -> Dict[str, Any]:
    profile = ProfileNode.run(
        duration_months=state["duration_months"],
        level=state["level"],
        daily_count=state["daily_count"]
    )
    return {"profile": profile}

def doc_ingest_step(state: RoadmapState) -> Dict[str, Any]:
    total_needed = state["profile"]["total_problems_needed"]
    pool = DocIngestNode.run(state.get("uploaded_problems"), total_needed)
    return {"pool_problems": pool}

def retriever_step(state: RoadmapState) -> Dict[str, Any]:
    categorized = RetrieverNode.run(state["pool_problems"])
    return {"categorized": categorized}

def planner_step(state: RoadmapState) -> Dict[str, Any]:
    roadmap_days = PlannerNode.run(
        profile=state["profile"],
        categorized=state["categorized"],
        all_problems_pool=state["pool_problems"]
    )
    return {"roadmap_days": roadmap_days}

def validator_step(state: RoadmapState) -> Dict[str, Any]:
    is_valid, errors = ValidatorNode.run(state["roadmap_days"], state["profile"])
    retry_count = state.get("retry_count", 0)
    if not is_valid:
        retry_count += 1
        logger.warning(f"Validation failed (attempt {retry_count}): {errors}")
    return {
        "is_valid": is_valid,
        "validation_errors": errors,
        "retry_count": retry_count
    }

def route_after_validation(state: RoadmapState) -> str:
    if state["is_valid"]:
        return END
    if state.get("retry_count", 0) >= 3:
        logger.warning("Max retries reached in LangGraph. Falling back to deterministic valid plan.")
        return END
    return "planner"

# Build LangGraph workflow
workflow = StateGraph(RoadmapState)

workflow.add_node("profile", profile_step)
workflow.add_node("doc_ingest", doc_ingest_step)
workflow.add_node("retriever", retriever_step)
workflow.add_node("planner", planner_step)
workflow.add_node("validator", validator_step)

workflow.set_entry_point("profile")
workflow.add_edge("profile", "doc_ingest")
workflow.add_edge("doc_ingest", "retriever")
workflow.add_edge("retriever", "planner")
workflow.add_edge("planner", "validator")

workflow.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "planner": "planner",
        END: END
    }
)

roadmap_agent = workflow.compile()

def generate_roadmap_plan(
    duration_months: int,
    level: str,
    daily_count: int,
    uploaded_problems: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    initial_state: RoadmapState = {
        "duration_months": duration_months,
        "level": level,
        "daily_count": daily_count,
        "uploaded_problems": uploaded_problems,
        "profile": {},
        "pool_problems": [],
        "categorized": {},
        "roadmap_days": [],
        "is_valid": False,
        "validation_errors": [],
        "retry_count": 0
    }
    
    final_state = roadmap_agent.invoke(initial_state)
    return final_state["roadmap_days"]
