import os
import json
import re
from typing import List, Dict, Any, Optional

class ProblemClassifier:
    """
    Classifies problems into DSA topics, difficulties, subtopics, prerequisites, and similar concepts.
    Uses a hybrid approach:
    1. Built-in curated dataset (Ground Truth)
    2. Deterministic keyword and pattern rules
    3. LLM API fallback for ambiguous items (if enabled)
    """

    TOPIC_KEYWORD_MAP = {
        "Arrays": ["array", "subarray", "matrix", "rotate", "duplicate", "majority", "pascal", "product of array"],
        "Hashing": ["hash", "hashmap", "hashing", "two sum", "anagram", "frequency", "contains duplicate"],
        "Strings": ["string", "substring", "palindrome", "parentheses", "roman", "prefix", "anagram", "word"],
        "Two Pointers": ["two pointer", "pointer", "container with most water", "3sum", "move zeroes", "remove duplicate"],
        "Sliding Window": ["sliding window", "minimum size subarray", "longest substring", "permutation in string"],
        "Bit Manipulation": ["bit", "xor", "bits", "single number", "power of two", "hamming"],
        "Stack": ["stack", "parentheses", "reverse polish", "asteroid", "temperatures", "histogram", "rain water", "monotonic"],
        "Queue": ["queue", "circular queue", "sliding window maximum", "recent counter"],
        "Linked List": ["linked list", "list node", "cycle", "reverse linked list", "merge two sorted lists", "lru cache", "middle of"],
        "Binary Search": ["binary search", "search in rotated", "koko", "capacity", "median of two sorted", "peak element", "sqrt", "insert position"],
        "Recursion & Backtracking": ["backtracking", "recursion", "n-queens", "sudoku", "combination sum", "subsets", "permutations", "word search"],
        "Greedy": ["greedy", "jump game", "gas station", "interval", "task scheduler", "candy", "fractional knapsack", "shortest job first", "maximum units"],
        "Binary Tree": ["tree", "binary tree", "inorder", "preorder", "postorder", "level order", "diameter", "symmetric tree", "depth"],
        "Binary Search Tree": ["bst", "binary search tree", "kth smallest", "validate bst", "lowest common ancestor"],
        "Heap": ["heap", "priority queue", "kth largest", "k closest", "median from data stream", "stone weight", "top k"],
        "Trie": ["trie", "prefix tree", "word search ii", "autocomplete"],
        "Graphs": ["graph", "island", "islands", "connected components", "topological sort", "dijkstra", "bipartite", "course schedule", "rotting", "flood fill", "shortest path"],
        "Dynamic Programming": ["dynamic programming", "dp", "climbing stairs", "coin change", "longest increasing subsequence", "edit distance", "knapsack", "house robber", "unique paths", "subset sum"]
    }

    PREREQUISITES_MAP = {
        "Arrays": ["Basic Syntax", "Iteration"],
        "Math": ["Basic Arithmetic"],
        "Hashing": ["Arrays", "Hash Functions"],
        "Strings": ["Arrays", "Character Manipulation"],
        "Two Pointers": ["Arrays"],
        "Sliding Window": ["Arrays", "Two Pointers"],
        "Bit Manipulation": ["Binary Representation"],
        "Stack": ["Arrays", "LIFO Principle"],
        "Queue": ["Arrays", "FIFO Principle"],
        "Linked List": ["Pointers", "Memory References"],
        "Binary Search": ["Arrays", "Two Pointers"],
        "Recursion & Backtracking": ["Call Stack", "Recursion Basics"],
        "Greedy": ["Arrays", "Sorting"],
        "Binary Tree": ["Recursion & Backtracking", "Pointers"],
        "Binary Search Tree": ["Binary Tree", "Binary Search"],
        "Heap": ["Binary Tree", "Arrays", "Priority Queues"],
        "Trie": ["Strings", "Trees"],
        "Graphs": ["Queue", "Stack", "Recursion & Backtracking"],
        "Dynamic Programming": ["Recursion & Backtracking", "Memoization", "Subproblems"]
    }

    SIMILAR_CONCEPTS_MAP = {
        "jump game": "Greedy Reachability",
        "maximum units on a truck": "Fractional Knapsack (Greedy by Value/Weight)",
        "single-threaded cpu": "Shortest Job First (Min-Heap Simulation)",
        "best time to buy and sell stock": "Kadane's / Peak-Valley Single Pass",
        "linked list cycle": "Floyd's Tortoise and Hare Cycle Detection",
        "reverse linked list": "Iterative Pointer Reversal",
        "two sum": "HashMap Complement Lookup",
        "3sum": "Two Pointers on Sorted Array",
        "valid parentheses": "LIFO Stack Matching",
        "koko eating bananas": "Binary Search on Answer Space",
        "last stone weight": "Max-Heap Priority Extraction",
        "number of islands": "Grid BFS / Connected Components DFS",
        "course schedule": "Topological Sort / Kahn's Algorithm / Cycle Detection",
        "climbing stairs": "Fibonacci Dynamic Programming",
        "coin change": "Unbounded Knapsack DP",
        "longest increasing subsequence": "Patience Sorting / 1D DP",
        "trapping rain water": "Monotonic Stack / Two Pointers Boundary Check",
        "lru cache": "Doubly Linked List + Hash Map",
        "word search": "Backtracking Matrix DFS",
        "merge intervals": "Sorting + Interval Overlap Merge"
    }

    def __init__(self, known_problems_db: Optional[List[Dict[str, Any]]] = None):
        if known_problems_db is None:
            self.known_problems = self._load_known_problems()
        else:
            self.known_problems = known_problems_db
            
        self.num_map = {}
        self.title_map = {}
        for p in self.known_problems:
            if p.get("leetcode_number"):
                self.num_map[int(p["leetcode_number"])] = p
            if p.get("title"):
                norm = self._norm(p["title"])
                self.title_map[norm] = p

    @staticmethod
    def _norm(text: str) -> str:
        return re.sub(r'[^a-z0-9]', '', str(text).lower())

    def _load_known_problems(self) -> List[Dict[str, Any]]:
        paths = [
            os.path.join(os.path.dirname(__file__), "..", "data", "problems.json"),
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "problems.json")
        ]
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    pass
        return []

    def classify_problem(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw problem dictionary and enriches it with topics, difficulty, similar_concept, prerequisites.
        """
        lc_num = item.get("leetcode_number")
        title = item.get("title", "").strip()
        norm_title = self._norm(title)

        # 1. Check exact match in database
        matched_known = None
        if lc_num and int(lc_num) in self.num_map:
            matched_known = self.num_map[int(lc_num)]
        elif norm_title in self.title_map:
            matched_known = self.title_map[norm_title]

        # Use matched known values if available
        if matched_known:
            title = matched_known.get("title", title)
            slug = matched_known.get("slug") or self._slugify(title)
            difficulty = item.get("difficulty") or matched_known.get("difficulty", "Medium")
            if difficulty not in ["Easy", "Medium", "Hard"]:
                difficulty = matched_known.get("difficulty", "Medium")
            
            topics = item.get("topics") or matched_known.get("topics", ["General"])
            if not topics or topics == ["General"] or topics == [""]:
                topics = matched_known.get("topics", ["General"])

            similar_concept = item.get("similar_concept") or matched_known.get("similar_concept")
            if not similar_concept:
                similar_concept = self._find_similar_concept(title, topics)

            prereqs = matched_known.get("prerequisites") or self.PREREQUISITES_MAP.get(topics[0], ["Basic Programming"])
            estimated_minutes = matched_known.get("estimated_minutes", 20 if difficulty == "Easy" else 35 if difficulty == "Medium" else 55)

            return {
                "leetcode_number": matched_known.get("leetcode_number", lc_num),
                "title": title,
                "slug": slug,
                "difficulty": difficulty,
                "topics": topics,
                "subtopics": matched_known.get("subtopics", [f"{topics[0]} Fundamentals"]),
                "source": item.get("source", "uploaded_document"),
                "description": matched_known.get("description", f"{difficulty} DSA problem covering {topics[0]}."),
                "similar_problems": matched_known.get("similar_problems", [similar_concept] if similar_concept else []),
                "similar_concept": similar_concept,
                "prerequisites": prereqs,
                "estimated_minutes": estimated_minutes,
                "note": item.get("note") or matched_known.get("note", "")
            }

        # 2. Rule-based classification for unknown problems
        slug = self._slugify(title)
        inferred_topics = self._infer_topics_from_text(f"{title} {item.get('raw_text', '')}")
        difficulty = item.get("difficulty", "Medium").capitalize()
        if difficulty not in ["Easy", "Medium", "Hard"]:
            difficulty = "Medium"

        primary_topic = inferred_topics[0] if inferred_topics else "Arrays"
        similar_concept = item.get("similar_concept") or self._find_similar_concept(title, inferred_topics)
        prereqs = self.PREREQUISITES_MAP.get(primary_topic, ["Basic Programming"])
        estimated_minutes = 20 if difficulty == "Easy" else 35 if difficulty == "Medium" else 55

        return {
            "leetcode_number": lc_num,
            "title": title,
            "slug": slug,
            "difficulty": difficulty,
            "topics": inferred_topics if inferred_topics else ["Arrays"],
            "subtopics": [f"{primary_topic} Problem"],
            "source": item.get("source", "uploaded_document"),
            "description": f"{difficulty} DSA problem on {primary_topic}.",
            "similar_problems": [similar_concept] if similar_concept else [],
            "similar_concept": similar_concept,
            "prerequisites": prereqs,
            "estimated_minutes": estimated_minutes,
            "note": item.get("note", "")
        }

    def _infer_topics_from_text(self, text: str) -> List[str]:
        text_lower = text.lower()
        matched = []
        for topic, keywords in self.TOPIC_KEYWORD_MAP.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                    matched.append(topic)
                    break
        return matched if matched else ["Arrays"]

    def _find_similar_concept(self, title: str, topics: List[str]) -> str:
        title_lower = title.lower()
        for key, concept in self.SIMILAR_CONCEPTS_MAP.items():
            if key in title_lower:
                return concept
        if topics:
            return f"Standard {topics[0]} Technique"
        return "Core DSA Pattern"

    @staticmethod
    def _slugify(title: str) -> str:
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        return re.sub(r'[\s_]+', '-', slug).strip('-')
