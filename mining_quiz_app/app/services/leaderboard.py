"""Leaderboard computation for multiple periods and subjects."""

from __future__ import annotations

from app.database.db import Database


class LeaderboardService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def refresh(self, period: str = "all_time", subject: str | None = None) -> None:
        where_clause = ""
        params: list[object] = []
        if subject:
            where_clause = "WHERE subject = ?"
            params.append(subject)

        rows = self.db.fetchall(
            f"""
            SELECT user_id, SUM(score) AS points
            FROM quiz_results
            {where_clause}
            GROUP BY user_id
            ORDER BY points DESC
            """,
            params,
        )

        for row in rows:
            self.db.execute(
                """
                INSERT INTO leaderboard(user_id, period, subject, points, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (row["user_id"], period, subject, row["points"], self.db.now()),
            )

    def get_top(self, period: str = "all_time", limit: int = 20):
        return self.db.fetchall(
            """
            SELECT l.points, u.name, u.user_id
            FROM leaderboard l
            JOIN users u ON u.id = l.user_id
            WHERE l.period = ?
            ORDER BY l.points DESC
            LIMIT ?
            """,
            (period, limit),
        )
