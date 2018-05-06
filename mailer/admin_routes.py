from functools import wraps
from pprint import pprint

from flask import Blueprint, flash, redirect, render_template, request
from werkzeug.exceptions import BadRequestKeyError

from mailer.models.customers import CustomerManager
from mailer.models.queue import QueueManager
from mailer.models.sessions import SessionManager
from mailer.models.users import UserManager

admin_routes = Blueprint(__name__, 'admin_routes',
                         url_prefix='/admin')


def login_required(f):
    @wraps(f)
    def decorator(**kwargs):
        try:
            args = request.args
            if SessionManager.validate(args['token']):
                return f(**kwargs)
            else:
                return redirect('/login')
        except BadRequestKeyError:
            return redirect('/login')
    return decorator


@admin_routes.route('/', methods=['GET'])
@login_required
def index():
    args = request.args
    return render_template('index.j2', title="Home", current_link="admin_home", token=args['token'], admin_view=True)


@admin_routes.route('/users', methods=['GET'])
@login_required
def users():
    args = request.args
    return render_template('users.j2', title="Users", current_link="users", token=args['token'], admin_view=True)


@admin_routes.route('/franchises', methods=['GET'])
@login_required
def franchises():
    args = request.args
    return render_template('franchises.j2', title="Franchises", current_link="franchises", token=args['token'], admin_view=True)
