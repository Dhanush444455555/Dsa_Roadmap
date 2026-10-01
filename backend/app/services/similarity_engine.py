import re
from typing import List, Dict, Any, Optional

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class SimilarityEngine:
    """
    Computes semantic and conceptual similarity between DSA problems.
    Supports TF-IDF + Cosine Similarity with automatic fallback to Jaccard token matching.
    """

    def __init__(self, problems: List[Dict[str, Any]]):
        self.problems = problems
        self.vectorizer = None
        self.tfidf_matrix = None
        self._fit()

    def _fit(self):
        if not self.problems:
            return

        corpus = []
        for p in self.problems:
            title = p.get("title", "")
            topics = " ".join(p.get("topics", []))
            subtopics = " ".join(p.get("subtopics", []))
            similar_concept = p.get("similar_concept", "")
            doc = f"{title} {topics} {subtopics} {similar_concept} {p.get('difficulty', '')}"
            corpus.append(doc)

        if SKLEARN_AVAILABLE and len(corpus) > 1:
            try:
                self.vectorizer = TfidfVectorizer(stop_words="english")
                self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
            except Exception:
                self.vectorizer = None
                self.tfidf_matrix = None

    def find_similar_problems(self, target_problem: Dict[str, Any], top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.problems:
            return []

        target_lc = target_problem.get("leetcode_number")
        target_title = target_problem.get("title", "").lower()
        target_topic = (target_problem.get("topics") or [""])[0]

        # If vectorizer is fitted
        if SKLEARN_AVAILABLE and self.vectorizer and self.tfidf_matrix is not None:
            try:
                target_doc = f"{target_problem.get('title', '')} {' '.join(target_problem.get('topics', []))} {target_problem.get('similar_concept', '')}"
                target_vec = self.vectorizer.transform([target_doc])
                sims = cosine_similarity(target_vec, self.tfidf_matrix)[0]
                
                scored_indices = []
                for idx, score in enumerate(sims):
                    p = self.problems[idx]
                    if p.get("leetcode_number") == target_lc or p.get("title", "").lower() == target_title:
                        continue
                    scored_indices.append((score, p))

                scored_indices.sort(key=lambda x: x[0], reverse=True)
                return [p for score, p in scored_indices[:top_k]]
            except Exception:
                pass

        # Fallback Jaccard & Topic matching
        scored = []
        target_tokens = set(re.findall(r'\w+', target_title))
        for p in self.problems:
            if p.get("leetcode_number") == target_lc or p.get("title", "").lower() == target_title:
                continue
            
            p_tokens = set(re.findall(r'\w+', p.get("title", "").lower()))
            intersection = len(target_tokens & p_tokens)
            union = len(target_tokens | p_tokens) or 1
            jaccard = intersection / union

            score = jaccard
            if (p.get("topics") or [""])[0] == target_topic:
                score += 0.5
            if p.get("difficulty") == target_problem.get("difficulty"):
                score += 0.2

            scored.append((score, p))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for score, p in scored[:top_k]]
