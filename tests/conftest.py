import os
import sys
import tempfile

import pytest

sys.path.append('C:/Users/Adriel/PycharmProjects/Notekeeper')
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


# Test app features
@pytest.fixture  # Fixture used to provide a fixed baseline to execute test reliably and repeatedly
def app():
    """Creates app for testing."""
    db_fd, db_path = tempfile.mkstemp()  # Opens a temporary file

    app = create_app({
        'TESTING': True,  # In test mode
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Creates test client to make requests to the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Tests click commands."""
    return app.test_cli_runner()


# Test authentication (login, logout) - make POST request to "login" view with the client (call auth.login)
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
