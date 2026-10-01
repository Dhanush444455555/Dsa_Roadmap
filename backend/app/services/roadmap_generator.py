import math
import uuid
from typing import List, Dict, Any, Optional

class RoadmapGenerator:
    """
    Intelligent DSA Roadmap Generation Service.
    Applies topic prerequisite graph, difficulty progression curve based on user level,
    concept interleaving (preventing single-topic fatigue), and spaced revision intervals.
    """

    TOPIC_ORDER = [
        "Arrays",
        "Hashing",
        "Strings",
        "Two Pointers",
        "Sliding Window",
        "Bit Manipulation",
        "Stack",
        "Queue",
        "Linked List",
        "Binary Search",
        "Recursion & Backtracking",
        "Greedy",
        "Binary Tree",
        "Binary Search Tree",
        "Heap",
        "Trie",
        "Graphs",
        "Dynamic Programming"
    ]

    DIFFICULTY_WEIGHTS = {
        "Beginner": {"Easy": 0.65, "Medium": 0.35, "Hard": 0.00},
        "Average": {"Easy": 0.25, "Medium": 0.60, "Hard": 0.15},
        "Advanced": {"Easy": 0.10, "Medium": 0.55, "Hard": 0.35}
    }

    MONTH_TOPIC_FOCUS = {
        1: ["Arrays", "Hashing", "Strings", "Two Pointers", "Sliding Window"],
        2: ["Bit Manipulation", "Stack", "Queue", "Linked List", "Binary Search"],
        3: ["Recursion & Backtracking", "Greedy", "Binary Tree", "Binary Search Tree"],
        4: ["Heap", "Trie", "Graphs"],
        5: ["Dynamic Programming", "Advanced Graphs", "Mixed Patterns"],
        6: ["Systematic Revision", "Weak Topics Reinforcement", "Mock Interviews"]
    }

    @classmethod
    def generate_roadmap(
        cls,
        problems: List[Dict[str, Any]],
        user_level: str = "Average",
        duration_months: int = 6,
        target_problem_count: int = 150,
        title: str = "Personalized DSA Roadmap"
    ) -> Dict[str, Any]:
        """
        Main roadmap creation pipeline.
        """
        # 1. Sanitize, deduplicate and categorize problems
        unique_problems = cls._deduplicate_problems(problems)
        
        # 2. Score and sort problems based on topic order and difficulty curve
        ranked_problems = cls._rank_and_order_problems(unique_problems, user_level, target_problem_count)
        
        total_selected = len(ranked_problems)
        total_weeks = max(4, duration_months * 4)
        
        # Determine problems per day
        days_per_week = 6  # 6 study days + 1 revision day
        total_active_days = total_weeks * days_per_week
        
        # Distribute problems into weeks and days
        weeks_data = cls._distribute_into_schedule(
            ranked_problems=ranked_problems,
            total_weeks=total_weeks,
            duration_months=duration_months,
            user_level=user_level
        )
        
        # Build month breakdown summary
        month_breakdown = cls._build_month_breakdown(duration_months, weeks_data)

        roadmap_id = str(uuid.uuid4())[:8]

        return {
            "id": roadmap_id,
            "title": title,
            "user_level": user_level,
            "duration_months": duration_months,
            "target_problem_count": target_problem_count,
            "total_problems": total_selected,
            "total_weeks": total_weeks,
            "month_breakdown": month_breakdown,
            "weeks": weeks_data
        }

    @classmethod
    def _deduplicate_problems(cls, problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        deduped = []
        for p in problems:
            lc = p.get("leetcode_number")
            title = p.get("title", "").strip().lower()
            key = f"{lc}_{title}" if lc else title
            if key and key not in seen:
                seen.add(key)
                # Ensure primary topic exists
                topics = p.get("topics") or []
                if not topics or topics == [""]:
                    topics = ["Arrays"]
                p["topic"] = topics[0]
                p["topics"] = topics
                p["difficulty"] = (p.get("difficulty") or "Medium").capitalize()
                if p["difficulty"] not in ["Easy", "Medium", "Hard"]:
                    p["difficulty"] = "Medium"
                deduped.append(p)
        return deduped

    @classmethod
    def _rank_and_order_problems(
        cls,
        problems: List[Dict[str, Any]],
        user_level: str,
        target_count: int
    ) -> List[Dict[str, Any]]:
        # Bucket by Topic
        topic_buckets: Dict[str, List[Dict[str, Any]]] = {t: [] for t in cls.TOPIC_ORDER}
        topic_buckets["Other"] = []

        for p in problems:
            primary_topic = p.get("topic", "Arrays")
            matched_key = "Other"
            for t in cls.TOPIC_ORDER:
                if t.lower() == primary_topic.lower() or t.lower() in [x.lower() for x in p.get("topics", [])]:
                    matched_key = t
                    break
            topic_buckets[matched_key].append(p)

        # Sort within each bucket by difficulty: Easy -> Medium -> Hard
        diff_order = {"Easy": 1, "Medium": 2, "Hard": 3}
        for t, bucket in topic_buckets.items():
            bucket.sort(key=lambda p: diff_order.get(p.get("difficulty", "Medium"), 2))

        # Interleaved topic collection along prerequisite DAG
        # We iterate through topics in order, picking Easy first, then Medium, then Hard
        ordered_problems = []
        
        # Pass 1: Core foundational problems (Easy & early Medium)
        for t in cls.TOPIC_ORDER:
            bucket = topic_buckets[t]
            easy_probs = [p for p in bucket if p.get("difficulty") == "Easy"]
            ordered_problems.extend(easy_probs)

        # Pass 2: Medium problems across topics in DAG order
        for t in cls.TOPIC_ORDER:
            bucket = topic_buckets[t]
            med_probs = [p for p in bucket if p.get("difficulty") == "Medium"]
            ordered_problems.extend(med_probs)

        # Pass 3: Hard / Advanced problems across topics in DAG order (for Average/Advanced)
        if user_level != "Beginner":
            for t in cls.TOPIC_ORDER:
                bucket = topic_buckets[t]
                hard_probs = [p for p in bucket if p.get("difficulty") == "Hard"]
                ordered_problems.extend(hard_probs)

        # Pass 4: Include any leftover or "Other" problems
        for p in topic_buckets["Other"]:
            if p not in ordered_problems:
                ordered_problems.append(p)

        # Include remaining unpicked problems if any
        for p in problems:
            if p not in ordered_problems:
                ordered_problems.append(p)

        # Filter according to user_level difficulty constraints if count exceeds target
        if len(ordered_problems) > target_count:
            if user_level == "Beginner":
                # Filter out Hard problems if possible
                filtered = [p for p in ordered_problems if p.get("difficulty") != "Hard"]
                if len(filtered) >= target_count:
                    ordered_problems = filtered[:target_count]
                else:
                    ordered_problems = ordered_problems[:target_count]
            else:
                ordered_problems = ordered_problems[:target_count]

        return ordered_problems

    @classmethod
    def _distribute_into_schedule(
        cls,
        ranked_problems: List[Dict[str, Any]],
        total_weeks: int,
        duration_months: int,
        user_level: str
    ) -> List[Dict[str, Any]]:
        weeks_data = []
        total_problems = len(ranked_problems)
        
        if total_problems == 0:
            return []

        # Average problems per week
        problems_per_week = max(1, math.ceil(total_problems / total_weeks))
        
        prob_idx = 0
        current_problem_id = 1

        for w in range(1, total_weeks + 1):
            # Calculate month
            month_num = min(duration_months, ((w - 1) // 4) + 1)
            
            # Select problems for this week
            week_problems = []
            while prob_idx < total_problems and len(week_problems) < problems_per_week:
                week_problems.append(ranked_problems[prob_idx])
                prob_idx += 1

            # If no problems left, we can review or stretch
            focus_topics = list(dict.fromkeys([p.get("topic", "DSA") for p in week_problems])) if week_problems else ["Revision & Mastery"]

            days_data = []
            # 7 Days in a week (Days 1-6 are learning/solving, Day 7 is Weekly Revision)
            num_learning_days = 6
            probs_per_day = math.ceil(len(week_problems) / num_learning_days) if len(week_problems) > 0 else 0

            p_week_idx = 0
            for d in range(1, 7):
                day_probs = []
                day_topic = "General DSA"
                
                for _ in range(probs_per_day):
                    if p_week_idx < len(week_problems):
                        p = week_problems[p_week_idx]
                        day_topic = p.get("topic", day_topic)
                        
                        day_prob_item = {
                            "id": current_problem_id,
                            "leetcode_number": p.get("leetcode_number"),
                            "title": p.get("title"),
                            "slug": p.get("slug") or cls._slugify(p.get("title", "")),
                            "difficulty": p.get("difficulty", "Medium"),
                            "topic": p.get("topic", "General"),
                            "topics": p.get("topics", [p.get("topic", "General")]),
                            "similar_concept": p.get("similar_concept") or "Standard Pattern",
                            "status": "Not Started",
                            "estimated_minutes": p.get("estimated_minutes", 30),
                            "order_in_day": len(day_probs) + 1,
                            "notes": p.get("note", "")
                        }
                        day_probs.append(day_prob_item)
                        current_problem_id += 1
                        p_week_idx += 1

                days_data.append({
                    "day": d,
                    "focus_topic": day_topic,
                    "is_revision": False,
                    "problems": day_probs
                })

            # Day 7: Weekly Revision & Practice
            days_data.append({
                "day": 7,
                "focus_topic": "Weekly Revision & Mock Practice",
                "is_revision": True,
                "problems": []
            })

            weeks_data.append({
                "week": w,
                "month": month_num,
                "focus": focus_topics if focus_topics else ["DSA Review"],
                "days": days_data
            })

        return weeks_data

    @classmethod
    def _build_month_breakdown(cls, duration_months: int, weeks_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        months = []
        for m in range(1, duration_months + 1):
            m_weeks = [w for w in weeks_data if w["month"] == m]
            week_nums = [w["week"] for w in m_weeks]
            
            # Aggregate topics in this month
            topics_in_month = []
            for w in m_weeks:
                for f in w["focus"]:
                    if f not in topics_in_month and f != "Revision & Mastery":
                        topics_in_month.append(f)

            default_title = " - ".join(topics_in_month[:3]) if topics_in_month else f"Month {m} Milestones"
            
            months.append({
                "month": m,
                "title": default_title,
                "focus_topics": topics_in_month if topics_in_month else ["DSA Foundations"],
                "weeks": week_nums
            })
        return months

    @staticmethod
    def _slugify(title: str) -> str:
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        return re.sub(r'[\s_]+', '-', slug).strip('-')
