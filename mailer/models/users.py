from nacl.pwhash import scrypt
from pony.orm import PrimaryKey, Required, db_session

from mailer.models import db
from mailer.models.sessions import SessionManager

from typing import Union

from jose import jwt
from mailer.config import Config

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

    @classmethod
    @db_session
    def add_user(cls, franchise_id: int, first_name: str, last_name: str, username: str, password: str, is_admin: bool) -> Union[None, bool]:
        if Users.exists(username=username) is False:
            try:
                print("Trying to add user...")
                Users(franchise_id=franchise_id, first_name=first_name,
                      last_name=last_name, username=username,
                      password=scrypt.str(password.encode()), is_admin=is_admin)
            except Exception as e:
                print("Failure: {}".format(e))
                return False
        else:
            return False

    @classmethod
    @db_session
    def remove_user(cls, user_id: int) -> bool:
        if Users.exists(user_id=user_id):
            user = Users[user_id]
            user.delete()
            return True
        else:
            return False

    @classmethod
    @db_session
    def update_user(cls, user_id: int, franchise_id: int, first_name: str, last_name: str, password: str, is_admin: bool) -> bool:
        if Users.exists(user_id=user_id):
            try:
                user = Users.get(user_id=user_id)
                user.franchise_id = franchise_id
                user.first_name = first_name
                user.last_name = last_name
                if password:
                    user.password = scrypt.str(password.encode())
                user.is_admin = is_admin
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def validate(cls, username: str, password: str) -> Union[dict, bool]:
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
    def get_user(cls, user_id: int) -> dict:
        try:
            return Users[user_id]
        except Exception as e:
            print(e)
            return False

    @classmethod
    @db_session
    def get_users(cls) -> dict:
        try:
            return Users.select(lambda u: u.user_id > 0)[:]
        except Exception as e:
            print(e)
            return {}

    @classmethod
    @db_session
    def first_run(cls) -> bool or None:
        if Users.exists(username='tuser'):
            return False
        else:
            UserManager.add_user(0, 'Test', 'User', 'tuser', 'testing', True)

    @classmethod
    @db_session
    def admin_verification(cls, token):
        try:
            token_decoded = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256', issuer='mailer')
            if token_decoded['is_admin']:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
