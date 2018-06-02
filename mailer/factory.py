from getpass import getpass

from flask import Flask, render_template
from pony.orm import commit, db_session, commit

from mailer.config import Config
from mailer.extensions import csrf_protect, db, login_manager


def unauthorized(error):
    return render_template('401.j2', title='Unauthorized')


def page_not_found(error):
    return render_template('404.j2', title='Page not found')


def create_app():
    app = Flask(__name__, template_folder='views', static_folder='static', static_url_path='/')
    app.config.from_object('mailer.config.Config')

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    try:
        db.bind(provider=Config.PONY['provider'],
                user=Config.PONY['user'],
                password=Config.PONY['password'],
                db=Config.PONY['dbname'],
                host=Config.PONY['host'],
                port=Config.PONY['port'])
        db.generate_mapping(create_tables=True)
    except Exception as e:
        print(e)

    installer()

    return app


def register_extensions(app):
    login_manager.init_app(app)
    csrf_protect.init_app(app)
    return None


def register_blueprints(app):
    from mailer.routes import app_routes
    app.register_blueprint(app_routes)
    # app.register_blueprint('mailer.admin_routes.app_routes')
    return None


def register_errorhandlers(app):
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, page_not_found)


def installer():
    with db_session:
        """This is executed the first time mailer is run to setup an admin account"""
        from mailer.models import Installer

        if Installer.exists(installed=True) is False:
            from mailer.models import Group, User, Role

            print("********************************************************")
            print("*                                                      *")
            print("*                  Welcome to Mailer                   *")
            print("*                                                      *")
            print("********************************************************")
            print("Please enter the following info to create an admin user.")
            username = input("username: ")
            password = getpass("password: ")
            email = input("email: ")
            first_name = input("first name: ")
            last_name = input("last name: ")

            admin_group = Group(name='Admin')
            admin_role = Role(name='Admin', is_admin=True,
                              is_group_admin=True, can_add_group_admin=True,
                              can_remove_group_admin=True, is_subgroup_admin=True,
                              can_add_subgroup_admin=True, can_remove_subgroup_admin=True,
                              can_add_templates=True, can_edit_templates=True,
                              can_delete_templates=True, can_add_users=True,
                              can_edit_users=True, can_delete_users=True,
                              can_add_groups=True, can_edit_groups=True,
                              can_delete_groups=True, can_add_subgroups=True,
                              can_edit_subgroups=True, can_delete_subgroups=True,
                              can_add_queue_items=True, can_edit_queue_items=True,
                              can_delete_queue_items=True, can_add_customers=True,
                              can_edit_customers=True, can_delete_customers=True)
            user = User.add(first_name=first_name, last_name=last_name, email=email,
                            username=username, password=password, role=admin_role, group=admin_group)
            admin_group.users.add(User[user.uid])
            admin_role.users.add(User[user.uid])
            Installer(iid=1, installed=True)
            commit()
