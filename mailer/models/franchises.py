from flask import flash

from mailer.models import Franchises
from mailer.models.users import UserManager


class FranchiseManager(object):

    @classmethod
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
    def remove_franchise(cls, franchise_id: int) -> bool:
        if Franchises.exists(franchise_id=franchise_id):
            try:
                UserManager.update_user_franchises(franchise_id)
                franchise = Franchises[franchise_id]
                franchise.delete()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    def update_franchise(cls, franchise_id: int, name: str) -> bool:
        if Franchises.exists(franchise_id=franchise_id):
            try:
                franchise = Franchises[franchise_id]
                franchise.name = name
                return True
            except Exception as err:
                print(err)
                return False
        else:
            return False

    @classmethod
    def get_franchises(cls) -> dict:
        try:
            return Franchises.select(lambda f: f.franchise_id >= 0)[:]
        except Exception as err:
            print(err)
            return {}
