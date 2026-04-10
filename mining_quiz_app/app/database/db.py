"""SQLite database setup and repository helpers."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from app.config import DB_PATH


class Database:
    """Low-level database wrapper for schema initialization and CRUD operations."""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def initialize(self) -> None:
        with self.connection() as conn:
            conn.executescript(
                """
                PRAGMA foreign_keys = ON;
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'student',
                    profile_photo TEXT,
                    total_score REAL DEFAULT 0,
                    subject_points TEXT DEFAULT '{}',
                    rank INTEGER DEFAULT 0,
                    badges TEXT DEFAULT '[]',
                    achievements TEXT DEFAULT '[]',
                    bookmarked_questions TEXT DEFAULT '[]',
                    weak_topics TEXT DEFAULT '[]',
                    performance_trend TEXT DEFAULT '[]',
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_option TEXT NOT NULL,
                    explanation TEXT,
                    marks REAL DEFAULT 1,
                    negative_marks REAL DEFAULT 0.25,
                    time_limit_sec INTEGER DEFAULT 60,
                    image_path TEXT,
                    tags TEXT DEFAULT '[]',
                    question_type TEXT DEFAULT 'mcq',
                    status TEXT DEFAULT 'approved',
                    created_by INTEGER,
                    approved_by INTEGER,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (created_by) REFERENCES users(id),
                    FOREIGN KEY (approved_by) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    quiz_type TEXT NOT NULL,
                    subject TEXT,
                    score REAL NOT NULL,
                    correct_count INTEGER NOT NULL,
                    wrong_count INTEGER NOT NULL,
                    accuracy REAL NOT NULL,
                    speed_qpm REAL DEFAULT 0,
                    duration_sec INTEGER NOT NULL,
                    rank_at_time INTEGER DEFAULT 0,
                    wrong_topics TEXT DEFAULT '[]',
                    attempted_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    period TEXT NOT NULL,
                    subject TEXT,
                    points REAL NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS badges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    xp_value INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS bookmarked_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE (user_id, question_id),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                );

                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS admin_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    payload TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (admin_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    category TEXT NOT NULL,
                    is_read INTEGER DEFAULT 0,
                    trigger_at TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                """
            )

    def execute(self, query: str, params: Iterable[Any] = ()) -> int:
        with self.connection() as conn:
            cur = conn.execute(query, tuple(params))
            return cur.lastrowid

    def fetchone(self, query: str, params: Iterable[Any] = ()) -> sqlite3.Row | None:
        with self.connection() as conn:
            return conn.execute(query, tuple(params)).fetchone()

    def fetchall(self, query: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
        with self.connection() as conn:
            return conn.execute(query, tuple(params)).fetchall()

    @staticmethod
    def dumps(value: Any) -> str:
        return json.dumps(value)

    @staticmethod
    def now() -> str:
        return datetime.utcnow().isoformat()
