"""Main dashboard window with quiz, analytics, leaderboard and admin views."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.models.constants import MINING_TOPICS, QUIZ_TYPES, SUBJECTS
from app.services.admin_panel import AdminService
from app.services.analytics import AnalyticsService
from app.services.leaderboard import LeaderboardService
from app.services.question_manager import QuestionManager
from app.services.quiz_engine import QuizEngine
from app.ui.theme import DARK_THEME, LIGHT_THEME


class MainWindow(QMainWindow):
    def __init__(
        self,
        user,
        quiz_engine: QuizEngine,
        leaderboard_service: LeaderboardService,
        analytics_service: AnalyticsService,
        admin_service: AdminService,
        question_manager: QuestionManager,
    ):
        super().__init__()
        self.user = user
        self.quiz_engine = quiz_engine
        self.leaderboard_service = leaderboard_service
        self.analytics_service = analytics_service
        self.admin_service = admin_service
        self.question_manager = question_manager
        self.is_dark_mode = False

        self.setWindowTitle(f"Mining Exam Prep - {user.name}")
        self.resize(1200, 760)
        self._build()

    def _build(self):
        shell = QWidget()
        layout = QHBoxLayout(shell)
        self.nav = QListWidget()
        self.nav.addItems(["Dashboard", "Take Quiz", "Analytics", "Leaderboard", "Admin"])
        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)

        self.pages = QStackedWidget()
        self.pages.addWidget(self._dashboard_page())
        self.pages.addWidget(self._quiz_page())
        self.pages.addWidget(self._analytics_page())
        self.pages.addWidget(self._leaderboard_page())
        self.pages.addWidget(self._admin_page())

        layout.addWidget(self.nav, 1)
        layout.addWidget(self.pages, 4)
        self.setCentralWidget(shell)
        self.nav.setCurrentRow(0)

    def _dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        card = QFrame(objectName="card")
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(QLabel(f"Welcome, {self.user.name} ({self.user.role})"))
        card_layout.addWidget(QLabel("Prepare for Mining and competitive examinations with smart practice."))

        theme_btn = QPushButton("Toggle Dark/Light Mode")
        theme_btn.clicked.connect(self._toggle_theme)
        card_layout.addWidget(theme_btn)

        layout.addWidget(card)
        return page

    def _quiz_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        form = QFormLayout()

        self.quiz_type = QComboBox()
        self.quiz_type.addItems(QUIZ_TYPES)
        self.subject = QComboBox()
        self.subject.addItems(["Mixed"] + SUBJECTS)
        self.topic = QComboBox()
        self.topic.addItems(["Any"] + MINING_TOPICS)
        self.question_limit = QSpinBox()
        self.question_limit.setRange(5, 100)
        self.question_limit.setValue(25)

        form.addRow("Test type", self.quiz_type)
        form.addRow("Subject", self.subject)
        form.addRow("Topic", self.topic)
        form.addRow("Questions", self.question_limit)

        start_btn = QPushButton("Start Mock Test")
        start_btn.clicked.connect(self._start_quiz)
        self.quiz_output = QTextEdit()
        self.quiz_output.setReadOnly(True)

        layout.addLayout(form)
        layout.addWidget(start_btn)
        layout.addWidget(self.quiz_output)
        return page

    def _analytics_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        refresh_btn = QPushButton("Refresh Analytics")
        refresh_btn.clicked.connect(self._refresh_analytics)
        self.analytics_text = QTextEdit()
        self.analytics_text.setReadOnly(True)
        layout.addWidget(refresh_btn)
        layout.addWidget(self.analytics_text)
        return page

    def _leaderboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        refresh_btn = QPushButton("Refresh Leaderboard")
        refresh_btn.clicked.connect(self._refresh_leaderboard)
        self.leaderboard_text = QTextEdit()
        self.leaderboard_text.setReadOnly(True)
        layout.addWidget(refresh_btn)
        layout.addWidget(self.leaderboard_text)
        return page

    def _admin_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.admin_text = QTextEdit()
        self.admin_text.setReadOnly(True)

        refresh_btn = QPushButton("Refresh Admin Dashboard")
        refresh_btn.clicked.connect(self._refresh_admin)
        add_sample_btn = QPushButton("Seed Sample Mining Question")
        add_sample_btn.clicked.connect(self._add_sample_question)

        layout.addWidget(refresh_btn)
        layout.addWidget(add_sample_btn)
        layout.addWidget(self.admin_text)
        return page

    def _toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.setStyleSheet(DARK_THEME if self.is_dark_mode else LIGHT_THEME)

    def _start_quiz(self):
        subject = None if self.subject.currentText() == "Mixed" else self.subject.currentText()
        topic = None if self.topic.currentText() == "Any" else self.topic.currentText()
        questions = self.quiz_engine.build_test(
            self.quiz_type.currentText(),
            subject=subject,
            topic=topic,
            limit=self.question_limit.value(),
        )
        if not questions:
            QMessageBox.information(self, "No questions", "No approved questions available for this filter.")
            return

        answers = {q["id"]: q["correct_option"] for q in questions[: max(1, len(questions) // 2)]}
        summary = self.quiz_engine.evaluate(questions, answers)
        self.quiz_engine.save_result(self.user.id, self.quiz_type.currentText(), summary, duration_sec=900, subject=subject)
        self.quiz_output.setText(
            "\n".join(
                [
                    f"Generated Questions: {len(questions)}",
                    f"Score: {summary['score']}",
                    f"Correct: {summary['correct_count']}",
                    f"Wrong: {summary['wrong_count']}",
                    f"Accuracy: {summary['accuracy']}%",
                    "(Demo flow auto-submitted with simulated answers)",
                ]
            )
        )

    def _refresh_analytics(self):
        metrics = self.analytics_service.dashboard_metrics(self.user.id)
        self.analytics_text.setText("\n".join(f"{k}: {v}" for k, v in metrics.items()))

    def _refresh_leaderboard(self):
        self.leaderboard_service.refresh(period="all_time")
        rows = self.leaderboard_service.get_top(period="all_time")
        body = [f"{idx+1}. {row['name']} ({row['user_id']}): {row['points']}" for idx, row in enumerate(rows)]
        self.leaderboard_text.setText("\n".join(body) if body else "No leaderboard data")

    def _refresh_admin(self):
        if self.user.role != "admin":
            self.admin_text.setText("Admin permissions required.")
            return
        summary = self.admin_service.dashboard_summary()
        self.admin_text.setText("\n".join(f"{k}: {v}" for k, v in summary.items()))

    def _add_sample_question(self):
        if self.user.role != "admin":
            QMessageBox.warning(self, "Access denied", "Only admin can add questions.")
            return
        qid = self.question_manager.add_question(
            {
                "subject": "Mining Engineering",
                "topic": "Mine Ventilation",
                "difficulty": "medium",
                "question_text": "Which instrument is commonly used to measure airflow in mine ventilation?",
                "option_a": "Anemometer",
                "option_b": "Clinometer",
                "option_c": "Barometer",
                "option_d": "Hydrometer",
                "correct_option": "A",
                "explanation": "An anemometer is used to measure air velocity.",
                "marks": 1,
                "negative_marks": 0.25,
                "time_limit_sec": 60,
                "tags": ["ventilation", "instrumentation"],
                "status": "approved",
            },
            created_by=self.user.id,
        )
        self.admin_text.setText(f"Sample question inserted with ID {qid}")
