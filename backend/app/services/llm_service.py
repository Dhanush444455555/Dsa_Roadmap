import os
import json
import re
from typing import Dict, Any, Optional, List
import httpx
from ..schemas.dsa_schemas import LLMProblemExtraction

class LLMService:
    """
    Optional LLM service for enriching messy problem descriptions or extracting concepts.
    Uses environment variable LLM_API_KEY or GEMINI_API_KEY or OPENAI_API_KEY.
    Strictly returns structured JSON and validates with Pydantic.
    Gracefully falls back when API key is missing or fails.
    """

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

    def is_available(self) -> bool:
        return bool(self.gemini_key or self.openai_key)

    async def analyze_problem_with_llm(self, raw_input: str) -> Optional[LLMProblemExtraction]:
        """
        Structured prompt asking LLM to return strictly JSON according to requirements:
        {
          "leetcode_number": 1710,
          "title": "Maximum Units on a Truck",
          "difficulty": "Easy",
          "topics": ["Greedy", "Sorting"],
          "subtopics": ["Greedy by value"],
          "similar_concept": "Fractional Knapsack",
          "prerequisites": ["Arrays", "Sorting"]
        }
        """
        if not self.is_available():
            return None

        prompt = f"""You are a DSA problem classifier. Analyze this LeetCode problem input:
"{raw_input}"

Return ONLY a valid JSON object with these exact keys:
{{
  "leetcode_number": <number or null>,
  "title": "<exact problem title>",
  "difficulty": "<Easy | Medium | Hard>",
  "topics": ["<Main Topic>", "<Secondary Topic>"],
  "subtopics": ["<Specific pattern/subtopic>"],
  "similar_concept": "<Famous classic algorithm or similar problem>",
  "prerequisites": ["<Prerequisite concepts>"]
}}
Do NOT output markdown or backticks, output pure JSON only."""

        # Attempt Gemini API if key is present
        if self.gemini_key:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "responseMimeType": "application/json",
                            "temperature": 0.1
                        }
                    }
                    response = await client.post(url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        text_res = data["candidates"][0]["content"]["parts"][0]["text"]
                        clean_json = self._extract_json_str(text_res)
                        parsed = json.loads(clean_json)
                        return LLMProblemExtraction(**parsed)
            except Exception as e:
                print(f"Gemini API call failed: {e}")

        # Attempt OpenAI API if key is present
        if self.openai_key:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    headers = {"Authorization": f"Bearer {self.openai_key}"}
                    payload = {
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": "You are a DSA expert that outputs strict JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.1
                    }
                    response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        text_res = data["choices"][0]["message"]["content"]
                        clean_json = self._extract_json_str(text_res)
                        parsed = json.loads(clean_json)
                        return LLMProblemExtraction(**parsed)
            except Exception as e:
                print(f"OpenAI API call failed: {e}")

        return None

    @staticmethod
    def _extract_json_str(text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
        return text.strip()
