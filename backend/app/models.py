import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey, Index, Enum, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    documents = relationship("UploadedDocument", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")
    revision_items = relationship("RevisionQueue", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    timezone = Column(String(64), default="UTC")
    reminder_time = Column(String(10), default="09:00")  # HH:MM format in user's timezone
    paused = Column(Boolean, default=False)
    duration_months = Column(Integer, default=6)
    level = Column(String(32), default="Average")  # Beginner, Average, Advanced
    daily_count = Column(Integer, default=1)  # 1 or 2
    source_type = Column(String(32), default="default")  # default or uploaded
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="settings")


class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(32), nullable=False)  # pdf, docx, csv, xlsx
    parsed_problems = Column(JSON, nullable=True)  # List of {number, title, ...}
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="documents")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, index=True, nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    difficulty = Column(String(32), index=True, nullable=False)  # Easy, Medium, Hard
    topic = Column(String(64), index=True, nullable=False)
    pattern = Column(String(128), nullable=True)
    similar_to = Column(String(255), nullable=True)
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    roadmap_items = relationship("RoadmapItem", back_populates="problem")
    revision_items = relationship("RevisionQueue", back_populates="problem")


class CheatSheet(Base):
    __tablename__ = "cheatsheets"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(64), unique=True, index=True, nullable=False)
    content = Column(JSON, nullable=False)  # Structured JSON cheat sheet
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    duration_months = Column(Integer, nullable=False)
    level = Column(String(32), nullable=False)
    daily_count = Column(Integer, default=1)
    status = Column(String(32), default="active")  # active, completed, archived
    current_day_index = Column(Integer, default=1)
    last_response_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    items = relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapItem.day_index")


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), index=True, nullable=False)
    day_index = Column(Integer, index=True, nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="RESTRICT"), nullable=False)
    is_revision = Column(Boolean, default=False)
    # pending, done, hard, easy, skipped
    status = Column(String(32), default="pending", index=True, nullable=False)
    assigned_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    unlock_at = Column(DateTime, nullable=True)  # Server-side 24-hour cycle enforcement
    tip = Column(Text, nullable=True)  # Concept tip for this specific problem

    roadmap = relationship("Roadmap", back_populates="items")
    problem = relationship("Problem", back_populates="roadmap_items")

    __table_args__ = (
        Index("ix_roadmap_items_roadmap_day", "roadmap_id", "day_index"),
    )


class RevisionQueue(Base):
    __tablename__ = "revision_queue"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String(64), default="too_hard")  # too_hard, skipped, periodic_revision
    added_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved = Column(Boolean, default=False)

    user = relationship("User", back_populates="revision_items")
    problem = relationship("Problem", back_populates="revision_items")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(32), default="reminder")  # reminder, system, achievement
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="notifications")
