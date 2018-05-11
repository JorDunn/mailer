import datetime
import time

from jose import jwt
from nacl.pwhash import scrypt
from pony.orm import Database, Optional, PrimaryKey, Required, db_session, select
from pony.orm.serialization import to_dict, to_json

from mailer.config import Config
from mailer.models import db
from mailer.models.sessions import SessionManager
from pprint import pprint
import json


class Templates(db.Entity):

    _table_ = 'templates'

    template_id = PrimaryKey(int, auto=True)
    name = Required(str)
    body = Required(str)
    added = Required(datetime.datetime)
    expires = Optional(datetime.datetime)


class TemplateManager(object):

    @classmethod
    @db_session
    def add_template(cls, name: str, body: str, expires: str) -> bool:
        try:
            if expires != '':
                Templates(name=name, body=body, added=datetime.datetime.utcnow(), expires=expires)
            else:
                Templates(name=name, body=body, added=datetime.datetime.utcnow())
            return True
        except BaseException as e:
            print("Failure: {}".format(e))
            return False

    @classmethod
    @db_session
    def remove_template(cls, template_id: int) -> bool:
        try:
            if Templates.exists(template_id=template_id):
                tpl = Templates[template_id]
                tpl.delete()
                return True
            else:
                return False
        except BaseException as e:
            print("Failure: {}".format(e))
            return False

    @classmethod
    @db_session
    def update_template(cls, template_id: int, name: str, body: str, expires: str) -> bool:
        try:
            if Templates.exists(template_id=template_id):
                tpl = Templates[template_id]
                tpl.name = name
                tpl.body = body
                if expires != "":
                    tpl.expires = expires
                else:
                    tpl.expires = None
                return True
            else:
                return False
        except BaseException as e:
            print("Failure: {}".format(e))
            return False

    @classmethod
    @db_session
    def get_template(cls, template_id: int) -> dict or bool:
        try:
            if Templates.exists(template_id=template_id):
                return Templates[template_id]
            else:
                return False
        except BaseException as e:
            print("Failure: {}".format(e))
            return False

    @classmethod
    @db_session
    def get_template_list(cls) -> dict or bool:
        try:
            return Templates.select(lambda t: t.template_id > 0)[:]
        except BaseException as e:
            print("Failure: {}".format(e))
            return {}
