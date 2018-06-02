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
    User(username='testuser', password='somepassword')
    Template()
    Customer()
    Queue()


def tearDown():
    db.drop_all_tables(with_all_data=True)


def login(app, username, password):
    return app.post('/login', data=dict(username=username, password=password), follow_redirects=True)


def logout(app):
    return app.get('/logout', follow_redirects=True)


def test_login(app):
    """I have to rework the user authentication to catch the error
    that nacl throws if the password is wrong so that I can test for
    wrong usernames and passwords"""
    res = login(app, 'testuser', 'somepassword')
    assert res.status_code == 200


def test_logout(app):
    login(app, 'testuser', 'somepassword')
    res = logout(app)
    assert res.status_code == 200


def test_index(app):
    login(app, 'testuser', 'somepassword')
    res = app.get('/')
    assert res.status_code == 200


def test_queue(app):
    login(app, 'testuser', 'somepassword')
    res = app.get('/queue')
    assert res.status_code == 200


def test_queue_add(app):
    pass


def test_queue_remove(app):
    pass


def test_queue_edit(app):
    pass


def test_customers(app):
    pass


def test_customers_add(app):
    pass


def test_customers_remove(app):
    pass


def test_customers_edit(app):
    pass


def test_templates(app):
    pass


def test_templates_add(app):
    pass


def test_templates_remove(app):
    pass


def test_templates_edit(app):
    pass


def test_groups(app):
    pass


def test_groups_add(app):
    pass


def test_groups_remove(app):
    pass


def test_groups_edit(app):
    pass


def test_subgroups(app):
    pass


def test_subgroups_add(app):
    pass


def test_subgroups_remove(app):
    pass


def test_subgroups_edit(app):
    pass


def test_roles(app):
    pass


def test_roles_add(app):
    pass


def test_roles_remove(app):
    pass


def test_roles_edit(app):
    pass


def test_users(app):
    pass


def test_users_add(app):
    pass


def test_users_remove(app):
    pass


def test_users_edit(app):
    pass
