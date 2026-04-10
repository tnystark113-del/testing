from app.database.db import Database


def test_database_init(tmp_path):
    db = Database(tmp_path / "test.sqlite")
    db.initialize()
    assert (tmp_path / "test.sqlite").exists()
