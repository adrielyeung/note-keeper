import pytest
from flask import g, session
from flaskr.db import get_db


# Registering
def test_register(client, app):
    """Tests registration procedures, with username and password. """
    assert client.get('/auth/register').status_code == 200  # 200 = Status OK so loaded register page
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )  # Test with fake data
    assert 'http://localhost/' == response.headers['Location']
    # Tests whether redirected to index page after registration

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None  # Tests whether username in database


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))  # Different inputs for registering
def test_register_validate_input(client, username, password, message):
    """Test registering with different inputs (shown above) of username and password."""
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


# Logging in
def test_login(client, auth):
    """Tests logging in procedures (similar to test_register), with username and password."""
    assert client.get('/auth/login').status_code == 200  # Loaded login page
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'  # Redirected to index page

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'  # Checks user ID and username


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))  # Different inputs for logging in
def test_login_validate_input(auth, username, password, message):
    """Test logging in with different inputs (shown above) of username and password."""
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    """Tests logging out."""
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session  # User_ID should not be stored