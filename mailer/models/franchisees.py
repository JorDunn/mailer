import datetime
import time

from jose import jwt
from nacl.pwhash import scrypt
from pony.orm import Database, Optional, PrimaryKey, Required

from mailer.config import Config
from mailer.models import db


class Franchisees(db.Entity):

    _table_ = 'franchisees'

    franchise_id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)


class FranchiseManager(object):

    @classmethod
    def add_franchise(cls, name):
        if Franchisees.exists(name=name):
            return False
        else:
            try:
                Franchisees(name=name)
                return True
            except:
                return False

    @classmethod
    def remove_franchise(cls, franchise_id):
        if Franchisees.exists(franchise_id=franchise_id):
            try:
                franchise = Franchisees.get(franchise_id=franchise_id)
                franchise.delete()
                return True
            except:
                return False
        else:
            return False

    @classmethod
    def update_franchise(cls, franchise_id, name):
        if Franchisees.exists(franchise_id=franchise_id):
            try:
                franchise = Franchisees.get(franchise_id=franchise_id)
                franchise.name = name
                return True
            except:
                return False
        else:
            return False
