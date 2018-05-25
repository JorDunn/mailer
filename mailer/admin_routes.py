import typing
from functools import wraps

from flask import (Blueprint, Response, abort, flash, redirect,
                   render_template, request, url_for)
from pony.orm import db_session
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
            if SessionManager.validate(request.args.get('token')):
                return f(**kwargs)
            else:
                return redirect(url_for('mailer.routes.login'))
        except BadRequestKeyError as err:
            print(err)
            print("Requested URL: {0}".format(request.url))
            return redirect(url_for('mailer.routes.login'))
    return decorator


def admin_required(f):
    @wraps(f)
    def decorator(**kwargs):
        try:
            if UserManager.admin_verification(request.args.get('token')):
                return f(**kwargs)
            else:
                return abort(401)
        except Exception as err:
            print(err)
            print("Requested URL: {0}".format(request.url))
            return abort(401)
    return decorator


@admin_routes.route('/', methods=['GET'])
@login_required
@admin_required
def index() -> Response:
    return render_template('admin.j2', title="Admin Home", current_link="admin_home", token=request.args.get('token'), admin_view=True)


@admin_routes.route('/users', methods=['GET'])
@login_required
@admin_required
@db_session
def users() -> Response:
    return render_template('users.j2', title="Users", current_link="users", token=request.args.get('token'), admin_view=True, users=UserManager.get_users(), franchises=FranchiseManager.get_franchises())


@admin_routes.route('/users/add', methods=['GET'])
@login_required
@admin_required
@db_session
def users_add() -> Response:
    return render_template('users_add.j2', title="Add User", current_link="users", token=request.args.get('token'), admin_view=True, franchises=FranchiseManager.get_franchises())


@admin_routes.route('/users/add/do', methods=['POST'])
@login_required
@admin_required
@db_session
def users_add_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    if form['password'] != form['password_verification']:
        flash("The passwords entered do not match")
        return redirect(url_for('.users_add', **{'token': request.args.get('token')}))
    else:
        UserManager.add_user(form['franchises'], form['first_name'], form['last_name'],
                             form['username'], form['password'], request.form.get('is_admin', False))
        return redirect(url_for('.users', **{'token': request.args.get('token')}))


@admin_routes.route('/users/edit/<int:user_id>', methods=['GET'])
@login_required
@admin_required
@db_session
def users_edit(user_id: int) -> Response:
    return render_template('users_edit.j2', title="Edit User", current_link="users", token=request.args.get('token'), admin_view=True, user=UserManager.get_user(user_id), franchises=FranchiseManager.get_franchises())


@admin_routes.route('/users/edit/do', methods=['POST'])
@login_required
@admin_required
@db_session
def users_edit_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    if request.form.get('password', '') != request.form.get('password_verification', ''):
        flash("The passwords entered do not match")
        return redirect(url_for('.users_edit', **{'user_id': form['user_id'], 'token': request.args.get('token')}))
    else:
        UserManager.update_user(form['user_id'], form['franchises'], form['first_name'],
                                form['last_name'], form['password'], request.form.get('is_admin', False))
        return redirect(url_for('.users', **{'token': request.args.get('token')}))


@admin_routes.route('/users/remove/<int:user_id>', methods=['GET'])
@login_required
@admin_required
@db_session
def users_remove(user_id: int) -> Response:
    UserManager.remove_user(user_id)
    return redirect(url_for('.users', **{'token': request.args.get('token')}))


@admin_routes.route('/franchises', methods=['GET'])
@login_required
@admin_required
@db_session
def franchises() -> Response:
    return render_template('franchises.j2', title="Franchises", current_link="franchises", token=request.args.get('token'), admin_view=True, franchises=FranchiseManager.get_franchises())


@admin_routes.route('/franchises/add/do', methods=['POST'])
@login_required
@admin_required
@db_session
def franchises_add_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    FranchiseManager.add_franchise(form['name'])
    return redirect(url_for('.franchises', **{'token': request.args.get('token')}))


@admin_routes.route('/franchises/remove/<int:franchise_id>', methods=['GET'])
@login_required
@admin_required
@db_session
def franchises_remove(franchise_id: int) -> Response:
    FranchiseManager.remove_franchise(franchise_id)
    return redirect(url_for('.franchises', **{'token': request.args.get('token')}))


@admin_routes.route('/franchises/edit/<int:franchise_id>', methods=['GET'])
@login_required
@admin_required
@db_session
def franchises_edit(franchise_id: int) -> Response:
    pass
