"""Application bootstrap and dependency wiring."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from app.auth.service import AuthService
from app.database.db import Database
from app.services.admin_panel import AdminService
from app.services.analytics import AnalyticsService
from app.services.leaderboard import LeaderboardService
from app.services.question_manager import QuestionManager
from app.services.quiz_engine import QuizEngine
from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow
from app.ui.theme import LIGHT_THEME


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(LIGHT_THEME)

    db = Database()
    db.initialize()

    auth_service = AuthService(db)
    question_manager = QuestionManager(db)
    quiz_engine = QuizEngine(db)
    leaderboard_service = LeaderboardService(db)
    analytics_service = AnalyticsService(db)
    admin_service = AdminService(db)

    seed_admin(auth_service)

    state = {}

    def on_authenticated(user):
        state["window"] = MainWindow(
            user=user,
            quiz_engine=quiz_engine,
            leaderboard_service=leaderboard_service,
            analytics_service=analytics_service,
            admin_service=admin_service,
            question_manager=question_manager,
        )
        login.hide()
        state["window"].show()

    login = LoginWindow(auth_service, on_authenticated)
    login.show()
    sys.exit(app.exec())


def seed_admin(auth_service: AuthService) -> None:
    try:
        auth_service.register("admin", "Administrator", "admin@123", role="admin")
    except ValueError:
        pass
