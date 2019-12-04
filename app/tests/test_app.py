import os
import tempfile

import pytest
from config import Config


@pytest.fixture
def client():
    db_fd, flask.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_login_logout(client):
    """Make sure login and logout works."""

    rv = login(client, config.app.config['USERNAME'], app.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, config.app.config['USERNAME'] + 'x', config.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client, config.app.config['USERNAME'], config.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data

def test_messages(client):
    """Test that messages work."""

    login(client, config.app.config['USERNAME'], config.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data