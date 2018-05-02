from flask import Blueprint, render_template, redirect, request, flash
from werkzeug.exceptions import BadRequestKeyError
from functools import wraps
from mailer.models.sessions import SessionManager
from mailer.models.users import UserManager
from mailer.models.queue import QueueManager
from mailer.models.customers import CustomerManager

from pprint import pprint

app_routes = Blueprint(__name__, 'app_routes')


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


@app_routes.route('/', methods=['GET'])
@login_required
def index():
    args = request.args
    return render_template('index.j2', title="Home", current_link="home", token=args['token'])


@app_routes.route('/login', methods=['GET'])
def login():
    return render_template('login.j2', title="Login", current_link="login")


@app_routes.route('/login/do', methods=['POST'])
def login_do():
    data = request.form
    res = UserManager.validate(data['username'], data['password'])
    if res is not False:
        return redirect('/?token='+str(res))
    else:
        flash('Invalid username and/or password', 'login_error')
        return redirect('/login')


@app_routes.route('/logout', methods=['GET'])
@login_required
def logout():
    return redirect('/login')


@app_routes.route('/queue', methods=['GET'])
@login_required
def queue():
    args = request.args
    queue = QueueManager.get_queue()
    return render_template('queue.j2', title="Queue", current_link="queue", token=args['token'], queue=queue)


@app_routes.route('/queue/add', methods=['GET'])
@login_required
def queue_add():
    args = request.args
    return render_template('queue_add.j2', title="Add Customer", current_link="queue", token=args['token'])


@app_routes.route('/queue/add/do', methods=['POST'])
@login_required
def queue_add_do():
    args = request.args
    data = request.form
    if CustomerManager.add_customer(data['first_name'], data['last_name'], data['email'], data['phone']):
        customer = CustomerManager.get_customer(data['email'])
        if QueueManager.add_queue(customer.customer_id):
            return redirect('/queue?token=' + args['token'])
        else:
            flash("Error adding customer to queue", "queue_error")
            return redirect('/queue/add?token=' + args['token'])
    else:
        flash("Error adding customer", "queue_error")
        return redirect('/queue/add?token=' + args['token'])


@app_routes.route('/queue/remove/<int:queue_id>', methods=['GET'])
@login_required
def queue_remove(queue_id):
    pass


@app_routes.route('/queue/update/<int:queue_id>', methods=['GET'])
@login_required
def queue_update(queue_id):
    pass


@app_routes.route('/customers', methods=['GET'])
@login_required
def customers():
    pass


@app_routes.route('/customers/add', methods=['GET'])
@login_required
def customers_add():
    pass


@app_routes.route('/customers/remove/<int:customer_id>', methods=['GET'])
@login_required
def customers_remove(customer_id):
    pass


@app_routes.route('/customers/update/<int:customer_id>', methods=['GET'])
@login_required
def customers_update(customer_id):
    pass


@app_routes.route('/customers/profile/<int:customer_id>', methods=['GET'])
@login_required
def customers_profile(customer_id):
    pass


@app_routes.route('/templates', methods=['GET'])
@login_required
def templates():
    pass
