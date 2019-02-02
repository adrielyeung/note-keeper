import pytest
from flaskr.db import get_db


# Index / main page
def test_index(client, auth):
    """Tests whether index page has features which should appear, both before and after logging in."""
    response = client.get('/')
    assert b"Log In" in response.data  # Checks for login link
    assert b"Register" in response.data  # Checks for register link

    auth.login()  # Login as test user
    response = client.get('/')
    assert b'Log Out' in response.data  # Checks for logout link
    assert b'test title' in response.data  # Checks for test title in test note
    assert b'by test on 01-01-2018' in response.data  # Checks for username and date in test note
    assert b'test\nbody' in response.data  # Checks for body of note in test note
    assert b'href="/1/update"' in response.data  # Checks for update link in test note
    assert b'href="/1/to_archive' in response.data  # Checks for link to archive test note
    assert b'href="/archive"' in response.data  # Checks for link to archived notes

    auth.logout()  # Checks situation after logging out
    response = client.get('/')
    assert b"Log In" in response.data  # Checks for login link
    assert b"Register" in response.data  # Checks for register link


# Archive page
def test_archive(client, auth, app):
    """Tests whether archived page has features which should appear for logged in users, and redirected to empty index page if logged out."""
    auth.login()  # Login as test user
    response = client.get('/archive')
    assert b'Log Out' in response.data  # Checks for logout link
    # Checks that test note is not archived by checking all features not existing
    assert b'test title' not in response.data  # Checks for test title in test note
    assert b'by test on 01-01-2018' not in response.data  # Checks for username and date in test note
    assert b'test\nbody' not in response.data  # Checks for body of note in test note
    assert b'href="/1/update"' not in response.data  # Checks for update link in test note
    assert b'href="/1/to_archive' not in response.data  # Checks for link to archive test note
    assert b'href="/1/unarchive"' not in response.data  # Checks for link to unarchive test note

    # archive the test note
    client.post('/1/to_archive')
    response_arch = client.get('/archive')

    # Checks that test note is in archived notes
    assert b'test title' in response_arch.data  # Checks for test title in test note
    assert b'by test on 01-01-2018' in response_arch.data  # Checks for username and date in test note
    assert b'test\nbody' in response_arch.data  # Checks for body of note in test note
    assert b'href="/1/update"' in response_arch.data  # Checks for update link in test note
    assert b'href="/1/unarchive"' in response_arch.data  # Checks for link to unarchive test note

    # Checks that test note is not in main (unarchived notes)
    response_main = client.get('/')
    assert b'test title' not in response_main.data  # Checks for test title in test note
    assert b'by test on 01-01-2018' not in response_main.data  # Checks for username and date in test note
    assert b'test\nbody' not in response_main.data  # Checks for body of note in test note
    assert b'href="/1/update"' not in response_main.data  # Checks for update link in test note
    assert b'href="/1/unarchive"' not in response_main.data  # Checks for link to unarchive test note

    auth.logout()  # Checks situation after logging out (from archived page)
    response_out = client.get('/')
    assert b"Log In" in response_out.data  # Checks for login link
    assert b"Register" in response_out.data  # Checks for register link

    auth.login()
    # reset (unarchive the test note)
    client.post('/1/unarchive')
    response_unarch_main = client.get('/')
    assert b'Log Out' in response_unarch_main.data  # Checks for logout link
    assert b'test title' in response_unarch_main.data  # Checks for test title in test note
    assert b'by test on 01-01-2018' in response_unarch_main.data  # Checks for username and date in test note
    assert b'test\nbody' in response_unarch_main.data  # Checks for body of note in test note
    assert b'href="/1/update"' in response_unarch_main.data  # Checks for update link in test note
    assert b'href="/1/to_archive' in response_unarch_main.data  # Checks for link to archive test note
    assert b'href="/archive"' in response_unarch_main.data  # Checks for link to archived notes

    response_unarch_ar = client.get('/archive')
    # Checks that test note is not archived by checking all features not existing
    assert b'test title' not in response_unarch_ar.data  # Checks for test title in test note
    assert b'by test on 01-01-2018' not in response_unarch_ar.data  # Checks for username and date in test note
    assert b'test\nbody' not in response_unarch_ar.data  # Checks for body of note in test note
    assert b'href="/1/update"' not in response_unarch_ar.data  # Checks for update link in test note
    assert b'href="/1/to_archive' not in response_unarch_ar.data  # Checks for link to archive test note
    assert b'href="/1/unarchive"' not in response_unarch_ar.data  # Checks for link to unarchive test note


@pytest.mark.parametrize('path', (
    '/create',
    '/archive',
    '/1/update',
    '/1/delete',
    '/1/to_archive',
    '/1/unarchive',
))
def test_login_required(client, path):
    """Test whether unauthorised access to the above pages is allowed.
        Should redirect to login page if not logged in yet."""
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    """Test whether current user can access another user's notes."""
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't access other user's post
    response = client.get('/')
    assert b'test title' not in response.data  # Checks for test title in test note
    assert b'by test on 01-01-2018' not in response.data  # Checks for username and date in test note
    assert b'test\nbody' not in response.data  # Checks for body of note in test note
    assert b'href="/1/update"' not in response.data  # Checks for update link in test note
    assert b'href="/1/to_archive' not in response.data  # Checks for link to archive test note
    # current user can't modify other user's post
    assert client.post( '/1/update' ).status_code == 403
    assert client.post( '/1/delete' ).status_code == 403


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    """Tests whether a non-existing note returns the required error."""
    auth.login()
    assert client.post(path).status_code == 404  # Not found


# Create
def test_create(client, auth, app):
    """Tests whether new post can be created and number of posts after creation = 2."""
    auth.login()
    assert client.get('/create').status_code == 200  # Can access create page after login
    client.post('/create', data={'title': 'created', 'body': ' '})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2  # number of posts after creation = 2


def test_update(client, auth, app):
    """Tests whether test note can be updated."""
    auth.login()
    assert client.get('/1/update').status_code == 200  # Can access update page after login
    client.post('/1/update', data={'title': 'updated', 'body': ' '})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'  # Check whether title is updated


# Create / update pages
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    """Test whether error message is displayed correctly with no body text, for both create and update pages."""
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Body is required.' in response.data


# Delete
def test_delete(client, auth, app):
    """Test whether test note is successfully deleted."""
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'  # Check whether redirected to index page

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None  # Checks whether post is deleted
