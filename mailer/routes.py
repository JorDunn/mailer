import os
from time import time
from flask import (Blueprint, current_app, flash, redirect,
                   render_template, request, send_from_directory, url_for, g)
from pony.orm import db_session
from mailer.extensions import login_manager
from mailer.models import User, Role, Group, Subgroup
from flask_login import current_user, login_required, login_user, logout_user


app_routes = Blueprint(__name__, 'app_routes')

login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    try:
        with db_session:
            return User.get_user(uid=user_id)
    except Exception as err:
        print(err)
        return None


@app_routes.before_request
def before_request():
    request_start_time = time()
    g.user = current_user
    if g.user.is_anonymous:
        g.permissions = Role.get_permissions(0)
    else:
        g.permissions = Role.get_permissions(g.user.uid)
    g.request_time = lambda: "%.5fs" % (time() - request_start_time)


@app_routes.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.j2', title="Login", current_link="login")
    elif request.method == 'POST':
        with db_session:
            username = request.form.get('username', None)
            password = request.form.get('password', None)
            if username and password:
                user = User.authenticate(username=username, password=password)
                if user:
                    login_user(user)
                    return redirect(request.args.get('next', url_for('.index')))
                else:
                    flash('Invalid username and/or password', 'login_error')
                    return redirect(url_for('.login'))
            else:
                flash('Invalid username and/or password', 'login_error')
                return redirect(url_for('.login'))


@app_routes.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@app_routes.route('/', methods=['GET'])
@login_required
def index():
    # return redirect(url_for('.queue'))
    return render_template('index.j2', title="Home", current_link="home")


@app_routes.route('/queue', methods=['GET', 'POST'])
@login_required
def queue():
    pass


@app_routes.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    pass


@app_routes.route('/templates', methods=['GET', 'POST'])
@login_required
def templates():
    pass
