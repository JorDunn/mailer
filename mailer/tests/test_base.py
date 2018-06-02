from mailer.factory import create_app
from mailer.extensions import db
from mailer.models import User, Role, Group, Subgroup, Template, Customer, Queue
import pytest


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    app.config['WTF_CSRF_METHODS'] = []
    return app.test_client()


def setUp():
    Role()
    Group()
    Subgroup()
    User(username='testuser')
    Template()
    Customer()
    Queue()


def tearDown():
    db.drop_all_tables(with_all_data=True)


def login(app, username, password):
    return app.post('/login', data=dict(username=username, password=password), follow_redirects=True)


def logout(app):
    return app.get('/logout', follow_redirects=True)


def test_login_logout(app):
    """I have to rework the user authentication to catch the error
    that nacl throws if the password is wrong so that I can test for
    wrong usernames and passwords"""
    res = login(app, 'testuser', 'somepassword')
    assert res.status_code == 200
    res = logout(app)
    assert res.status_code == 200


def test_index(app):
    login(app, 'testuser', 'somepassword')
    res = app.get('/')
    assert res.status_code == 200


def test_queue_list(app):
    login(app, 'testuser', 'somepassword')
    res = app.get('/queue')
    assert res.status_code == 200
