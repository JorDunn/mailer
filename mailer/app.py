from flask import Flask
from flask_pony import Pony
from mailer import models

app = Flask(__name__, template_folder='templates')
app.config.from_object('config.Config')

pony = Pony(app)
pony.connect()
