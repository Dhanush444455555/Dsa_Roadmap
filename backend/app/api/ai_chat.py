"""
AI Chat endpoint for DSA Roadmap — uses Google Gemini API (free tier).
Endpoint: POST /api/ai-chat
"""
import os
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["ai-chat"])


class ChatMessage(BaseModel):
    role: str  # "user" or "model"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    problem_context: Optional[dict] = None  # {title, number, topic, difficulty}


class ChatResponse(BaseModel):
    reply: str
    model_used: str


DSA_SYSTEM_PROMPT = """You are an expert DSA (Data Structures & Algorithms) tutor and interview coach.
Your name is "AlgoBot". You help students prepare for technical interviews at top tech companies.

Your expertise covers:
- All major DSA topics: Arrays, Strings, Hashing, Two Pointers, Sliding Window, Stacks, Queues, 
  Linked Lists, Binary Search, Recursion, Backtracking, Trees, BST, Heaps, Greedy, 
  Intervals, Graphs, Dynamic Programming, Tries, Bit Manipulation
- LeetCode problem solving strategies and patterns
- Time/Space complexity analysis (Big-O)
- Interview techniques and approaches
- Debugging and optimizing algorithms

Guidelines:
1. Be concise, clear, and encouraging
2. Explain concepts with examples when needed
3. Give hints rather than full solutions unless asked explicitly
4. Point out patterns (e.g. "this is a sliding window problem")
5. Always mention time and space complexity
6. For code, use Python or preferred language
7. Format code blocks properly
8. Never be condescending — treat the student as a peer

If the user asks about a specific LeetCode problem, help them think through the approach step by step."""


