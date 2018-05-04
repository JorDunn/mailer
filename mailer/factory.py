from flask import Flask

from mailer.config import Config


def create_app():
    app = Flask(__name__, template_folder='views')
    app.config.from_object('mailer.config.Config')

    from mailer.routes import app_routes
    app.register_blueprint(app_routes)

    from mailer.models import db
    try:
        db.bind(provider='mysql', user='root', password='flaber', db='mailer')
        db.generate_mapping(create_tables=True)
    except TypeError:
        print("Already bound to database")

    return app
