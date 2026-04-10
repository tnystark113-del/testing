"""Question bank management with CSV import/export support."""

from __future__ import annotations

import csv
from pathlib import Path

from app.database.db import Database


class QuestionManager:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add_question(self, payload: dict, created_by: int | None = None) -> int:
        return self.db.execute(
            """
            INSERT INTO questions(
                subject, topic, difficulty, question_text,
                option_a, option_b, option_c, option_d,
                correct_option, explanation, marks, negative_marks,
                time_limit_sec, image_path, tags, question_type,
                status, created_by, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["subject"],
                payload["topic"],
                payload.get("difficulty", "medium"),
                payload["question_text"],
                payload["option_a"],
                payload["option_b"],
                payload["option_c"],
                payload["option_d"],
                payload["correct_option"],
                payload.get("explanation", ""),
                payload.get("marks", 1),
                payload.get("negative_marks", 0.25),
                payload.get("time_limit_sec", 60),
                payload.get("image_path"),
                self.db.dumps(payload.get("tags", [])),
                payload.get("question_type", "mcq"),
                payload.get("status", "pending"),
                created_by,
                self.db.now(),
            ),
        )

    def approve_question(self, question_id: int, admin_id: int) -> None:
        self.db.execute(
            "UPDATE questions SET status = 'approved', approved_by = ? WHERE id = ?",
            (admin_id, question_id),
        )

    def search(self, keyword: str = "", subject: str | None = None, topic: str | None = None):
        sql = "SELECT * FROM questions WHERE 1=1"
        params = []
        if keyword:
            sql += " AND question_text LIKE ?"
            params.append(f"%{keyword}%")
        if subject:
            sql += " AND subject = ?"
            params.append(subject)
        if topic:
            sql += " AND topic = ?"
            params.append(topic)
        return self.db.fetchall(sql + " ORDER BY id DESC", params)

    def import_from_csv(self, file_path: Path, created_by: int | None = None) -> int:
        inserted = 0
        with file_path.open("r", encoding="utf-8") as csv_file:
            for row in csv.DictReader(csv_file):
                self.add_question(row, created_by=created_by)
                inserted += 1
        return inserted

    def export_to_csv(self, output_path: Path) -> Path:
        rows = self.db.fetchall("SELECT * FROM questions ORDER BY id")
        if not rows:
            output_path.write_text("", encoding="utf-8")
            return output_path

        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
        return output_path
