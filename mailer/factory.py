from flask import Flask

from mailer.config import Config

from pony.orm import db_session

from mailer.models import db

from getpass import getpass


def create_app():
    app = Flask(__name__, template_folder='views')
    app.config.from_object('mailer.config.Config')

    from mailer.routes import app_routes
    from mailer.admin_routes import admin_routes
    app.register_blueprint(app_routes)
    app.register_blueprint(admin_routes)

    try:
        db.bind(provider='mysql', user='root', password='flaber', db='mailer')
        db.generate_mapping(create_tables=True)
    except TypeError:
        print("Already bound to database")

    installer()

    return app


@db_session
def installer():
    """This is executed the first time mailer is run to setup an admin account"""
    from mailer.models import Installer
    from mailer.models.users import UserManager
    from mailer.models.franchises import FranchiseManager

    if Installer.exists(installed=True) is False:
        print("Please enter the following info to create an admin user.")
        username = input("username: ")
        password = getpass("password: ")
        first_name = input("first name: ")
        last_name = input("last name: ")
        FranchiseManager.add_franchise(name="Null")
        UserManager.add_user(franchise_id=1, username=username, password=password,
                             first_name=first_name, last_name=last_name, is_admin=True)
        Installer(installed=True)
