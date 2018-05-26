from flask import Flask, render_template

from mailer.extensions import login_manager, db, csrf_protect
from mailer.config import Config


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

    db.bind(provider=Config.PONY['provider'],
            user=Config.PONY['user'],
            password=Config.PONY['password'],
            db=Config.PONY['dbname'],
            host=Config.PONY['host'],
            port=Config.PONY['port'])
    db.generate_mapping(create_tables=True)

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
