"""Database backup and restore helpers."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from app.config import BACKUP_DIR, DB_PATH


class BackupService:
    def create_backup(self) -> Path:
        stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"mining_quiz_{stamp}.sqlite"
        shutil.copy2(DB_PATH, backup_path)
        return backup_path

    def restore_backup(self, backup_path: Path) -> None:
        shutil.copy2(backup_path, DB_PATH)
