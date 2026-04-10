"""Authentication and user account management."""

from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import asdict

from app.database.db import Database
from app.models.entities import User


class AuthService:
    def __init__(self, db: Database) -> None:
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
        return f"{salt.hex()}:{digest.hex()}"

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        salt_hex, digest_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
        return hmac.compare_digest(expected, actual)

    def register(self, user_id: str, name: str, password: str, role: str = "student") -> User:
        existing = self.db.fetchone("SELECT id FROM users WHERE user_id = ?", (user_id,))
        if existing:
            raise ValueError("User ID already exists")

        new_id = self.db.execute(
            """
            INSERT INTO users(user_id, name, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, name, self.hash_password(password), role, self.db.now()),
        )
        return self.get_user_by_id(new_id)

    def login(self, user_id: str, password: str) -> User:
        row = self.db.fetchone("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not row:
            raise ValueError("Invalid credentials")
        if not self.verify_password(password, row["password_hash"]):
            raise ValueError("Invalid credentials")
        return self._row_to_user(row)

    def get_user_by_id(self, user_db_id: int) -> User:
        row = self.db.fetchone("SELECT * FROM users WHERE id = ?", (user_db_id,))
        if not row:
            raise ValueError("User not found")
        return self._row_to_user(row)

    @staticmethod
    def _row_to_user(row) -> User:
        return User(
            id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            role=row["role"],
            total_score=row["total_score"],
        )
