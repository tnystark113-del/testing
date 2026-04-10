# Mining Exam Prep (Windows Desktop Quiz Software)

A modular Python desktop quiz and mock-test platform for mining students and competitive exam preparation.

## Stack
- Python 3.11+
- PyQt6 GUI
- SQLite database
- PyInstaller for `.exe` packaging

## Modules Implemented
- Authentication & profile foundation (`app/auth/service.py`)
- Database schema for users, questions, quizzes, leaderboard, badges, analytics, bookmarks, logs, notifications
- Question management with add/search/approve/import/export
- Quiz engine with random question and option order, negative marking, result storage
- Leaderboard aggregation
- Analytics summary for dashboard metrics and trend data
- Admin dashboard service with usage summaries and logs
- Backup & restore utility
- Export utility (CSV/JSON ready)
- Notification service
- PyQt6 login and dashboard UI (with dark/light theme switch)

## Run locally
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements.txt
python main.py
```

## Build `.exe`
```bash
pyinstaller pyinstaller.spec
```
Output executable is produced under `dist/MiningExamPrep/`.

## Default admin
- User ID: `admin`
- Password: `admin@123`

## Notes on scalability
- Modular service architecture keeps core logic isolated for future AI features:
  - AI question generation
  - AI difficulty analysis
  - recommendation engine
  - personalized study plans
  - cloud sync
