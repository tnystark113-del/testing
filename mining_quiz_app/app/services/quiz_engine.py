"""Quiz assembly, scoring, and persistence."""

from __future__ import annotations

import random
from typing import Iterable

from app.database.db import Database


class QuizEngine:
    def __init__(self, db: Database) -> None:
        self.db = db

    def build_test(self, quiz_type: str, subject: str | None = None, topic: str | None = None, limit: int = 25):
        sql = "SELECT * FROM questions WHERE status = 'approved'"
        params: list[object] = []
        if subject:
            sql += " AND subject = ?"
            params.append(subject)
        if topic:
            sql += " AND topic = ?"
            params.append(topic)
        sql += " ORDER BY RANDOM() LIMIT ?"
        params.append(limit)
        questions = [dict(row) for row in self.db.fetchall(sql, params)]

        for question in questions:
            options = [
                ("A", question["option_a"]),
                ("B", question["option_b"]),
                ("C", question["option_c"]),
                ("D", question["option_d"]),
            ]
            random.shuffle(options)
            question["shuffled_options"] = options

        return questions

    def evaluate(self, questions: Iterable[dict], answers: dict[int, str]):
        score = 0.0
        correct = 0
        wrong = 0
        wrong_topics: list[str] = []

        for question in questions:
            user_choice = answers.get(question["id"])
            if user_choice is None:
                continue
            if user_choice == question["correct_option"]:
                score += float(question["marks"])
                correct += 1
            else:
                score -= float(question["negative_marks"])
                wrong += 1
                wrong_topics.append(question["topic"])

        attempted = correct + wrong
        accuracy = (correct / attempted * 100.0) if attempted else 0.0
        return {
            "score": round(score, 2),
            "correct_count": correct,
            "wrong_count": wrong,
            "accuracy": round(accuracy, 2),
            "wrong_topics": wrong_topics,
        }

    def save_result(self, user_id: int, quiz_type: str, summary: dict, duration_sec: int, subject: str | None = None):
        self.db.execute(
            """
            INSERT INTO quiz_results(
                user_id, quiz_type, subject, score, correct_count, wrong_count,
                accuracy, speed_qpm, duration_sec, wrong_topics, attempted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                quiz_type,
                subject,
                summary["score"],
                summary["correct_count"],
                summary["wrong_count"],
                summary["accuracy"],
                round((summary["correct_count"] + summary["wrong_count"]) / max(duration_sec / 60, 1), 2),
                duration_sec,
                self.db.dumps(summary.get("wrong_topics", [])),
                self.db.now(),
            ),
        )
