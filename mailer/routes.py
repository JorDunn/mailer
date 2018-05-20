import typing
from functools import wraps

from flask import (Blueprint, Response, flash, redirect, render_template,
                   request, url_for, current_app)
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
        try:
            args: typing.Dict(str, typing.Any) = request.args
            if SessionManager.validate(args['token']):
                return f(**kwargs)
            else:
                return redirect('/login')
        except BadRequestKeyError as err:
            print(err)
            return redirect('/login')
    return decorator


@app_routes.route('/', methods=['GET'])
@login_required
def index() -> Response:
    args: typing.Dict[str, typing.Any] = request.args
    return render_template('index.j2', title="Home", current_link="home", token=args['token'], admin_view=False)


@app_routes.route('/login', methods=['GET'])
def login() -> Response:
    return render_template('login.j2', title="Login", current_link="login")


@app_routes.route('/login/do', methods=['POST'])
def login_do() -> Response:
    form: typing.Dict(str, typing.Any) = request.form
    if form['username'] and form['password']:
        res = UserManager.validate(form['username'], form['password'])
        if res is not False:
            return redirect('/?token=' + str(res))
        else:
            flash('Invalid username and/or password', 'login_error')
            return redirect('/login')
    else:
        flash('Invalid username and/or password', 'login_error')
        return redirect('/login')


@app_routes.route('/logout', methods=['GET'])
@login_required
def logout() -> Response:
    return redirect('/login')


@app_routes.route('/queue', methods=['GET'])
@login_required
def queue() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    queue = QueueManager.get_queue()
    return render_template('queue.j2', title="Queue", current_link="queue", token=args['token'], queue=queue)


@app_routes.route('/queue/add', methods=['GET'])
@login_required
def queue_add() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    templates = TemplateManager.get_templates()
    return render_template('queue_add.j2', title="Add Customer", current_link="queue", token=args['token'], templates=templates)


@app_routes.route('/queue/add/do', methods=['POST'])
@login_required
def queue_add_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    if CustomerManager.add_customer(form['first_name'], form['last_name'], form['email'], form['phone']):
        customer = CustomerManager.get_customer(email=form['email'])
    else:
        return redirect('/queue/add?token=' + args['token'])
    if QueueManager.add_queue(customer.customer_id, form['template_id']):
        return redirect('/queue?token=' + args['token'])
    else:
        return redirect('/queue/add?token=' + args['token'])


@app_routes.route('/queue/remove/<int:queue_id>', methods=['GET'])
@login_required
def queue_remove(queue_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    if QueueManager.remove_queue(queue_id):
        return redirect('/queue?token=' + args['token'])
    else:
        flash("Error removing customer from queue")
        return redirect('/queue?token=' + args['token'])


@app_routes.route('/customers', methods=['GET'])
@login_required
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
def customers_add_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    if CustomerManager.add_customer(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], phone=form['phone']):
        return redirect('/customers?token=' + args['token'])
    else:
        return redirect('/customers/add?token=' + args['token'])


@app_routes.route('/customers/remove/<int:customer_id>', methods=['GET'])
@login_required
def customers_remove(customer_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    CustomerManager.remove_customer(customer_id=customer_id)
    return redirect('/customers?token=' + args['token'])


@app_routes.route('/customers/edit/<int:customer_id>', methods=['GET'])
@login_required
def customers_edit(customer_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    customer = CustomerManager.get_customer(customer_id=customer_id)
    return render_template('customers_edit.j2', title='Add Customer', token=args['token'], current_link='customers', customer=customer)


@app_routes.route('/customers/edit/do', methods=['POST'])
@login_required
def customers_edit_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    CustomerManager.update_customer(customer_id=form['customer_id'], first_name=form['first_name'],
                                    last_name=form['last_name'], email=form['email'], phone=form['phone'])
    return redirect('/customers?token=' + args['token'])


@app_routes.route('/templates', methods=['GET'])
@login_required
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
def templates_add_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    TemplateManager.add_template(name=form['title'], body=form['template'], expires=form['expires'])
    return redirect('/templates?token=' + args['token'])


@app_routes.route('/templates/remove/<int:template_id>', methods=['GET'])
@login_required
def templates_remove(template_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    TemplateManager.remove_template(template_id=template_id)
    return redirect('/templates?token=' + args['token'])


@app_routes.route('/templates/edit/<int:template_id>', methods=['GET'])
@login_required
def templates_edit(template_id: int) -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    tpl = TemplateManager.get_template(template_id=template_id)
    return render_template('templates_edit.j2', title='Edit Template', token=args['token'], current_link='templates', template=tpl)


@app_routes.route('/templates/edit/do', methods=['POST'])
@login_required
def templates_edit_do() -> Response:
    args: typing.Dict(str, typing.Any) = request.args
    form: typing.Dict(str, typing.Any) = request.form
    TemplateManager.update_template(template_id=form['template_id'],
                                    name=form['title'], body=form['template'], expires=form['expires'])
    return redirect('/templates?token=' + args['token'])
