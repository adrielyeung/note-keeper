import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    """Test  that get_db returns the same database everytime """
    with app.app_context():
        db = get_db()
        assert db is get_db()  # Same database obtained

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')  # 1 = True so returns True

    assert 'closed' in str(e)  # Whether databse is closed after connection (get_db)


def test_init_db_command(runner, monkeypatch):
    """Tests whether (fake_)init_db is called with init-db command (initialise databse).
        Uses monkeypatch fixture to call fake_int_db function instead of init_db, and
        result of whether it's called is recorded into the Recorder object."""
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output  # Checks whether
    assert Recorder.called