def _get_gemini_client():
    """Initialize Gemini generative AI client."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None, None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=DSA_SYSTEM_PROMPT,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1024,
            }
        )
        return genai, model
    except Exception as e:
        logger.warning(f"Could not initialize Gemini: {e}")
        return None, None


@router.post("/ai-chat", response_model=ChatResponse)
async def ai_chat(req: ChatRequest):
    """
    Chat with the AI DSA tutor using Google Gemini (free tier).
    Supports multi-turn conversation history.
    """
    genai, model = _get_gemini_client()

    # Build user message with optional problem context
    user_message = req.message
    if req.problem_context:
        p = req.problem_context
        context_prefix = (
            f"[Context: I'm working on LeetCode #{p.get('number', '')} "
            f"'{p.get('title', '')}' — {p.get('difficulty', '')} difficulty, "
            f"Topic: {p.get('topic', '')}]\n\n"
        )
        user_message = context_prefix + user_message

    # No API key fallback — rule-based response
    if model is None:
        reply = _rule_based_response(req.message, req.problem_context)
        return ChatResponse(reply=reply, model_used="rule-based-fallback")

    try:
        # Convert history to Gemini format
        history = []
        for msg in (req.history or []):
            history.append({
                "role": msg.role,
                "parts": [msg.content]
            })

        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        reply = response.text

        return ChatResponse(reply=reply, model_used="gemini-1.5-flash")

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        # Graceful fallback
        reply = _rule_based_response(req.message, req.problem_context)
        return ChatResponse(reply=reply, model_used="rule-based-fallback")


def _rule_based_response(message: str, context: Optional[dict] = None) -> str:
    """
    Fallback rule-based DSA assistant when no API key is configured.
    Provides helpful responses for common DSA queries.
    """
    msg = message.lower()

    # Problem-context aware responses
    if context:
        topic = context.get("topic", "").lower()
        title = context.get("title", "")
        difficulty = context.get("difficulty", "Medium")

        if "hint" in msg or "help" in msg or "approach" in msg or "how" in msg:
            hints = {
                "arrays": f"For '{title}': Think about in-place manipulation, prefix sums, or two pointers. Arrays often have O(n) solutions.",
                "hashing": f"For '{title}': Use a HashMap/dict to trade space for time. Store frequencies or complements.",
                "two pointers": f"For '{title}': Place left/right pointers and move them based on a condition. Good for sorted arrays.",
                "sliding window": f"For '{title}': Expand right pointer, shrink left when constraint violated. Track window state.",
                "stack": f"For '{title}': Use a monotonic stack. Push elements, pop when a condition breaks.",
                "binary search": f"For '{title}': Define your search space clearly. Binary search on answer space is powerful.",
                "trees": f"For '{title}': Think recursion — what does each subtree return? DFS (pre/in/post) or BFS?",
                "graphs": f"For '{title}': BFS for shortest path, DFS for connectivity/cycles. Use visited set.",
                "dynamic programming": f"For '{title}': Define dp[i] clearly. Find the recurrence. Bottom-up or top-down?",
                "greedy": f"For '{title}': Sort first, then make locally optimal choices. Prove greedy works.",
            }
            for key, hint in hints.items():
                if key in topic:
                    return f"💡 **Hint for {title}:**\n\n{hint}\n\n> 📝 Add your `GEMINI_API_KEY` to Vercel environment variables to unlock full AI responses!"
            return f"💡 **Hint for {title} ({difficulty}):**\n\nBreak the problem into smaller subproblems. What's the brute force O(n²) approach? Can you optimize it?\n\n> 📝 Add your `GEMINI_API_KEY` to unlock full AI tutor!"

    # General DSA queries
    responses = {
        "time complexity": "⏱️ **Time Complexity Guide:**\n- O(1): Hash lookup\n- O(log n): Binary search\n- O(n): Linear scan\n- O(n log n): Sorting\n- O(n²): Nested loops\n- O(2^n): Subsets/backtracking",
        "space complexity": "💾 **Space Complexity:**\n- O(1): In-place operations\n- O(n): HashMap, stack, recursion depth\n- O(n²): 2D DP table",
        "sliding window": "🪟 **Sliding Window Pattern:**\n```python\nleft = 0\nfor right in range(len(arr)):\n    # expand window\n    while window_invalid:\n        left += 1  # shrink\n    # update answer\n```",
        "two pointer": "👆👆 **Two Pointer Pattern:**\n```python\nleft, right = 0, len(arr)-1\nwhile left < right:\n    if condition: left += 1\n    else: right -= 1\n```",
        "binary search": "🔍 **Binary Search Template:**\n```python\nlo, hi = 0, len(arr)-1\nwhile lo <= hi:\n    mid = (lo + hi) // 2\n    if arr[mid] == target: return mid\n    elif arr[mid] < target: lo = mid+1\n    else: hi = mid-1\n```",
        "dynamic programming": "🧠 **DP Approach:**\n1. Define dp[i] (what does it represent?)\n2. Base case\n3. Transition (recurrence)\n4. Answer (usually dp[n] or max(dp))",
        "graph": "🕸️ **Graph Traversals:**\n- BFS: Shortest path, level order\n- DFS: Connectivity, cycles, paths\n- Dijkstra: Weighted shortest path\n- Union-Find: Connected components",
    }

    for keyword, response in responses.items():
        if keyword in msg:
            return response + "\n\n> 📝 Add your `GEMINI_API_KEY` to Vercel env vars for full AI responses!"

    return (
        "👋 **I'm AlgoBot, your DSA tutor!**\n\n"
        "I can help you with:\n"
        "- 🔍 Problem-solving approaches & hints\n"
        "- ⏱️ Time/Space complexity analysis\n"
        "- 📚 DSA patterns (Sliding Window, Two Pointers, DP...)\n"
        "- 💡 Interview tips & techniques\n\n"
        "**Try asking:**\n"
        "- \"Give me a hint for this problem\"\n"
        "- \"Explain sliding window pattern\"\n"
        "- \"What's the time complexity of binary search?\"\n\n"
        "> 📝 Set `GEMINI_API_KEY` in Vercel environment variables to enable full AI responses!"
    )
