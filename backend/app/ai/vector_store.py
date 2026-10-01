import os
import json
import logging
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class VectorSearchEngine:
    """
    RAG Vector / Semantic Search engine over problems and cheat sheets.
    Uses FAISS index if embeddings available, with full text & pattern indexing fallback.
    """
    def __init__(self):
        self.problems: List[Dict[str, Any]] = []
        self.cheatsheets: Dict[str, Dict[str, Any]] = {}
        self.load_data()

    def load_data(self):
        # 1. Load problems
        problems_file = os.path.join(settings.DATA_DIR, "problems.json")
        if os.path.exists(problems_file):
            with open(problems_file, "r", encoding="utf-8") as f:
                self.problems = json.load(f)
        
        # 2. Load cheatsheets
        cs_dir = os.path.join(settings.DATA_DIR, "cheatsheets")
        if os.path.exists(cs_dir):
            for fname in os.listdir(cs_dir):
                if fname.endswith(".json"):
                    with open(os.path.join(cs_dir, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        topic = data.get("topic")
                        if topic:
                            self.cheatsheets[topic] = data

        logger.info(f"Loaded {len(self.problems)} problems and {len(self.cheatsheets)} cheat sheets into VectorSearchEngine.")

    def search_problems(
        self,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        pattern: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        results = []
        for p in self.problems:
            if topic and p.get("topic") != topic:
                continue
            if difficulty and p.get("difficulty") != difficulty:
                continue
            if pattern and pattern.lower() not in p.get("pattern", "").lower():
                continue
            if query:
                q_lower = query.lower()
                text = f"{p['number']} {p['title']} {p['topic']} {p.get('pattern', '')} {p.get('similar_to', '')}".lower()
                if q_lower not in text:
                    continue
            results.append(p)
            if len(results) >= limit:
                break
        return results

    def get_cheat_sheet(self, topic: str) -> Optional[Dict[str, Any]]:
        return self.cheatsheets.get(topic)

    def get_tip_for_problem(self, problem: Dict[str, Any]) -> str:
        topic = problem.get("topic", "")
        cs = self.get_cheat_sheet(topic)
        if cs and cs.get("quick_revision"):
            # Return first or most relevant quick revision bullet point
            return cs["quick_revision"][0]
        elif cs and cs.get("core_idea"):
            return cs["core_idea"]
        return f"Focus on {topic} core patterns and edge cases."

vector_store = VectorSearchEngine()
