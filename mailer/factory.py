from getpass import getpass

from flask import Flask, current_app, render_template, request, url_for
from pony.orm import db_session

from mailer.config import Config
from mailer.models import db

from pprint import pprint


def unauthorized(error):
    args = request.args
    return render_template('401.j2', title='Unauthorized', token=args['token'])


def page_not_found(error):
    args = request.args
    return render_template('404.j2', title='Page not found', token=args['token'])


def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static', static_url_path='/')
    app.config.from_object('mailer.config.Config')

    from mailer.routes import app_routes
    from mailer.admin_routes import admin_routes
    app.register_blueprint(app_routes)
    app.register_blueprint(admin_routes)

    try:
        db.bind(provider=Config.PONY['provider'], user=Config.PONY['user'],
                password=Config.PONY['password'], db=Config.PONY['dbname'],
                host=Config.PONY['host'], port=Config.PONY['port'])
        db.generate_mapping(create_tables=True)
    except Exception as err:
        print("Already bound to database: ", err)

    installer()

    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, page_not_found)

    return app


@db_session
def installer():
    """This is executed the first time mailer is run to setup an admin account"""
    from mailer.models import Installer
    from mailer.models.users import UserManager
    from mailer.models.franchises import FranchiseManager

    if Installer.exists(installed=True) is False:
        print("********************************************************")
        print("*                                                      *")
        print("*                  Welcome to Mailer                   *")
        print("*                                                      *")
        print("********************************************************")
        print("Please enter the following info to create an admin user.")
        username = input("username: ")
        password = getpass("password: ")
        first_name = input("first name: ")
        last_name = input("last name: ")
        FranchiseManager.add_franchise(name="Null")
        UserManager.add_user(franchise_id=1, username=username, password=password,
                             first_name=first_name, last_name=last_name, is_admin=True)
        Installer(installed=True)
