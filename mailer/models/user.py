from nacl.pwhash import scrypt

from mailer.models import db

from flask_login import UserMixin
from pony.orm import PrimaryKey, Required, db_session


class User(db.Entity, UserMixin):

    _table_ = 'user'

    uid = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    username = Required(str, unique=True)
    password = Required(bytes)
    role = Required(int)

    def get_id(self):
        return self.uid

    @classmethod
    def add_user(cls, first_name, last_name, username, password, role):
        with db_session:
            try:
                if User.exists(username=username):
                    return False
                else:
                    User(first_name=first_name, last_name=last_name,
                         username=username, password=scrypt.str(password.encode()), role=role)
                    return True
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

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Role(db.Entity):

    _table_ = 'role'

    rid = PrimaryKey(int, auto=True)
    uid = Required(int)
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
    def get_permissions(self, user_id):
        pass

    @classmethod
    def update_permissions(self, user_id, **kwargs):
        pass
