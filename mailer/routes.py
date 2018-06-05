import os
from datetime import datetime
from functools import wraps
from time import time
from pprint import pprint

from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, send_from_directory, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from pony.orm import db_session, commit

from mailer.extensions import login_manager
from mailer.models import (Customer, Group, Queue, Role, Subgroup, Template,
                           User)

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
@db_session
def before_request():
    request_start_time = time()
    g.user = current_user
    if g.user.is_anonymous:
        g.role = None
        g.group = None
        g.subgroup = None
    else:
        g.role = Role.get_permissions(rid=g.user.role.rid)
        g.group = Group.get_group(gid=g.user.group.gid)
        g.subgroup = Subgroup.get(gid=g.group.gid)
    g.request_time = lambda: "%.5fs" % (time() - request_start_time)


def admin_required(f):
    @wraps(f)
    def decorator(**kwargs):
        if g.user.is_admin:
            return f(**kwargs)
        else:
            return abort(401)
    return decorator


@app_routes.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app_routes.route('/login', methods=['GET', 'POST'])
@db_session
def login():
    if request.method == 'GET':
        return render_template('login.j2', title="Login", current_link="login")
    elif request.method == 'POST':
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
@db_session
def index():
    return render_template('index.j2', title="Home", current_link="home")


@app_routes.route('/queue', methods=['GET'])
@login_required
@db_session
def queue():
    queue = Queue.get_items()
    return render_template('queue.j2', title='Queue', current_link='queue', queue=queue)


@app_routes.route('/queue/add', methods=['GET', 'POST'])
@login_required
@db_session
def queue_add():
    if request.method == 'GET':
        if g.role.can_add_queue_items:
            templates = Template.get_all()
            return render_template('queue_add.j2', title='Add to queue', current_link='queue', templates=templates)
        else:
            return redirect(url_for('.queue'))
    elif request.method == 'POST':
        if g.role.can_add_queue_items:
            if Customer.exists(email=request.form.get('email')):
                customer = Customer.get(email=request.form.get('email'))
                if Queue.exists(customer=customer):
                    flash('Customer is already in the queue', 'queue_error')
                    return redirect(url_for('.queue'))
            else:
                customer = Customer(first_name=request.form.get('first_name'),
                                    last_name=request.form.get('last_name'),
                                    email=request.form.get('email'),
                                    added_on=datetime.now())
                commit()
            template = Template.get(tid=request.form.get('template'))
            user = User.get(uid=g.user.uid)
            queue_item = Queue(customer=customer, user=user, template=template)
            customer.queue_item = queue_item
            commit()
            return redirect(url_for('.queue'))
        else:
            return redirect(url_for('.queue'))


@app_routes.route('/queue/<int:customer_id>/add', methods=['GET'])
@login_required
@db_session
def queue_add_customer(customer_id):
    if g.role.can_add_queue_items:
        customer = Customer.get(cid=customer_id)
        templates = Template.get_all()
        return render_template('queue_add_customer.j2', title='Add Customer to Queue', current_link='queue', customer=customer, templates=templates)
    else:
        return redirect(url_for('.customers'))


@app_routes.route('/queue/<int:queue_id>/remove', methods=['GET'])
@login_required
@db_session
def queue_remove(queue_id):
    if g.role.can_delete_queue_items:
        Queue.get(qid=queue_id).delete()
        commit()
        return redirect(url_for('.queue'))
    else:
        return redirect(url_for('.queue'))


@app_routes.route('/queue/<int:queue_id>/edit', methods=['GET', 'POST'])
@login_required
@db_session
def queue_edit(queue_id):
    if g.role.can_edit_queue_items:
        if request.method == 'GET':
            queue_item = Queue.get(qid=queue_id)
            customer = Customer.get(cid=queue_item.customer.cid)
            templates = Template.get_all()
            return render_template('queue_edit.j2', title='Edit Customer in Queue', current_link='queue', queue_item=queue_item, customer=customer, templates=templates)
        elif request.method == 'POST':
            queue_item = Queue.get(qid=queue_id)
            queue_item.template = Template.get(tid=request.form.get('template'))
            return redirect(url_for('.queue'))


