"""Simple light/dark stylesheet helpers."""

LIGHT_THEME = """
QWidget { background-color: #f5f7fb; color: #0f172a; font-family: Segoe UI; }
QPushButton { background-color: #2563eb; color: white; border-radius: 6px; padding: 8px; }
QLineEdit, QComboBox { background: white; border: 1px solid #cbd5e1; border-radius: 6px; padding: 6px; }
QFrame#card { background: white; border-radius: 8px; border: 1px solid #e2e8f0; }
"""

DARK_THEME = """
QWidget { background-color: #0f172a; color: #e2e8f0; font-family: Segoe UI; }
QPushButton { background-color: #1d4ed8; color: white; border-radius: 6px; padding: 8px; }
QLineEdit, QComboBox { background: #1e293b; border: 1px solid #334155; border-radius: 6px; padding: 6px; }
QFrame#card { background: #1e293b; border-radius: 8px; border: 1px solid #334155; }
"""
