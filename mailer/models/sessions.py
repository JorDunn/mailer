import datetime
import time

from jose import jwt
from pony.orm import db_session

from mailer.config import Config
from mailer.models import Sessions


class SessionManager(object):

    @classmethod
    @db_session
    def add_session(cls, username, is_admin):
        try:
            current_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=-1)
            future_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            payload = {'username': username, 'is_admin': is_admin,
                       'exp': future_time, 'nbf': current_time, 'iss': 'mailer'}
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
            Sessions(token=token)
            return token
        except Exception as e:
            print(e)
            return False

    @classmethod
    @db_session
    def remove_session(cls, token):
        if Sessions.exists(token=token):
            try:
                session = Sessions.get(token=token)
                session.delete()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def validate(cls, token):
        """Checks to see if a session token is valid still"""
        try:
            token_decoded = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256', issuer='mailer')
            if token_decoded['exp'] <= time.time() or token_decoded['nbf'] >= time.time():
                return False
            else:
                return True
        except Exception as e:
            print(e)
            cls.remove_session(token)
            return False
