from typing import Any, Dict, Union

from jose import jwt
from nacl.pwhash import scrypt
from pony.orm import commit

from mailer.config import Config
from mailer.models import Franchises, Users
from mailer.models.sessions import SessionManager


class UserManager(object):

    @classmethod
    def add_user(cls, franchise_id: int, first_name: str, last_name: str, username: str, password: str, is_admin: bool) -> Union[None, bool]:
        if Users.exists(username=username) is False:
            try:
                Users(franchise_id=franchise_id, first_name=first_name.capitalize(),
                      last_name=last_name.capitalize(), username=username.lower(),
                      password=scrypt.str(password.encode()), is_admin=is_admin)
                commit()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    def remove_user(cls, user_id: int) -> bool:
        if Users.exists(user_id=user_id):
            try:
                user = Users[user_id]
                user.delete()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    def update_user(cls, user_id: int, franchise_id: int, first_name: str, last_name: str, password: str, is_admin: bool) -> bool:
        if Users.exists(user_id=user_id):
            try:
                user = Users[user_id]
                user.franchise_id = franchise_id
                user.first_name = first_name
                user.last_name = last_name
                if password:
                    user.password = scrypt.str(password.encode())
                user.is_admin = is_admin
                commit()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    def validate(cls, username: str, password: str) -> Union[dict, bool]:
        if Users.exists(username=username):
            try:
                user = Users.get(username=username)
                if scrypt.verify(user.password, password.encode()):
                    return SessionManager.add_session(username, user.is_admin)
                else:
                    return False
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    def get_user(cls, user_id: int) -> dict:
        if Users.exists(user_id=user_id):
            try:
                return Users[user_id]
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    def get_users(cls) -> dict:
        try:
            data: Dict(str, Any) = {}
            for u in Users.select(lambda u: u.user_id > 0):
                for f in Franchises.select(lambda f: f.franchise_id == u.franchise_id):
                    data[u.user_id] = {'user_id': u.user_id,
                                       'franchise_id': f.franchise_id,
                                       'franchise_name': f.name,
                                       'username': u.username,
                                       'first_name': u.first_name,
                                       'last_name': u.last_name,
                                       'is_admin': u.is_admin}
            return data
        except Exception as err:
            print(err)
            return {}

    @classmethod
    def admin_verification(cls, token):
        try:
            token_decoded = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256', issuer='mailer')
            if token_decoded['is_admin']:
                return True
            else:
                return False
        except Exception as err:
            print(err)
            return False

    @classmethod
    def update_user_franchises(cls, franchise_id):
        try:
            users = Users.select(lambda u: u.franchise_id == franchise_id)
            for user in users:
                user.franchise_id = 1
        except Exception as err:
            print(err)
            return False
