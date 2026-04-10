"""Login and registration window."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.auth.service import AuthService


class LoginWindow(QWidget):
    def __init__(self, auth_service: AuthService, on_authenticated):
        super().__init__()
        self.auth_service = auth_service
        self.on_authenticated = on_authenticated
        self.setWindowTitle("Mining Exam Prep - Login")
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        title = QLabel("Mining Exam Prep")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")

        form = QFormLayout()
        self.user_id = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.name = QLineEdit()
        self.name.setPlaceholderText("Required only for registration")

        form.addRow("User ID", self.user_id)
        form.addRow("Password", self.password)
        form.addRow("Name", self.name)

        btn_row = QHBoxLayout()
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self._login)
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self._register)
        btn_row.addWidget(login_btn)
        btn_row.addWidget(register_btn)

        root.addWidget(title)
        root.addLayout(form)
        root.addLayout(btn_row)

    def _login(self):
        try:
            user = self.auth_service.login(self.user_id.text().strip(), self.password.text())
        except Exception as exc:
            QMessageBox.warning(self, "Login failed", str(exc))
            return
        self.on_authenticated(user)

    def _register(self):
        name = self.name.text().strip()
        if not name:
            QMessageBox.warning(self, "Registration failed", "Name is required for registration")
            return
        try:
            user = self.auth_service.register(self.user_id.text().strip(), name, self.password.text())
        except Exception as exc:
            QMessageBox.warning(self, "Registration failed", str(exc))
            return
        self.on_authenticated(user)
