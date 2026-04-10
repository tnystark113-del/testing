"""Performance analytics and chart-ready data generation."""

from __future__ import annotations

from collections import defaultdict

from app.database.db import Database


class AnalyticsService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def dashboard_metrics(self, user_id: int) -> dict:
        rows = self.db.fetchall("SELECT * FROM quiz_results WHERE user_id = ? ORDER BY attempted_at", (user_id,))
        attempted = len(rows)
        if attempted == 0:
            return {
                "tests_attempted": 0,
                "average_score": 0,
                "accuracy": 0,
                "speed_qpm": 0,
                "trend": [],
                "subject_progress": {},
            }

        average_score = sum(row["score"] for row in rows) / attempted
        accuracy = sum(row["accuracy"] for row in rows) / attempted
        speed_qpm = sum(row["speed_qpm"] for row in rows) / attempted
        trend = [{"attempted_at": row["attempted_at"], "score": row["score"]} for row in rows]

        subject_points = defaultdict(float)
        for row in rows:
            subject_points[row["subject"] or "Mixed"] += row["score"]

        return {
            "tests_attempted": attempted,
            "average_score": round(average_score, 2),
            "accuracy": round(accuracy, 2),
            "speed_qpm": round(speed_qpm, 2),
            "trend": trend,
            "subject_progress": dict(subject_points),
        }
