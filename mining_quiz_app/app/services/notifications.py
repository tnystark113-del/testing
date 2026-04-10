"""Notification scheduling and retrieval module."""

from app.database.db import Database


class NotificationService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, user_id: int, title: str, body: str, category: str, trigger_at: str | None = None) -> None:
        self.db.execute(
            """
            INSERT INTO notifications(user_id, title, body, category, trigger_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, body, category, trigger_at, self.db.now()),
        )

    def unread_for_user(self, user_id: int):
        return self.db.fetchall(
            "SELECT * FROM notifications WHERE user_id = ? AND is_read = 0 ORDER BY created_at DESC",
            (user_id,),
        )
