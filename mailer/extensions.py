from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from pony.orm import Database

login_manager = LoginManager()
db = Database()
csrf_protect = CSRFProtect()
