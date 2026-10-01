from typing import List, Dict, Any

class RecommendationEngine:
    """
    Identifies weak topics based on user completion rate (<50% completion or lowest % topic)
    and suggests targeted unsolved problems from the uploaded sheet / problem pool.
    """

    @staticmethod
    def analyze_weak_topics(
        topic_stats: Dict[str, Dict[str, int]],
        threshold_percentage: float = 50.0
    ) -> List[Dict[str, Any]]:
        """
        Returns list of topics that need reinforcement.
        """
        weak_topics = []
        for topic, stat in topic_stats.items():
            total = stat.get("total", 0)
            completed = stat.get("completed", 0)
            if total > 0:
                pct = (completed / total) * 100.0
                if pct < threshold_percentage:
                    weak_topics.append({
                        "topic": topic,
                        "total": total,
                        "completed": completed,
                        "percentage": round(pct, 1),
                        "gap": total - completed
                    })

        # Sort by lowest percentage first, then largest uncompleted count
        weak_topics.sort(key=lambda x: (x["percentage"], -x["gap"]))
        return weak_topics

    @staticmethod
    def recommend_problems_for_weak_topics(
        weak_topics: List[Dict[str, Any]],
        available_problems: List[Dict[str, Any]],
        completed_problem_ids: set,
        limit_per_topic: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Finds unsolved problems from the available pool belonging to the weak topics.
        """
        recommendations = []
        
        for wt in weak_topics[:3]:  # Top 3 weakest topics
            topic_name = wt["topic"]
            found = 0
            for p in available_problems:
                p_id = p.get("id") or p.get("leetcode_number")
                if p_id in completed_problem_ids:
                    continue

                p_topics = p.get("topics") or [p.get("topic", "")]
                if topic_name.lower() in [t.lower() for t in p_topics]:
                    diff = p.get("difficulty", "Medium")
                    recommendations.append({
                        "id": p.get("id"),
                        "leetcode_number": p.get("leetcode_number"),
                        "title": p.get("title"),
                        "slug": p.get("slug"),
                        "difficulty": diff,
                        "topic": topic_name,
                        "similar_concept": p.get("similar_concept") or "Pattern Practice",
                        "reason": f"Your {topic_name} progress is currently at {wt['percentage']}%. Solve this {diff} problem to build mastery."
                    })
                    found += 1
                    if found >= limit_per_topic:
                        break

        return recommendations
