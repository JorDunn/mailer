from pony.orm import db_session

from flask import flash

from mailer.models import Franchises
from mailer.models.users import UserManager


class FranchiseManager(object):

    @classmethod
    @db_session
    def add_franchise(cls, name: str) -> bool:
        if Franchises.exists(name=name):
            flash("A franchise with that name already exists", 'franchise_error')
            return False
        else:
            try:
                Franchises(name=name)
                return True
            except Exception as err:
                flash("There was an error adding the franchise: {}".format(err), 'franchise_error')
                print(err)
                return False

    @classmethod
    @db_session
    def remove_franchise(cls, franchise_id):
        if Franchises.exists(franchise_id=franchise_id):
            try:
                UserManager.update_franchises(franchise_id=franchise_id)
                franchise = Franchises[franchise_id]
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
        if Franchises.exists(franchise_id=franchise_id):
            try:
                franchise = Franchises[franchise_id]
                franchise.name = name
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    @classmethod
    @db_session
    def get_franchises(cls) -> dict:
        try:
            return Franchises.select(lambda f: f.franchise_id >= 0)[:]
        except Exception as e:
            print(e)
            return {}