@app_routes.route('/customers', methods=['GET'])
@login_required
@db_session
def customers():
    customers = Customer.get_all()
    return render_template('customers.j2', title='Customers', current_link='customers', customers=customers)


@app_routes.route('/customers/add', methods=['GET', 'POST'])
@login_required
@db_session
def customers_add():
    if request.method == 'GET':
        return render_template('customers_add.j2', title='Add a Customer', current_link='customers')
    elif request.method == 'POST':
        pprint(request.form)
        current_time = datetime.now()
        Customer(first_name=request.form.get('first_name'),
                 last_name=request.form.get('last_name'),
                 email=request.form.get('email'),
                 added_on=current_time)
        commit()
        return redirect(url_for('.customers'))


@app_routes.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
@db_session
def customers_edit(customer_id):
    if g.role.can_edit_customers:
        if request.method == 'GET':
            return render_template('customers_edit.j2', title='Edit Customer', current_link='customers', customer=Customer.get(cid=customer_id))
        elif request.method == 'POST':
            customer = Customer.get(cid=customer_id)
            customer.first_name = request.form.get('first_name')
            customer.last_name = request.form.get('last_name')
            customer.email = request.form.get('email')
            commit()
            return redirect(url_for('.customers'))


@app_routes.route('/customers/<int:customer_id>/remove', methods=['GET'])
@login_required
@db_session
def customers_remove(customer_id):
    if g.role.can_delete_customers:
        Customer.get(cid=customer_id).delete()
        commit()
        return redirect(url_for('.customers'))


@app_routes.route('/templates', methods=['GET'])
@login_required
@db_session
def templates():
    templates = Template.get_all()
    return render_template('templates.j2', title='Templates', current_link='templates', templates=templates)


@app_routes.route('/templates/add', methods=['GET', 'POST'])
@login_required
@db_session
def templates_add():
    if g.role.can_add_templates:
        if request.method == 'GET':
            return render_template('templates_add.j2', title='Add template', current_link='templates')
        elif request.method == 'POST':
            if request.form['expires']:
                Template(name=request.form.get('name'),
                         subject=request.form.get('subject'),
                         body=request.form.get('body'),
                         added_by=request.form.get('added_by'),
                         added_on=datetime.now(),
                         expires_on=request.form.get('expires'))
            else:
                Template(name=request.form.get('name'),
                         subject=request.form.get('subject'),
                         body=request.form.get('body'),
                         added_by=request.form.get('added_by'),
                         added_on=datetime.now())
            commit()
            return redirect(url_for('.templates'))


@app_routes.route('/templates/<int:template_id>/edit', methods=['GET', 'POST'])
@login_required
@db_session
def templates_edit(template_id):
    if g.role.can_edit_templates:
        if request.method == 'GET':
            return render_template('templates_edit.j2', title='Edit Template', current_link='templates', template=Template.get(tid=template_id))
        elif request.method == 'POST':
            template = Template.get(tid=template_id)
            template.name = request.form.get('name')
            template.subject = request.form.get('subject')
            template.body = request.form.get('body')
            template.expires_on = request.form.get('expires')
            commit()
            return redirect(url_for('.templates'))


@app_routes.route('/templates/<int:template_id>/remove', methods=['GET'])
@login_required
@db_session
def templates_remove(template_id):
    if g.role.can_delete_templates:
        Template.get(tid=template_id).delete()
        commit()
        return redirect(url_for('.templates'))


@app_routes.route('/groups', methods=['GET'])
@login_required
@db_session
@admin_required
def groups():
    return render_template('groups.j2', title='Groups', current_link='groups', groups={})


@app_routes.route('/subgroups', methods=['GET'])
@login_required
@db_session
@admin_required
def subgroups():
    return render_template('subgroups.j2', title='Subgroups', current_link='subgroups', subgroups={})


@app_routes.route('/roles', methods=['GET'])
@login_required
@db_session
@admin_required
def roles():
    return render_template('roles.j2', title='Roles', current_link='roles', roles={})


@app_routes.route('/users', methods=['GET'])
@login_required
@db_session
@admin_required
def users():
    return render_template('users.j2', title='Users', current_link='users', users={})


@app_routes.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.j2', title=f"{g.user.username}'s Profile", current_link='profile', user={})
