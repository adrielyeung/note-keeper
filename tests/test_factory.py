from flaskr import create_app


def test_config():
    """Test whether config is passed."""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    """Calls test page which prints 'Hello, World!'"""
    response = client.get('/hello')
    assert response.data == b'Hello, World!'