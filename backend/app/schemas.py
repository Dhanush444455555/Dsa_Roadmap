from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# --- Auth & User ---
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)
    date_of_birth: date

class UserLogin(BaseModel):
    email: EmailStr
    name: str
    date_of_birth: date

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserSettingsUpdate(BaseModel):
    timezone: Optional[str] = "UTC"
    reminder_time: Optional[str] = "09:00"
    paused: Optional[bool] = False
    duration_months: Optional[int] = 6
    level: Optional[str] = "Average"
    daily_count: Optional[int] = 1
    source_type: Optional[str] = "default"

class UserSettingsOut(BaseModel):
    timezone: str
    reminder_time: str
    paused: bool
    duration_months: int
    level: str
    daily_count: int
    source_type: str

    model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    date_of_birth: Optional[date] = None
    is_active: bool
    created_at: datetime
    settings: Optional[UserSettingsOut] = None

    model_config = ConfigDict(from_attributes=True)

# --- Problems & Cheat Sheets ---
class ProblemOut(BaseModel):
    id: int
    number: int
    title: str
    difficulty: str
    topic: str
    pattern: Optional[str] = None
    similar_to: Optional[str] = None
    url: str

    model_config = ConfigDict(from_attributes=True)

class CheatSheetOut(BaseModel):
    id: int
    topic: str
    content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CheatSheetSummary(BaseModel):
    id: int
    topic: str
    when_to_use: Optional[List[str]] = []
    core_idea: Optional[str] = ""

    model_config = ConfigDict(from_attributes=True)

# --- Roadmap & Items ---
class RoadmapItemOut(BaseModel):
    id: int
    day_index: int
    problem: ProblemOut
    is_revision: bool
    status: str  # pending, done, hard, easy, skipped
    assigned_at: datetime
    completed_at: Optional[datetime] = None
    unlock_at: Optional[datetime] = None
    tip: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class RoadmapOut(BaseModel):
    id: int
    user_id: int
    duration_months: int
    level: str
    daily_count: int
    status: str
    current_day_index: int
    created_at: datetime
    items: List[RoadmapItemOut] = []

    model_config = ConfigDict(from_attributes=True)

class RoadmapGenerateRequest(BaseModel):
    source_type: str = Field(default="default", description="'default' or 'uploaded'")
    document_id: Optional[int] = None
    duration_months: int = Field(default=6, ge=1, le=36)
    level: str = Field(default="Average", description="'Beginner', 'Average', 'Advanced'")
    daily_count: int = Field(default=1, ge=1, le=2)
    timezone: str = Field(default="UTC")
    reminder_time: str = Field(default="09:00")

class ProblemActionRequest(BaseModel):
    roadmap_item_id: int
    action: str = Field(..., description="'done', 'hard', 'easy', 'skip'")

class TodayViewOut(BaseModel):
    current_day: int
    total_days: int
    items: List[RoadmapItemOut]
    can_advance: bool
    next_unlock_at: Optional[datetime] = None
    revision_count: int = 0
    all_done_today: bool = False

# --- Notifications ---
class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
