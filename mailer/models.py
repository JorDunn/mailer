from pony.orm import Required, Optional, PrimaryKey, Database
import datetime
import time
from nacl.pwhash import scrypt
from jose import jwt
from mailer.config import Config

db = Database()


class Franchisees(db.Entity):

    _table_ = 'franchisees'

    franchise_id = PrimaryKey(int, auto=True)
    name = Required(str)


class Users(db.Entity):

    _table_ = 'users'

    user_id = PrimaryKey(int, auto=True)
    franchise_id = Required(int)
    first_name = Required(str)
    last_name = Required(str)
    username = Required(str, unique=True)
    password = Required(bytes)
