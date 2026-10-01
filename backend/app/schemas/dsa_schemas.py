from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ProblemBase(BaseModel):
    leetcode_number: Optional[int] = None
    title: str
    slug: Optional[str] = None
    difficulty: str = "Medium"
    topics: List[str] = []
    subtopics: List[str] = []
    source: str = "uploaded_document"
    description: Optional[str] = None
    similar_problems: List[str] = []
    similar_concept: Optional[str] = None
    prerequisites: List[str] = []
    estimated_minutes: int = 30
    note: Optional[str] = None

class ProblemCreate(ProblemBase):
    pass

class ProblemResponse(ProblemBase):
    id: Optional[int] = None

class ParsedProblemItem(BaseModel):
    leetcode_number: Optional[int] = None
    title: str
    difficulty: str = "Medium"
    topics: List[str] = []
    subtopics: List[str] = []
    similar_concept: Optional[str] = None
    prerequisites: List[str] = []
    source: str = "uploaded_document"
    raw_text: Optional[str] = None

class ParsedDocumentResponse(BaseModel):
    filename: str
    file_type: str
    total_problems_detected: int
    problems: List[ParsedProblemItem]
    warnings: List[str] = []

class LLMProblemExtraction(BaseModel):
    leetcode_number: Optional[int] = None
    title: str
    difficulty: str = Field(default="Medium", description="Easy, Medium, or Hard")
    topics: List[str] = Field(default=[], description="Main DSA topics e.g. Arrays, Greedy, Dynamic Programming")
    subtopics: List[str] = Field(default=[], description="Subtopics e.g. Greedy by value, Two Pointers")
    similar_concept: Optional[str] = Field(default=None, description="Equivalent concept e.g. Fractional Knapsack")
    prerequisites: List[str] = Field(default=[], description="Prerequisite concepts")

class RoadmapDayProblem(BaseModel):
    id: Optional[int] = None
    roadmap_item_id: Optional[int] = None
    leetcode_number: Optional[int] = None
    title: str
    slug: Optional[str] = None
    difficulty: str
    topic: str
    topics: List[str] = []
    similar_concept: Optional[str] = None
    status: str = "Not Started"
    estimated_minutes: int = 30
    order_in_day: int = 1
    notes: Optional[str] = None

class RoadmapDay(BaseModel):
    day: int
    focus_topic: str
    is_revision: bool = False
    problems: List[RoadmapDayProblem]

class RoadmapWeek(BaseModel):
    week: int
    month: int
    focus: List[str]
    days: List[RoadmapDay]

class RoadmapMonth(BaseModel):
    month: int
    title: str
    focus_topics: List[str]
    weeks: List[int]

class RoadmapConfigRequest(BaseModel):
    user_level: str = "Average"  # Beginner, Average, Advanced
    duration_months: int = 6     # 3, 6, 9, 12, or custom
    target_problem_count: int = 150
    problems: Optional[List[Dict[str, Any]]] = None  # Uploaded or selected problems list
    use_built_in: bool = False
    title: Optional[str] = "My Personalized DSA Roadmap"

class RoadmapResponse(BaseModel):
    id: str
    title: str
    user_level: str
    duration_months: int
    target_problem_count: int
    total_problems: int
    total_weeks: int
    month_breakdown: List[RoadmapMonth]
    weeks: List[RoadmapWeek]
    created_at: Optional[str] = None

class RoadmapItemStatusUpdate(BaseModel):
    status: str  # Not Started, In Progress, Completed, Skipped
    notes: Optional[str] = None

class TopicProgress(BaseModel):
    topic: str
    total: int
    completed: int
    percentage: float
    is_weak: bool = False

class ProgressResponse(BaseModel):
    roadmap_id: str
    total_problems: int
    completed: int
    in_progress: int
    not_started: int
    skipped: int
    completion_percentage: float
    current_streak: int
    estimated_hours_left: float
    topic_breakdown: List[TopicProgress]
    difficulty_breakdown: Dict[str, Dict[str, int]]
    weak_topics: List[str]

class RecommendedProblem(BaseModel):
    id: Optional[int] = None
    leetcode_number: Optional[int] = None
    title: str
    slug: Optional[str] = None
    difficulty: str
    topic: str
    similar_concept: Optional[str] = None
    reason: str

class RecommendationResponse(BaseModel):
    weak_topics: List[str]
    message: str
    recommendations: List[RecommendedProblem]

class RevisionItemResponse(BaseModel):
    id: int
    roadmap_id: str
    problem_id: Optional[int] = None
    leetcode_number: Optional[int] = None
    title: str
    topic: str
    difficulty: str
    similar_concept: Optional[str] = None
    interval_day: int
    due_date: str
    status: str
    is_due_today: bool
    is_overdue: bool
