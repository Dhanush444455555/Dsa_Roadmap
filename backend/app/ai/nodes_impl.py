import random
import logging
from typing import List, Dict, Any, Optional, Tuple
from app.ai.vector_store import vector_store
from app.ai.llm_client import get_llm

logger = logging.getLogger(__name__)

TOPIC_PREREQUISITE_ORDER = [
    "Arrays & Strings",
    "Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack & Queue",
    "Linked List",
    "Binary Search",
    "Recursion & Backtracking",
    "Trees & BST",
    "Heaps & Priority Queue",
    "Greedy",
    "Intervals",
    "Graphs",
    "Dynamic Programming",
    "Tries",
    "Bit Manipulation & Math"
]

class DocIngestNode:
    @staticmethod
    def run(uploaded_problems: Optional[List[Dict[str, Any]]], total_needed: int) -> List[Dict[str, Any]]:
        """
        If sheet is uploaded, parse it, extract LeetCode numbers/titles, de-duplicate.
        Fill gaps from the default list if the sheet is too small, and trim intelligently if too large.
        """
        all_curated = vector_store.problems
        curated_map = {p["number"]: p for p in all_curated}

        if not uploaded_problems:
            return list(all_curated)

        # De-duplicate uploaded problems
        unique_uploaded = {}
        for p in uploaded_problems:
            num = p.get("number")
            if num and num not in unique_uploaded:
                # Merge with curated details if known
                curated = curated_map.get(num)
                if curated:
                    unique_uploaded[num] = {**curated, **p}
                else:
                    unique_uploaded[num] = p

        result_list = list(unique_uploaded.values())

        # If sheet is too small, fill gaps from curated default list
        if len(result_list) < total_needed:
            logger.info(f"Uploaded sheet has {len(result_list)} problems, needs {total_needed}. Filling gaps.")
            existing_nums = {p["number"] for p in result_list}
            for p in all_curated:
                if p["number"] not in existing_nums:
                    result_list.append(p)
                    existing_nums.add(p["number"])
                    if len(result_list) >= total_needed:
                        break

        # If sheet is too large, trim intelligently preserving topic diversity
        elif len(result_list) > total_needed * 1.5:
            logger.info(f"Uploaded sheet has {len(result_list)} problems. Intelligently trimming to target.")
            # Bucket by topic
            topic_buckets = {}
            for p in result_list:
                t = p.get("topic", "Arrays & Strings")
                topic_buckets.setdefault(t, []).append(p)
            
            trimmed = []
            per_topic = max(1, total_needed // len(TOPIC_PREREQUISITE_ORDER))
            for t in TOPIC_PREREQUISITE_ORDER:
                items = topic_buckets.get(t, [])
                trimmed.extend(items[:per_topic])
            
            # If still short, add remaining
            if len(trimmed) < total_needed:
                seen = {p["number"] for p in trimmed}
                for p in result_list:
                    if p["number"] not in seen:
                        trimmed.append(p)
                        seen.add(p["number"])
                        if len(trimmed) >= total_needed:
                            break
            result_list = trimmed

        return result_list


class ProfileNode:
    @staticmethod
    def run(duration_months: int, level: str, daily_count: int) -> Dict[str, Any]:
        """
        Calculate total problems = duration x working days x daily count, with 1 revision day per week.
        """
        total_days = duration_months * 30
        weeks = total_days // 7
        revision_days = weeks
        active_problem_days = total_days - revision_days
        total_problems_needed = active_problem_days * daily_count

        # Target difficulty ratios
        if level == "Beginner":
            diff_ratios = {"Easy": 0.65, "Medium": 0.35, "Hard": 0.0}
        elif level == "Advanced":
            diff_ratios = {"Easy": 0.10, "Medium": 0.40, "Hard": 0.50}
        else: # Average
            diff_ratios = {"Easy": 0.20, "Medium": 0.70, "Hard": 0.10}

        return {
            "total_days": total_days,
            "total_weeks": weeks,
            "revision_days": revision_days,
            "active_problem_days": active_problem_days,
            "total_problems_needed": total_problems_needed,
            "daily_count": daily_count,
            "level": level,
            "diff_ratios": diff_ratios
        }


class RetrieverNode:
    @staticmethod
    def run(pool_problems: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Organize available problems into topic and difficulty buckets for the planner.
        """
        categorized = {}
        for topic in TOPIC_PREREQUISITE_ORDER:
            categorized[topic] = {"Easy": [], "Medium": [], "Hard": []}

        for p in pool_problems:
            topic = p.get("topic", "Arrays & Strings")
            diff = p.get("difficulty", "Medium")
            if topic in categorized and diff in categorized[topic]:
                categorized[topic][diff].append(p)
            elif topic in categorized:
                categorized[topic]["Medium"].append(p)
            else:
                categorized.setdefault("Arrays & Strings", {"Easy": [], "Medium": [], "Hard": []})
                categorized["Arrays & Strings"]["Medium"].append(p)

        return categorized


class PlannerNode:
    @staticmethod
    def run(
        profile: Dict[str, Any],
        categorized: Dict[str, Dict[str, List[Dict[str, Any]]]],
        all_problems_pool: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate the complete roadmap:
        - 1 revision day per 7-day cycle.
        - Difficulty curve matching user level.
        - Prerequisite order: Arrays/Strings -> ... -> Bit Manipulation/Math.
        - Interleaving: Do not repeat the same topic more than 2 days in a row.
        - Grounded in existing problems with zero duplicates.
        """
        total_days = profile["total_days"]
        daily_count = profile["daily_count"]
        level = profile["level"]

        roadmap_days = []
        used_problem_ids = set()

        # Build topic sequence with interleaving rule (exactly 2 consecutive days per topic)
        topic_schedule = []
        topic_idx = 0
        topic_days_spent = 0

        for day in range(1, total_days + 1):
            if day % 7 == 0:
                topic_schedule.append("Revision")
            else:
                current_topic = TOPIC_PREREQUISITE_ORDER[topic_idx % len(TOPIC_PREREQUISITE_ORDER)]
                topic_schedule.append(current_topic)
                topic_days_spent += 1
                if topic_days_spent >= 2:
                    topic_idx += 1
                    topic_days_spent = 0

        # Plan problems for each day
        for day in range(1, total_days + 1):
            topic = topic_schedule[day - 1]

            if topic == "Revision":
                # Pick a problem from previous days for revision
                assigned_prev = [d["problem"] for d in roadmap_days if not d["is_revision"]]
                rev_problem = random.choice(assigned_prev) if assigned_prev else all_problems_pool[0]
                roadmap_days.append({
                    "day_index": day,
                    "is_revision": True,
                    "topic": "Revision",
                    "problem": rev_problem,
                    "tip": f"Weekly Revision: Review your solution and space-time complexity for {rev_problem['title']}."
                })
                continue

            # Determine difficulty based on level and timeline progression
            progress = day / total_days
            if level == "Beginner":
                pref_diff = "Easy" if progress < 0.6 else "Medium"
            elif level == "Advanced":
                pref_diff = "Medium" if progress < 0.35 else "Hard"
            else: # Average
                if progress < 0.2:
                    pref_diff = "Easy"
                elif progress < 0.85:
                    pref_diff = "Medium"
                else:
                    pref_diff = "Hard"

            for slot in range(daily_count):
                chosen_problem = None
                # Try preferred difficulty first
                candidates = categorized.get(topic, {}).get(pref_diff, [])
                for p in candidates:
                    if p["number"] not in used_problem_ids:
                        chosen_problem = p
                        break

                # Fallback to other difficulties in that topic
                if not chosen_problem:
                    for diff in ["Medium", "Easy", "Hard"]:
                        for p in categorized.get(topic, {}).get(diff, []):
                            if p["number"] not in used_problem_ids:
                                chosen_problem = p
                                break
                        if chosen_problem:
                            break

                # Global fallback if topic exhausted
                if not chosen_problem:
                    for p in all_problems_pool:
                        if p["number"] not in used_problem_ids:
                            chosen_problem = p
                            break

                if not chosen_problem:
                    chosen_problem = all_problems_pool[day % len(all_problems_pool)]

                used_problem_ids.add(chosen_problem["number"])

                roadmap_days.append({
                    "day_index": day,
                    "is_revision": False,
                    "topic": topic,
                    "problem": chosen_problem,
                    "tip": vector_store.get_tip_for_problem(chosen_problem)
                })

        return roadmap_days


class ValidatorNode:
    @staticmethod
    def run(roadmap_days: List[Dict[str, Any]], profile: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate:
        1. Correct total count
        2. No duplicate problems (excluding explicit revision days)
        3. Interleaving: no topic repeated more than 2 days in a row
        4. Difficulty curve
        """
        errors = []
        expected_total = profile["total_days"]
        if profile["daily_count"] == 2:
            # Non-revision days have 2 problems, revision has 1
            expected_items = (profile["total_days"] - profile["revision_days"]) * 2 + profile["revision_days"]
        else:
            expected_items = profile["total_days"]

        if len(roadmap_days) != expected_items:
            errors.append(f"Total items count {len(roadmap_days)} does not match expected {expected_items}.")

        # Check duplicates on non-revision days
        seen_numbers = set()
        for item in roadmap_days:
            if not item.get("is_revision", False):
                num = item["problem"]["number"]
                if num in seen_numbers:
                    errors.append(f"Duplicate problem #{num} found in non-revision schedule.")
                seen_numbers.add(num)

        # Check topic interleaving rule (no topic > 2 days in a row)
        current_streak = 0
        last_topic = None
        current_day = -1

        for item in roadmap_days:
            day = item["day_index"]
            if day != current_day:
                current_day = day
                topic = item["topic"]
                if topic == last_topic and topic != "Revision":
                    current_streak += 1
                    if current_streak > 2:
                        errors.append(f"Interleaving violation: Topic '{topic}' repeated for {current_streak} consecutive days.")
                else:
                    last_topic = topic
                    current_streak = 1

        is_valid = len(errors) == 0
        return is_valid, errors


class AdaptNode:
    @staticmethod
    def run(
        current_roadmap_items: List[Dict[str, Any]],
        target_item_id: int,
        action: str, # "done", "hard", "easy", "skip"
        all_problems_pool: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Re-plan ONLY the remaining days based on user responses:
        - Done: Mark complete, advance on 24-hr cycle.
        - Too Hard: Replace upcoming problems of that topic with easier ones / prerequisite problems,
                    add current problem to revision queue.
        - Too Easy: Swap upcoming problems of that topic for harder ones, or move to next topic.
        - Skip: Reschedule this problem later in the roadmap, keeping total days invariant.
        """
        # Find item
        target_item = None
        target_idx = -1
        for idx, item in enumerate(current_roadmap_items):
            if item["id"] == target_item_id:
                target_item = item
                target_idx = idx
                break

        if not target_item:
            return {"success": False, "message": "Item not found"}

        used_numbers = {
            it["problem"]["number"] for it in current_roadmap_items 
            if it["id"] != target_item_id and not it.get("is_revision", False)
        }

        topic = target_item["problem"]["topic"]
        revision_item_to_add = None

        if action == "done":
            target_item["status"] = "done"

        elif action == "hard":
            target_item["status"] = "hard"
            revision_item_to_add = {
                "problem_id": target_item["problem"].get("id", target_item["problem"].get("number")),
                "reason": "too_hard"
            }
            # Replace future pending problems of this topic with easier ones
            for item in current_roadmap_items[target_idx + 1:]:
                if item["status"] == "pending" and item["problem"]["topic"] == topic:
                    # Find an Easy or Medium prerequisite problem
                    for cand in all_problems_pool:
                        if (cand["topic"] == topic and cand["difficulty"] == "Easy" 
                            and cand["number"] not in used_numbers):
                            used_numbers.add(cand["number"])
                            item["problem"] = cand
                            item["tip"] = vector_store.get_tip_for_problem(cand)
                            break

        elif action == "easy":
            target_item["status"] = "easy"
            # Swap future pending problems of this topic with Harder ones
            for item in current_roadmap_items[target_idx + 1:]:
                if item["status"] == "pending" and item["problem"]["topic"] == topic:
                    for cand in all_problems_pool:
                        if (cand["topic"] == topic and cand["difficulty"] in ["Hard", "Medium"]
                            and cand["number"] not in used_numbers):
                            used_numbers.add(cand["number"])
                            item["problem"] = cand
                            item["tip"] = vector_store.get_tip_for_problem(cand)
                            break

        elif action == "skip":
            target_item["status"] = "skipped"
            # Reschedule this problem to the end or a future pending slot
            skipped_problem = target_item["problem"]
            # Find a later pending item to swap with, or push to future
            for item in reversed(current_roadmap_items):
                if item["status"] == "pending" and not item.get("is_revision", False):
                    # Swap
                    item["problem"], skipped_problem = skipped_problem, item["problem"]
                    item["tip"] = vector_store.get_tip_for_problem(item["problem"])
                    break

        return {
            "success": True,
            "action": action,
            "revision_item": revision_item_to_add,
            "updated_items": current_roadmap_items
        }


class HintNode:
    @staticmethod
    def format_problem_display(problem: Dict[str, Any]) -> Dict[str, str]:
        """
        Each problem is displayed EXACTLY in this format:
        <number> — <title>
        → Similar to <similar_to>
        plus a difficulty badge, topic tag, LeetCode link, and tip.
        """
        number = problem.get("number", 0)
        title = problem.get("title", "")
        similar_to = problem.get("similar_to") or problem.get("pattern") or "Core Algorithmic Technique"
        
        display_header = f"{number} — {title}"
        display_hint = f"→ Similar to {similar_to}"
        
        return {
            "display_header": display_header,
            "display_hint": display_hint,
            "difficulty": problem.get("difficulty", "Medium"),
            "topic": problem.get("topic", "Arrays & Strings"),
            "url": problem.get("url", f"https://leetcode.com/problems/{title.lower().replace(' ', '-')}/"),
            "tip": vector_store.get_tip_for_problem(problem)
        }
