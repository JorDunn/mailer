from datetime import datetime

from pony.orm import Database, Required, Optional, PrimaryKey


db = Database()


class Users(db.Entity):

    _table_ = 'users'

    user_id = PrimaryKey(int, auto=True)
    franchise_id = Required(int)
    first_name = Required(str)
    last_name = Required(str)
    username = Required(str, unique=True)
    password = Required(bytes)
    is_admin = Required(bool)


class Franchises(db.Entity):

    _table_ = 'franchises'

    franchise_id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)


class Customers(db.Entity):

    _table_ = 'customers'

    customer_id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    email = Required(str, unique=True)
    phone = Required(str)


class Queue(db.Entity):

    _table_ = 'queue'

    queue_id = PrimaryKey(int, auto=True)
    customer_id = Required(int)


class Sessions(db.Entity):

    _table_ = 'sessions'

    session_id = PrimaryKey(int, auto=True)
    token = Required(str, unique=True)


class Templates(db.Entity):

    _table_ = 'templates'

    template_id = PrimaryKey(int, auto=True)
    name = Required(str)
    body = Required(str)
    added = Required(datetime)
    expires = Optional(datetime)


class Installer(db.Entity):

    _table_ = 'installer'

    installed = Required(bool)
