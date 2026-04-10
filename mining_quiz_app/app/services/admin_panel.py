"""Admin-level reporting and maintenance actions."""

from __future__ import annotations

from app.database.db import Database


class AdminService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def dashboard_summary(self) -> dict:
        total_users = self.db.fetchone("SELECT COUNT(*) AS c FROM users")
        active_users = self.db.fetchone("SELECT COUNT(DISTINCT user_id) AS c FROM quiz_results")
        top_scores = self.db.fetchall(
            """
            SELECT u.name, u.user_id, SUM(q.score) AS score
            FROM quiz_results q
            JOIN users u ON u.id = q.user_id
            GROUP BY u.id
            ORDER BY score DESC
            LIMIT 5
            """
        )
        hard_questions = self.db.fetchall(
            """
            SELECT topic, question_text, COUNT(*) AS wrongs
            FROM quiz_results
            JOIN json_each(quiz_results.wrong_topics)
            JOIN questions ON questions.topic = json_each.value
            GROUP BY questions.id
            ORDER BY wrongs DESC
            LIMIT 5
            """
        )
        return {
            "total_users": total_users["c"] if total_users else 0,
            "active_users": active_users["c"] if active_users else 0,
            "top_scores": [dict(row) for row in top_scores],
            "most_difficult": [dict(row) for row in hard_questions],
        }

    def log_action(self, admin_id: int, action: str, payload: dict | None = None) -> None:
        self.db.execute(
            "INSERT INTO admin_logs(admin_id, action, payload, created_at) VALUES (?, ?, ?, ?)",
            (admin_id, action, self.db.dumps(payload or {}), self.db.now()),
        )
