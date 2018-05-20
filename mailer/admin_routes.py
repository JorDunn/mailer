import typing
from functools import wraps

from flask import (Blueprint, Response, flash, redirect, render_template,
                   request, abort)
from werkzeug.exceptions import BadRequestKeyError

from mailer.models.franchises import FranchiseManager
from mailer.models.sessions import SessionManager
from mailer.models.users import UserManager

admin_routes = Blueprint(__name__, 'admin_routes',
                         url_prefix='/admin')


def login_required(f):
    @wraps(f)
    def decorator(**kwargs):
        try:
            args: typing.Dict(str, typing.Any) = request.args
            if SessionManager.validate(args['token']):
                return f(**kwargs)
            else:
                return redirect('/login')
        except BadRequestKeyError:
            return redirect('/login')
    return decorator


def admin_required(f):
    @wraps(f)
    def decorator(**kwargs):
        try:
            args: typing.Dict(str, typing.Any) = request.args
            if UserManager.admin_verification(args['token']):
                return f(**kwargs)
            else:
                return abort(401)
        except Exception as err:
            print(err)
            return abort(401)
    return decorator


@admin_routes.route('/', methods=['GET'])
@login_required
@admin_required
def index() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('admin.j2', title="Admin Home", current_link="admin_home", token=args['token'], admin_view=True)


@admin_routes.route('/users', methods=['GET'])
@login_required
@admin_required
def users() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('users.j2', title="Users", current_link="users", token=args['token'], admin_view=True, users=UserManager.get_users(), franchises=FranchiseManager.get_franchises())


@admin_routes.route('/users/add', methods=['GET'])
@login_required
@admin_required
def users_add() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('users_add.j2', title="Add User", current_link="users", token=args['token'], admin_view=True, franchises=FranchiseManager.get_franchises())


@admin_routes.route('/users/add/do', methods=['POST'])
@login_required
@admin_required
def users_add_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    if form['password'] != form['password_verification']:
        flash("The passwords entered do not match")
        return redirect('/admin/users/add?token=' + args['token'])
    else:
        UserManager.add_user(form['franchises'], form['first_name'], form['last_name'],
                             form['username'], form['password'], request.form.get('is_admin', False))
        return redirect('/admin/users?token=' + args['token'])


@admin_routes.route('/users/edit/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def users_edit(user_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('users_edit.j2', title="Edit User", current_link="users", token=args['token'], admin_view=True, user=UserManager.get_user(user_id), franchises=FranchiseManager.get_franchises())


@admin_routes.route('/users/edit/do', methods=['POST'])
@login_required
@admin_required
def users_edit_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    if request.form.get('password', '') != request.form.get('password_verification', ''):
        flash("The passwords entered do not match")
        return redirect('/admin/users/edit/' + form['user_id'] + '?token=' + args['token'])
    else:
        UserManager.update_user(form['user_id'], form['franchises'], form['first_name'],
                                form['last_name'], form['password'], request.form.get('is_admin', False))
        return redirect('/admin/users?token=' + args['token'])


@admin_routes.route('/users/remove/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def users_remove(user_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    UserManager.remove_user(user_id)
    return redirect('/admin/users?token=' + args['token'])


@admin_routes.route('/franchises', methods=['GET'])
@login_required
@admin_required
def franchises() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('franchises.j2', title="Franchises", current_link="franchises", token=args['token'], admin_view=True, franchises=FranchiseManager.get_franchises())


@admin_routes.route('/franchises/add/do', methods=['POST'])
@login_required
@admin_required
def franchises_add_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    FranchiseManager.add_franchise(form['name'])
    return redirect('/admin/franchises?token=' + args['token'])


@admin_routes.route('/franchises/remove/<int:franchise_id>', methods=['GET'])
@login_required
@admin_required
def franchises_remove(franchise_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    FranchiseManager.remove_franchise(franchise_id)
    return redirect('/admin/franchises?token=' + args['token'])
