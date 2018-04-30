from pony.orm import Required, Optional, PrimaryKey, Database, db_session
import datetime
import time
from nacl.pwhash import scrypt
from jose import jwt
from mailer.config import Config
from mailer.models import db
from mailer.models.sessions import SessionManager


class Users(db.Entity):

    _table_ = 'users'

    user_id = PrimaryKey(int, auto=True)
    franchise_id = Required(int)
    first_name = Required(str)
    last_name = Required(str)
    username = Required(str, unique=True)
    password = Required(bytes)
    is_admin = Required(bool)


class UserManager(object):

    @staticmethod
    @db_session
    def add_user(franchise_id, first_name, last_name, username, password, is_admin):
        if Users.exists(username=username) is False:
            try:
                Users(franchise_id=franchise_id, first_name=first_name,
                      last_name=last_name, username=username,
                      password=scrypt.str(password.encode()), is_admin=is_admin)
            except:
                return False
        else:
            return False

    @classmethod
    @db_session
    def remove_user(cls, user_id):
        if Users.exists(user_id=user_id):
            user = Users.get(user_id=user_id)
            user.delete()
            return True
        else:
            return False

    @classmethod
    @db_session
    def update_user(cls, user_id, password):
        if Users.exists(user_id=user_id):
            try:
                user = Users.get(user_id=user_id)
                user.password = scrypt.str(password.encode())
                return True
            except:
                return False
        else:
            return False

    @classmethod
    @db_session
    def validate(cls, username, password):
        if Users.exists(username=username):
            try:
                user = Users.get(username=username)
                if scrypt.verify(user.password, password.encode()):
                    token = SessionManager.add_session(username, user.is_admin)
                    return token
                else:
                    return False
            except:
                return False
        else:
            return False
