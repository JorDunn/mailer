from pony.orm import PrimaryKey, Required, db_session

from mailer.models import db


class Franchisees(db.Entity):

    _table_ = 'franchisees'

    franchise_id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)


class FranchiseManager(object):

    @classmethod
    @db_session
    def add_franchise(cls, name):
        if Franchisees.exists(name=name):
            return False
        else:
            try:
                Franchisees(name=name)
                return True
            except Exception as e:
                print(e)
                return False

    @classmethod
    @db_session
    def remove_franchise(cls, franchise_id):
        if Franchisees.exists(franchise_id=franchise_id):
            try:
                franchise = Franchisees.get(franchise_id=franchise_id)
                franchise.delete()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def update_franchise(cls, franchise_id, name):
        if Franchisees.exists(franchise_id=franchise_id):
            try:
                franchise = Franchisees.get(franchise_id=franchise_id)
                franchise.name = name
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def get_franchise(cls, franchise_id: int):
        pass
