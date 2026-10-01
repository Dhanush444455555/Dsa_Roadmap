from datetime import date, timedelta, datetime
from typing import List, Dict, Any, Optional

class RevisionEngine:
    """
    Spaced Repetition Engine for DSA Mastery:
    - Interval 1: 2 Days after solving (Quick Recall)
    - Interval 2: 7 Days after solving (Weekly Reinforcement)
    - Interval 3: 21 Days after solving (Long-term Retention)
    """

    INTERVALS = [2, 7, 21]

    @classmethod
    def schedule_revisions_for_completed_problem(
        cls,
        problem_id: int,
        leetcode_number: Optional[int],
        title: str,
        topic: str,
        difficulty: str,
        similar_concept: Optional[str],
        roadmap_id: str,
        completion_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        if completion_date is None:
            completion_date = date.today()

        scheduled = []
        for interval in cls.INTERVALS:
            due_date = completion_date + timedelta(days=interval)
            scheduled.append({
                "roadmap_id": roadmap_id,
                "problem_id": problem_id,
                "leetcode_number": leetcode_number,
                "title": title,
                "topic": topic,
                "difficulty": difficulty,
                "similar_concept": similar_concept,
                "interval_day": interval,
                "due_date": due_date,
                "status": "Pending"
            })
        return scheduled

    @staticmethod
    def classify_revision_urgency(due_date: date, target_date: Optional[date] = None) -> Dict[str, bool]:
        if target_date is None:
            target_date = date.today()

        is_due_today = (due_date == target_date)
        is_overdue = (due_date < target_date)
        return {
            "is_due_today": is_due_today,
            "is_overdue": is_overdue
        }
