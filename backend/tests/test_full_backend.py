import pytest
import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.ai.nodes import ProfileNode, PlannerNode, ValidatorNode, AdaptNode, HintNode, TOPIC_PREREQUISITE_ORDER
from app.ai.vector_store import vector_store
from app.ai.graph import generate_roadmap_plan

client = TestClient(app)

def test_profile_node():
    profile = ProfileNode.run(duration_months=6, level="Average", daily_count=1)
    assert profile["total_days"] == 180
    assert profile["total_weeks"] == 25
    assert profile["revision_days"] == 25
    assert profile["active_problem_days"] == 155
    assert profile["total_problems_needed"] == 155

def test_planner_and_validator_interleaving():
    profile = ProfileNode.run(duration_months=3, level="Beginner", daily_count=1)
    plan = generate_roadmap_plan(duration_months=3, level="Beginner", daily_count=1)
    assert len(plan) == profile["total_days"]
    
    # Check validator
    is_valid, errors = ValidatorNode.run(plan, profile)
    assert is_valid, f"Validation errors: {errors}"
    assert len(errors) == 0

def test_hint_node_formatting():
    prob = {
        "number": 1710,
        "title": "Maximum Units on a Truck",
        "difficulty": "Easy",
        "topic": "Greedy",
        "pattern": "Sort by Units/Box Descending",
        "similar_to": "Fractional Knapsack (greedy by value/weight)"
    }
    hint = HintNode.format_problem_display(prob)
    assert hint["display_header"] == "1710 — Maximum Units on a Truck"
    assert hint["display_hint"] == "→ Similar to Fractional Knapsack (greedy by value/weight)"
    assert "https://leetcode.com/problems/" in hint["url"]
    assert len(hint["tip"]) > 0

def test_adapt_node_actions():
    sample_pool = vector_store.problems
    sample_items = [
        {
            "id": 1,
            "day_index": 1,
            "status": "pending",
            "is_revision": False,
            "problem": sample_pool[0],
            "tip": "Tip 1"
        },
        {
            "id": 2,
            "day_index": 2,
            "status": "pending",
            "is_revision": False,
            "problem": sample_pool[1],
            "tip": "Tip 2"
        },
        {
            "id": 3,
            "day_index": 3,
            "status": "pending",
            "is_revision": False,
            "problem": sample_pool[2],
            "tip": "Tip 3"
        }
    ]

    # Test "done"
    res_done = AdaptNode.run(sample_items, target_item_id=1, action="done", all_problems_pool=sample_pool)
    assert res_done["success"]
    assert sample_items[0]["status"] == "done"

    # Test "hard"
    res_hard = AdaptNode.run(sample_items, target_item_id=2, action="hard", all_problems_pool=sample_pool)
    assert res_hard["success"]
    assert sample_items[1]["status"] == "hard"
    assert res_hard["revision_item"]["reason"] == "too_hard"

def test_full_roadmap_api_flow():
    # 1. Register test user
    email = f"coder_{int(datetime.datetime.utcnow().timestamp())}@test.com"
    pwd = "password123"
    reg = client.post("/api/auth/register", json={"email": email, "password": pwd, "name": "Algo Master"})
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Generate roadmap
    gen_resp = client.post("/api/roadmap/generate", json={
        "source_type": "default",
        "duration_months": 3,
        "level": "Average",
        "daily_count": 1,
        "timezone": "UTC",
        "reminder_time": "09:00"
    }, headers=headers)
    assert gen_resp.status_code == 200
    gen_data = gen_resp.json()
    assert gen_data["current_day"] == 1

    # 3. Get /today view
    today_resp = client.get("/api/roadmap/today", headers=headers)
    assert today_resp.status_code == 200
    today_data = today_resp.json()
    assert today_data["current_day"] == 1
    assert len(today_data["items"]) >= 1
    
    first_item = today_data["items"][0]
    assert "—" in first_item["problem"]["display_header"]
    assert "→ Similar to" in first_item["problem"]["display_hint"]

    # 4. Action: Done
    action_resp = client.post("/api/roadmap/action", json={
        "roadmap_item_id": first_item["id"],
        "action": "done"
    }, headers=headers)
    assert action_resp.status_code == 200

    # 5. Check Cheatsheets API
    cs_resp = client.get("/api/cheatsheets/", headers=headers)
    assert cs_resp.status_code == 200
    assert len(cs_resp.json()) == 16

    # 6. Check single topic cheat sheet
    single_cs = client.get("/api/cheatsheets/two-pointers", headers=headers)
    assert single_cs.status_code == 200
    content = single_cs.json()["content"]
    assert "code_templates" in content
    assert "python" in content["code_templates"]
    assert "cpp" in content["code_templates"]
    assert "java" in content["code_templates"]
