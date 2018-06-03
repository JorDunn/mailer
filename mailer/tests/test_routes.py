from datetime import datetime

import pytest

from mailer.extensions import db
from mailer.factory import create_app
from mailer.models import (Customer, Group, Queue, Role, Subgroup, Template,
                           User)


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    app.config['WTF_CSRF_METHODS'] = []
    return app.test_client()


def setUp():
    group = Group(name='TestAdminGroup', email_mask='tuser@example.com', email_username='tuser@example.com',
                  email_password='somepassword', email_host='secure.example.com', email_port=465)
    subgroup = Subgroup(gid=Group, name='TestAdminSubgroup')
    role = Role(name='TestAdmin', is_admin=True,
                is_group_admin=True, can_add_group_admin=True,
                can_remove_group_admin=True, is_subgroup_admin=True,
                can_add_subgroup_admin=True, can_remove_subgroup_admin=True,
                can_add_templates=True, can_edit_templates=True,
                can_delete_templates=True, can_add_users=True,
                can_edit_users=True, can_delete_users=True,
                can_add_groups=True, can_edit_groups=True,
                can_delete_groups=True, can_add_subgroups=True,
                can_edit_subgroups=True, can_delete_subgroups=True,
                can_add_queue_items=True, can_edit_queue_items=True,
                can_delete_queue_items=True, can_add_customers=True,
                can_edit_customers=True, can_delete_customers=True)
    User(first_name='Test', last_name='User',
         email='tuser@example.com', username='testuser',
         password='somepassword', role=role,
         group=group, subgroup=subgroup,
         creation_date=datetime.now())
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
    #    login(app, 'testuser', 'somepassword')
    #    res = app.get('/')
    #    assert res.status_code == 200
    pass


def test_queue(app):
    #    login(app, 'testuser', 'somepassword')
    #    res = app.get('/queue')
    #    assert res.status_code == 200
    pass


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


def test_profile(app):
    pass


def test_profile_edit(app):
    pass
