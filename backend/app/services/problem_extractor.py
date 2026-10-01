import re
import json
import os
from typing import List, Dict, Any, Optional, Tuple

class ProblemExtractor:
    """
    Extracts LeetCode problems from raw text, lists, or structured CSV tables.
    Normalizes problem numbers, titles, and tags.
    """

    def __init__(self, known_problems_db: Optional[List[Dict[str, Any]]] = None):
        if known_problems_db is None:
            self.known_problems = self._load_known_problems()
        else:
            self.known_problems = known_problems_db
            
        # Fast lookup indices
        self.num_to_problem = {}
        self.title_to_problem = {}
        for p in self.known_problems:
            if p.get("leetcode_number"):
                self.num_to_problem[int(p["leetcode_number"])] = p
            if p.get("title"):
                norm_title = self._clean_title_for_lookup(p["title"])
                self.title_to_problem[norm_title] = p

    @staticmethod
    def _clean_title_for_lookup(title: str) -> str:
        return re.sub(r'[^a-z0-9]', '', title.lower())

    def _load_known_problems(self) -> List[Dict[str, Any]]:
        paths = [
            os.path.join(os.path.dirname(__file__), "..", "data", "problems.json"),
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "problems.json"),
            os.path.join(os.path.dirname(__file__), "..", "data", "problems.json")
        ]
        for path in paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    pass
        return []

    def extract_from_tabular(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extracts problems from parsed CSV/TSV dictionaries.
        """
        extracted = []
        seen_keys = set()

        for row in rows:
            # Look for number
            lc_num = None
            for key in ["leetcode_number", "leetcode_no", "lc_number", "lc_no", "number", "id", "#"]:
                if key in row and str(row[key]).strip().isdigit():
                    lc_num = int(row[key].strip())
                    break

            # Look for title
            title = ""
            for key in ["title", "problem_name", "problem", "name", "question"]:
                if key in row and row[key].strip():
                    title = row[key].strip()
                    break

            # Look for difficulty
            difficulty = "Medium"
            for key in ["difficulty", "level", "diff"]:
                if key in row and row[key].strip():
                    d_val = row[key].strip().capitalize()
                    if d_val in ["Easy", "Medium", "Hard"]:
                        difficulty = d_val
                        break

            # Look for topic
            topic = "General"
            for key in ["topic", "topics", "category", "tag", "tags"]:
                if key in row and row[key].strip():
                    topic = row[key].strip()
                    break

            # Look for similar concept
            similar_concept = None
            for key in ["similar_concept", "similar_to", "similar", "similar_problems"]:
                if key in row and row[key].strip():
                    similar_concept = row[key].strip()
                    break

            if not title and lc_num and lc_num in self.num_to_problem:
                title = self.known_problems[lc_num].get("title", f"Problem {lc_num}")

            if not title and not lc_num:
                continue

            # Deduplication key
            dedup_key = f"{lc_num}_{self._clean_title_for_lookup(title) if title else ''}"
            if dedup_key in seen_keys:
                continue
            seen_keys.add(dedup_key)

            extracted.append({
                "leetcode_number": lc_num,
                "title": title or f"Problem {lc_num}",
                "difficulty": difficulty,
                "topics": [t.strip() for t in topic.split(",") if t.strip()],
                "similar_concept": similar_concept,
                "source": "uploaded_document"
            })

        return extracted

    def extract_from_raw_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts problem items from unformatted, bulleted, or messy text lines.
        """
        lines = text.split("\n")
        extracted = []
        seen_keys = set()

        # Regex patterns for matching problems
        # Pattern 1: "55 — Jump Game", "121 - Best Time", "141: Linked List Cycle", "1. Two Sum", "206) Reverse Linked List"
        p1 = re.compile(r'^\s*(?:[-*•]\s+)?(\d{1,5})\s*[\s—–\-\:\.\)\]]+\s*(.+)$')
        
        # Pattern 2: "1710 Maximum Units on a Truck" (Number followed by words)
        p2 = re.compile(r'^\s*(?:[-*•]\s+)?(\d{1,5})\s+([A-Za-z].+)$')
        
        # Pattern 3: LeetCode URLs like https://leetcode.com/problems/jump-game/
        p3 = re.compile(r'leetcode\.com/problems/([a-z0-9\-]+)')

        for raw_line in lines:
            line = raw_line.strip()
            if not line or len(line) < 3:
                continue

            lc_num = None
            title = ""
            matched = False

            # Check URL match
            url_match = p3.search(line)
            if url_match:
                slug = url_match.group(1).strip('/')
                # Convert slug to title
                title = " ".join([word.capitalize() for word in slug.split('-')])
                # Check if known
                norm = self._clean_title_for_lookup(title)
                if norm in self.title_to_problem:
                    known = self.title_to_problem[norm]
                    lc_num = known.get("leetcode_number")
                    title = known.get("title", title)
                matched = True

            # Check Pattern 1
            if not matched:
                m1 = p1.match(line)
                if m1:
                    potential_num = int(m1.group(1))
                    potential_title = m1.group(2).strip()
                    # Filter out false positives (e.g. "2026 March" or "10 items")
                    if potential_num < 4000:
                        lc_num = potential_num
                        title = potential_title
                        matched = True

            # Check Pattern 2
            if not matched:
                m2 = p2.match(line)
                if m2:
                    potential_num = int(m2.group(1))
                    potential_title = m2.group(2).strip()
                    if potential_num < 4000 and len(potential_title.split()) >= 1:
                        lc_num = potential_num
                        title = potential_title
                        matched = True

            # Check direct title lookup if line is just a title
            if not matched:
                norm = self._clean_title_for_lookup(line)
                if norm in self.title_to_problem:
                    known = self.title_to_problem[norm]
                    lc_num = known.get("leetcode_number")
                    title = known.get("title", line)
                    matched = True

            if matched and (title or lc_num):
                # Clean up title from trailing parentheses containing difficulty/topic
                cleaned_title, inline_diff, inline_topic = self._clean_extracted_title(title)
                
                # Check known DB to enrich title if needed
                if lc_num and lc_num in self.num_to_problem:
                    known = self.num_to_problem[lc_num]
                    if not cleaned_title or len(cleaned_title) < 3 or cleaned_title.startswith("Problem"):
                        cleaned_title = known.get("title", cleaned_title)

                if not cleaned_title:
                    continue

                dedup_key = f"{lc_num}_{self._clean_title_for_lookup(cleaned_title)}"
                if dedup_key in seen_keys:
                    continue
                seen_keys.add(dedup_key)

                item = {
                    "leetcode_number": lc_num,
                    "title": cleaned_title,
                    "difficulty": inline_diff or "Medium",
                    "topics": [inline_topic] if inline_topic else [],
                    "source": "uploaded_document",
                    "raw_text": line
                }
                extracted.append(item)

        return extracted

    @staticmethod
    def _clean_extracted_title(raw_title: str) -> Tuple[str, Optional[str], Optional[str]]:
        """
        Cleans brackets like "Jump Game (Medium) [Greedy]" into title, difficulty, topic.
        """
        title = raw_title
        diff = None
        topic = None

        # Check for difficulty in parentheses
        for d in ["Easy", "Medium", "Hard"]:
            if re.search(rf'\b{d}\b', title, re.IGNORECASE):
                diff = d
                title = re.sub(rf'\b{d}\b', '', title, flags=re.IGNORECASE)

        # Check for [Topic] or (Topic)
        topic_match = re.search(r'\[(.*?)\]|\((.*?)\)', title)
        if topic_match:
            cand = topic_match.group(1) or topic_match.group(2)
            if cand and len(cand) > 2 and not any(k in cand.lower() for k in ["easy", "medium", "hard"]):
                topic = cand.strip()
            title = re.sub(r'\[(.*?)\]|\((.*?)\)', '', title)

        # Clean trailing punctuation
        title = re.sub(r'[\s—–\-\:\,\.\|\/]+$', '', title).strip()
        title = re.sub(r'^[\s—–\-\:\,\.\|\/]+', '', title).strip()

        return title, diff, topic
