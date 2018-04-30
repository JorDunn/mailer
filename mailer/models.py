from pony.orm import Required, Optional, PrimaryKey
from .app import pony
import datetime
import time
from nacl.pwhash import scrypt
from jose import jwt
from .config import Config

db = pony.db


class Customers(db.Entity):

    _table_ = 'customers'

    customer_id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    email = Required(str, unique=True)
    phone_number = Required(int)


class Devices(db.Entity):

    _table_ = 'devices'

    device_id = PrimaryKey(int, auto=True)
    customer_id = Required(int)
    make = Required(str)
    model = Required(str)
    repair = Required(str)
    emailed = Required(bool)


class Queue(db.Entity):

    _table_ = 'queue'

    customer_id = Required(int)
    device_id = Required(int)


class Franchise(db.Entity):

    _table_ = 'franchise'

    franchise_id = PrimaryKey(int, auto=True)
    name = Required(str)


class Users(db.Entity):

    _table_ = 'users'

    user_id = PrimaryKey(int, auto=True)
    first_name = Required(str)
    last_name = Required(str)
    username = Required(str)
    password = Required(bytes)
    is_admin = Required(bool)


class Sessions(db.Entity):

    _table_ = 'sessions'

    session_id = PrimaryKey(int, auto=True)
    token = Required(str, unique=True)
    expires = Required(datetime.date)


class CustomerManager(object):

    def add_customer(self):
        pass

    def remove_customer(self, customer_id):
        pass

    def update_customer(self, customer_id):
        pass


class DeviceManager(object):

    def add_device(self, customer_id):
        pass

    def remove_device(self, device_id):
        pass

    def update_device(self, device_id):
        pass


class QueueManager(object):

    def add_customer(self):
        pass

    def remove_customer(self, customer_id):
        pass

    def update_customer(self, customer_id):
        pass


class FranchiseManager(object):

    def add_franchisee(self):
        pass

    def remove_franchisee(self, franchise_id):
        pass

    def update_franchisee(self, franchise_id):
        pass


class UserManager(object):

    @staticmethod
    def add_user(first_name, last_name, username, password, is_admin):
        try:
            Users(first_name=first_name, last_name=last_name,
                  username=username, password=scrypt.str(password.encode()),
                  is_admin=is_admin)
            return True
        except:
            return False

    @staticmethod
    def remove_user(user_id):
        if Users.exists(user_id=user_id):
            try:
                user = Users.get(user_id=user_id)
                user.delete()
            except:
                return False
        else:
            return False

    @staticmethod
    def update_user(user_id, password, is_admin):
        try:
            user = Users.get(user_id=user_id)
            user.password = scrypt.str(password).encode()
            user.is_admin = is_admin
            return True
        except:
            return False

    @staticmethod
    def login(username, password):
        user = Users.get(username=username)
        if scrypt.verify(user.password, password.encode()):
            try:
                token = SessionManager.add_session(user.user_id)
                return True, token
            except:
                return False
        else:
            return False

    @staticmethod
    def logout(token):
        if Sessions.exists(token=token):
            try:
                SessionManager.remove_session(token)
                return True
            except:
                return False
        else:
            return False


class SessionManager(object):

    @staticmethod
    def add_session(user_id):
        collision = False
        while collision is True:
            current_time = datetime.datetime.now()
            future_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            expiration = time.mktime(future_time.timetuple())
            payload = {'user_id': user_id, 'exp': future_time,
                       'nbf': current_time, 'iss': 'mailer',
                       'iat': current_time}
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS512')
            if Sessions.exists(token=token):
                collision = True
            else:
                try:
                    # Yes, I know that expires could be even further into the future
                    Sessions(token=token, expires=future_time)
                    return True
                except:
                    return False

    @staticmethod
    def remove_session(token):
        pass

    @staticmethod
    def verify_session(user_id, token):
        pass
