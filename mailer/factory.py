from flask import Flask
from mailer.config import Config


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('mailer.config.Config')

    from mailer.models import db
    try:
        db.bind(provider='mysql', user='root', password='flaber', db='mailer')
        db.generate_mapping(create_tables=True)
    except TypeError:
        print("Already bound to database")

    return app
