import os
import typing
from functools import wraps

from flask import (Blueprint, Response, current_app, flash, redirect,
                   render_template, request, send_from_directory, url_for)
from pony.orm import db_session
from werkzeug.exceptions import BadRequestKeyError

from mailer.models.customers import CustomerManager
from mailer.models.queue import QueueManager
from mailer.models.sessions import SessionManager
from mailer.models.templates import TemplateManager
from mailer.models.users import UserManager

app_routes = Blueprint(__name__, 'app_routes')


def login_required(f):
    @wraps(f)
    def decorator(**kwargs):
        with db_session:
            try:
                # set token to 'no_valid_token' if token doesnt exist. this stops 400 bad request errors.
                token = request.args.get('token', 'no_valid_token')
                if SessionManager.validate(token):
                    return f(**kwargs)
                else:
                    return redirect(url_for('.login'))
            except BadRequestKeyError as err:
                print(err)
                print("Requested URL: {0}".format(request.url))
                return redirect(url_for('.login'))
    return decorator


@app_routes.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app_routes.route('/', methods=['GET'])
@login_required
def index() -> Response:
    args: typing.Dict[str, typing.Any] = request.args
    return render_template('index.j2', title="Home", current_link="home", token=args['token'], admin_view=False)


@app_routes.route('/login', methods=['GET'])
def login() -> Response:
    return render_template('login.j2', title="Login", current_link="login")


@app_routes.route('/login/do', methods=['POST'])
@db_session
def login_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    if form['username'] and form['password']:
        res = UserManager.validate(form['username'], form['password'])
        if res is not False:
            qs: typing.Dict(str, str) = {'token': str(res)}
            return redirect(url_for('.index', **qs))
        else:
            flash('Invalid username and/or password', 'login_error')
            return redirect(url_for('.login'))
    else:
        flash('Invalid username and/or password', 'login_error')
        return redirect(url_for('.login'))


@app_routes.route('/logout', methods=['GET'])
def logout() -> Response:
    return redirect(url_for('.login'))


@app_routes.route('/queue', methods=['GET'])
@login_required
@db_session
def queue() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    queue = QueueManager.get_queue()
    return render_template('queue.j2', title="Queue", current_link="queue", token=args['token'], queue=queue)


@app_routes.route('/queue/add', methods=['GET'])
@login_required
@db_session
def queue_add() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    templates = TemplateManager.get_templates()
    return render_template('queue_add.j2', title="Add Customer", current_link="queue", token=args['token'], templates=templates)


@app_routes.route('/queue/add/do', methods=['POST'])
@login_required
@db_session
def queue_add_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    if CustomerManager.add_customer(form['first_name'], form['last_name'], form['email'], form['phone']):
        customer = CustomerManager.get_customer(email=form['email'])
    else:
        return redirect(url_for('.queue_add', **qs))
    if QueueManager.add_queue(customer.customer_id, form['template_id']):
        return redirect(url_for('.queue', **qs))
    else:
        return redirect(url_for('.queue_add', **qs))


@app_routes.route('/queue/remove/<int:queue_id>', methods=['GET'])
@login_required
@db_session
def queue_remove(queue_id: int) -> Response:
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    if QueueManager.remove_queue(queue_id):
        return redirect(url_for('.queue', **qs))
    else:
        flash("Error removing customer from queue")
        return redirect(url_for('.queue', **qs))


@app_routes.route('/customers', methods=['GET'])
@login_required
@db_session
def customers() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('customers.j2', title='Customers', token=args['token'], current_link='customers', customers=CustomerManager.get_customers())


@app_routes.route('/customers/add', methods=['GET'])
@login_required
def customers_add() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('customers_add.j2', title='Add Customer', token=args['token'], current_link='customers')


@app_routes.route('/customers/add/do', methods=['POST'])
@login_required
@db_session
def customers_add_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    if CustomerManager.add_customer(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], phone=form['phone']):
        return redirect(url_for('.customers', **qs))
    else:
        return redirect(url_for('.customers_add', **qs))


@app_routes.route('/customers/remove/<int:customer_id>', methods=['GET'])
@login_required
@db_session
def customers_remove(customer_id: int) -> Response:
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    CustomerManager.remove_customer(customer_id=customer_id)
    return redirect(url_for('.customers', **qs))


@app_routes.route('/customers/edit/<int:customer_id>', methods=['GET'])
@login_required
@db_session
def customers_edit(customer_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    customer = CustomerManager.get_customer(customer_id=customer_id)
    return render_template('customers_edit.j2', title='Add Customer', token=args['token'], current_link='customers', customer=customer)


@app_routes.route('/customers/edit/do', methods=['POST'])
@login_required
@db_session
def customers_edit_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    CustomerManager.update_customer(customer_id=form['customer_id'], first_name=form['first_name'],
                                    last_name=form['last_name'], email=form['email'], phone=form['phone'])
    return redirect(url_for('.customers', **qs))


@app_routes.route('/templates', methods=['GET'])
@login_required
@db_session
def templates() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    tpl_list = TemplateManager.get_templates()
    return render_template('templates.j2', title='Templates', token=args['token'], current_link='templates', template_list=tpl_list)


@app_routes.route('/templates/add', methods=['GET'])
@login_required
def templates_add() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    return render_template('templates_add.j2', title='Add Template', token=args['token'], current_link='templates')


@app_routes.route('/templates/add/do', methods=['POST'])
@login_required
@db_session
def templates_add_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    TemplateManager.add_template(name=form['title'], body=form['template'], expires=form['expires'])
    return redirect(url_for('.templates', **qs))


@app_routes.route('/templates/remove/<int:template_id>', methods=['GET'])
@login_required
@db_session
def templates_remove(template_id: int) -> Response:
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    TemplateManager.remove_template(template_id=template_id)
    return redirect(url_for('.templates', **qs))


@app_routes.route('/templates/edit/<int:template_id>', methods=['GET'])
@login_required
@db_session
def templates_edit(template_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    tpl = TemplateManager.get_template(template_id=template_id)
    return render_template('templates_edit.j2', title='Edit Template', token=args['token'], current_link='templates', template=tpl)


@app_routes.route('/templates/edit/do', methods=['POST'])
@login_required
@db_session
def templates_edit_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    qs: typing.Dict(str, str) = {'token': request.args.get('token')}
    TemplateManager.update_template(template_id=form['template_id'],
                                    name=form['title'], body=form['template'], expires=form['expires'])
    return redirect(url_for('.templates', **qs))
