"""Export quiz data to CSV and JSON for external reporting."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from app.database.db import Database


class ExportService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def export_user_results_csv(self, user_id: int, output_path: Path) -> Path:
        rows = self.db.fetchall("SELECT * FROM quiz_results WHERE user_id = ? ORDER BY attempted_at", (user_id,))
        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            if rows:
                writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
                writer.writeheader()
                for row in rows:
                    writer.writerow(dict(row))
        return output_path

    def export_user_results_json(self, user_id: int, output_path: Path) -> Path:
        rows = self.db.fetchall("SELECT * FROM quiz_results WHERE user_id = ? ORDER BY attempted_at", (user_id,))
        output_path.write_text(json.dumps([dict(row) for row in rows], indent=2), encoding="utf-8")
        return output_path
