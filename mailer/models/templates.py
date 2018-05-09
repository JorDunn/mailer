import datetime
import time

from jose import jwt
from nacl.pwhash import scrypt
from pony.orm import Database, Optional, PrimaryKey, Required, db_session

from mailer.config import Config
from mailer.models import db
from mailer.models.sessions import SessionManager


class Templates(db.Entity):

    _table_ = 'templates'

    template_id = PrimaryKey(int, auto=True)
    name = Required(str)
    body = Required(str)
    added = Required(datetime.datetime)
    expires = Required(datetime.datetime)


class TemplateManager(object):

    @classmethod
    @db_session
    def add_template(cls, name: str, body: str):
        pass

    @classmethod
    @db_session
    def remove_template(cls, template_id: int):
        pass

    @classmethod
    @db_session
    def update_template(cls, template_id: int):
        pass

    @classmethod
    @db_session
    def get_template(cls, template_id: int):
        pass
