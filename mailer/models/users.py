import datetime
import time

from jose import jwt
from nacl.pwhash import scrypt
from pony.orm import Database, Optional, PrimaryKey, Required, db_session

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
    def add_user(franchise_id: int, first_name: str, last_name: str, username: str, password: str, is_admin: bool) -> None or bool:
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
    def remove_user(cls, user_id: int) -> bool:
        if Users.exists(user_id=user_id):
            user = Users.get(user_id=user_id)
            user.delete()
            return True
        else:
            return False

    @classmethod
    @db_session
    def update_user(cls, user_id: int, password: str) -> bool:
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
    def validate(cls, username: str, password: str) -> str or bool:
        if Users.exists(username=username):
            try:
                user = Users.get(username=username)
                if scrypt.verify(user.password, password.encode()):
                    return SessionManager.add_session(username, user.is_admin)
                else:
                    return False
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def first_run(cls) -> bool or None:
        if Users.exists(username='tuser'):
            return False
        else:
            UserManager.add_user(0, 'Test', 'User', 'tuser', 'testing', True)

    @classmethod
    @db_session
    def get_users(cls) -> dict:
        pass
