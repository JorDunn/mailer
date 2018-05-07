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


@admin_routes.route('/users/add', methods=['GET'])
@login_required
def users_add():
    args = request.args
    return render_template('users_add.j2', title="Add User", current_link="users", token=args['token'], admin_view=True)


@admin_routes.route('/users/add/do', methods=['POST'])
@login_required
def users_add_do():
    args = request.args
    form = request.form
    return redirect('/users?token=' + args['token'])


@admin_routes.route('/users/remove/<int:user_id>', methods=['GET'])
@login_required
def users_remove(user_id):
    args = request.args
    return redirect('/users?token=' + args['token'])


@admin_routes.route('/franchises', methods=['GET'])
@login_required
def franchises():
    args = request.args
    return render_template('franchises.j2', title="Franchises", current_link="franchises", token=args['token'], admin_view=True)


@admin_routes.route('/franchises/add', methods=['GET'])
@login_required
def franchises_add():
    args = request.args
    return render_template('franchises_add.j2', title="Add Franchise", current_link="franchises", token=args['token'], admin_view=True)


@admin_routes.route('/franchises/add/do', methods=['POST'])
@login_required
def franchises_add_do():
    args = request.args
    form = request.form
    return redirect('/franchises?token=' + args['token'])


@admin_routes.route('/franchises/remove/<franchise_id>', methods=['GET'])
@login_required
def franchises_remove(franchise_id):
    args = request.args
    return redirect('/franchises?token=' + args['token'])
