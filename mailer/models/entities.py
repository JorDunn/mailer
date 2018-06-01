from datetime import datetime
from pprint import pprint

from flask_login import UserMixin
from nacl.pwhash import scrypt
from pony.orm import (LongUnicode, Optional, PrimaryKey, Required, Set, commit,
                      db_session, select)

from mailer.extensions import db


class Installer(db.Entity):

    _table_ = 'installer'

    iid = PrimaryKey(int)
    installed = Required(bool)


class User(db.Entity, UserMixin):

    _table_ = 'users'

    uid = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    email = Required(str, unique=True)
    username = Required(str, unique=True)
    password = Required(bytes)
    role = Required('Role')
    group = Required('Group')
    subgroup = Optional('Subgroup')
    creation_date = Required(datetime)
    queue_items = Set('Queue')
    templates = Set('Template')

    def get_id(self):
        return self.uid

    @classmethod
    def add(cls, first_name, last_name, email, username, password, role, group, subgroup=None):
        with db_session:
            try:
                if User.exists(username=username):
                    return False
                else:
                    if subgroup is None:
                        user = User(first_name=first_name, last_name=last_name, email=email,
                                    username=username, password=scrypt.str(password.encode()), role=role, group=group, creation_date=datetime.now())
                        commit()
                        return user
                    else:
                        user = User(first_name=first_name, last_name=last_name, email=email,
                                    username=username, password=scrypt.str(password.encode()), role=role, group=group, creation_date=datetime.now(), subgroup=subgroup)
                        commit()
                        return user
            except Exception as err:
                print(err)
                return False

    @classmethod
    def get_user(cls, **kwargs):
        if 'uid' in kwargs:
            return User[kwargs['uid']]
        elif 'username' in kwargs:
            return User.select(lambda u: u.username == kwargs['username'])
        else:
            return None

    @classmethod
    def authenticate(cls, username, password):
        if User.exists(username=username):
            user = User.get(username=username)
            if scrypt.verify(user.password, password.encode()):
                return user
            else:
                return False
        else:
            return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        role = Role.get_permissions(self.role.rid)
        return role.is_admin

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Role(db.Entity):

    _table_ = 'roles'

    rid = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    users = Set('User')
    is_admin = Required(bool)
    is_group_admin = Required(bool)
    can_add_group_admin = Required(bool)
    can_remove_group_admin = Required(bool)
    is_subgroup_admin = Required(bool)
    can_add_subgroup_admin = Required(bool)
    can_remove_subgroup_admin = Required(bool)
    can_add_templates = Required(bool)
    can_edit_templates = Required(bool)
    can_delete_templates = Required(bool)
    can_add_users = Required(bool)
    can_edit_users = Required(bool)
    can_delete_users = Required(bool)
    can_add_groups = Required(bool)
    can_edit_groups = Required(bool)
    can_delete_groups = Required(bool)
    can_add_subgroups = Required(bool)
    can_edit_subgroups = Required(bool)
    can_delete_subgroups = Required(bool)
    can_add_queue_items = Required(bool)
    can_edit_queue_items = Required(bool)
    can_delete_queue_items = Required(bool)
    can_add_customers = Required(bool)
    can_edit_customers = Required(bool)
    can_delete_customers = Required(bool)

    @classmethod
    def get_permissions(self, rid):
        role = None
        roles = Role.select(lambda r: rid == rid).prefetch()
        for each in roles:
            role = each
        return role

    @classmethod
    def update_permissions(self, user_id, **kwargs):
        pass


class Group(db.Entity):

    _table_ = 'groups'

    gid = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    subgroups = Set('Subgroup')
    users = Set(User)
    email_mask = Optional(str)
    email_username = Optional(str)
    email_password = Optional(str)
    email_host = Optional(str)
    email_port = Optional(int)

    def get_id(self):
        return self.gid

    def __repr__(self):
        return '<Group {}>'.format(self.name)

    def __add__(self, operand):
        # this will allow you to merge subgroups. Users from the right subgroup will be put in the left subgroup.
        pass

    @classmethod
    def get_group(cls, gid):
        group = None
        groups = Group.select(lambda g: gid == gid).prefetch()
        for each in groups:
            group = each
        return group


class Subgroup(db.Entity):

    _table_ = 'subgroups'

    sgid = PrimaryKey(int, auto=True)
    gid = Required(Group)
    name = Required(str, unique=True)
    users = Set(User)
    email_mask = Optional(str)
    email_username = Optional(str)
    email_password = Optional(str)
    email_host = Optional(str)
    email_port = Optional(int)

    def get_id(self):
        return self.sgid

    def __repr__(self):
        return '<Subgroup {}>'.format(self.name)

    def __add__(self, operand):
        # this will allow you to merge subgroups. Users from the right subgroup will be put in the left subgroup.
        pass


class Customer(db.Entity):

    _table_ = 'customers'

    cid = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    email = Required(str, unique=True)
    emailed_on = Required(datetime)
    added_on = Required(datetime)
    queue_item = Optional('Queue')

    @classmethod
    def get_all(cls):
        data = {}
        counter = 0
        for customer in Customer.select(lambda c: c.cid > 0):
            data[counter] = {
                'cid': customer.cid,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'emailed_on': customer.emailed_on,
                'added_on': customer.added_on,
                'queue_item': customer.queue_item
            }
            counter += 1
        return data


class Queue(db.Entity):

    _table_ = 'queue'

    qid = PrimaryKey(int, auto=True)
    customer = Required(Customer, unique=True)
    user = Required(User)
    template = Required('Template')

    @classmethod
    def get_all(cls):
        return Queue.select().prefetch()


class Template(db.Entity):

    _table_ = 'templates'

    tid = PrimaryKey(int, auto=True)
    name = Required(str)
    subject = Required(str)
    body = Required(LongUnicode)
    added_by = Required(User)
    added_on = Required(datetime)
    expires_on = Required(datetime)
    queue_items = Set(Queue)

    @classmethod
    def get_all(cls):
        data = {}
        for template in Template.select(lambda t: t.tid > 0):
            data[template.tid] = {
                'tid': template.tid,
                'name': template.name,
                'subject': template.subject,
                'body': template.body,
                'added_by': template.added_by.username,
                'added_on': template.added_on,
                'expires_on': template.expires_on
            }
        return data
