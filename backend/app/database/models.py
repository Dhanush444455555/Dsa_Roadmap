import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    leetcode_number = Column(Integer, index=True, nullable=True)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=True)
    difficulty = Column(String(50), default="Medium")
    topics = Column(Text, default="[]")  # JSON list
    subtopics = Column(Text, default="[]")  # JSON list
    source = Column(String(100), default="built_in")  # built_in, uploaded_document
    description = Column(Text, nullable=True)
    similar_problems = Column(Text, default="[]")  # JSON list
    similar_concept = Column(String(255), nullable=True)
    prerequisites = Column(Text, default="[]")  # JSON list
    estimated_minutes = Column(Integer, default=30)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "leetcode_number": self.leetcode_number,
            "title": self.title,
            "slug": self.slug,
            "difficulty": self.difficulty,
            "topics": json.loads(self.topics) if self.topics else [],
            "subtopics": json.loads(self.subtopics) if self.subtopics else [],
            "source": self.source,
            "description": self.description,
            "similar_problems": json.loads(self.similar_problems) if self.similar_problems else [],
            "similar_concept": self.similar_concept,
            "prerequisites": json.loads(self.prerequisites) if self.prerequisites else [],
            "estimated_minutes": self.estimated_minutes,
            "note": self.note
        }

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(String(64), primary_key=True, index=True)
    title = Column(String(255), default="Personalized DSA Roadmap")
    user_level = Column(String(50), default="Average")  # Beginner, Average, Advanced
    duration_months = Column(Integer, default=6)
    target_problem_count = Column(Integer, default=150)
    total_problems = Column(Integer, default=0)
    total_weeks = Column(Integer, default=24)
    is_active = Column(Boolean, default=True)
    roadmap_data = Column(Text, nullable=False)  # Full JSON hierarchy
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    items = relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan")

class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    roadmap_id = Column(String(64), ForeignKey("roadmaps.id", ondelete="CASCADE"), index=True)
    problem_id = Column(Integer, nullable=True)
    leetcode_number = Column(Integer, nullable=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True)
    difficulty = Column(String(50), default="Medium")
    topic = Column(String(100), default="General")
    similar_concept = Column(String(255), nullable=True)
    week_number = Column(Integer, default=1)
    day_number = Column(Integer, default=1)
    order_in_day = Column(Integer, default=1)
    status = Column(String(50), default="Not Started")  # Not Started, In Progress, Completed, Skipped
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    roadmap = relationship("Roadmap", back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "roadmap_id": self.roadmap_id,
            "problem_id": self.problem_id,
            "leetcode_number": self.leetcode_number,
            "title": self.title,
            "slug": self.slug,
            "difficulty": self.difficulty,
            "topic": self.topic,
            "similar_concept": self.similar_concept,
            "week_number": self.week_number,
            "day_number": self.day_number,
            "order_in_day": self.order_in_day,
            "status": self.status,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "notes": self.notes
        }

class RevisionItem(Base):
    __tablename__ = "revision_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    roadmap_id = Column(String(64), index=True)
    problem_id = Column(Integer, nullable=True)
    leetcode_number = Column(Integer, nullable=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(100), default="General")
    difficulty = Column(String(50), default="Medium")
    similar_concept = Column(String(255), nullable=True)
    interval_day = Column(Integer, default=2)  # 2, 7, 21
    due_date = Column(Date, nullable=False)
    status = Column(String(50), default="Pending")  # Pending, Completed, Skipped
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "roadmap_id": self.roadmap_id,
            "problem_id": self.problem_id,
            "leetcode_number": self.leetcode_number,
            "title": self.title,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "similar_concept": self.similar_concept,
            "interval_day": self.interval_day,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, default=1)
    current_level = Column(String(50), default="Average")
    duration_months = Column(Integer, default=6)
    target_problems = Column(Integer, default=150)
    has_api_key = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DriveResource(Base):
    __tablename__ = "drive_resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    drive_url = Column(Text, nullable=False)
    contributor = Column(String(100), default="Community Member")
    description = Column(Text, nullable=True)
    category = Column(String(100), default="Formulas & Notes")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "drive_url": self.drive_url,
            "contributor": self.contributor,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else None
        }

