"""Core domain entities used by services and UI."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class User:
    id: int
    user_id: str
    name: str
    role: str
    total_score: float = 0


@dataclass(slots=True)
class Question:
    id: int
    subject: str
    topic: str
    difficulty: str
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    explanation: str
    marks: float
    negative_marks: float
    time_limit_sec: int
    status: str = "approved"


@dataclass(slots=True)
class QuizResult:
    id: int
    user_id: int
    quiz_type: str
    score: float
    correct_count: int
    wrong_count: int
    accuracy: float
    attempted_at: datetime
    duration_sec: int
    subject: Optional[str] = None
