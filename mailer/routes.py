from flask import Blueprint, make_response
from functools import wraps

app_routes = Blueprint(__name__, 'app_routes')


def login_required(f):
    wraps(f)

    def decorator(f):
        return f
    return f


@login_required
@app_routes.route('/', methods=['GET'])
def index():
    pass


@login_required
@app_routes.route('/queue', methods=['GET'])
def queue():
    pass


@login_required
@app_routes.route('/queue/add', methods=['GET'])
def queue_add():
    pass


@login_required
@app_routes.route('/queue/remove/<int:queue_id>', methods=['GET'])
def queue_remove(queue_id):
    pass


@login_required
@app_routes.route('/queue/update/<int:queue_id>', methods=['GET'])
def queue_update(queue_id):
    pass


@login_required
@app_routes.route('/customers', methods=['GET'])
def customers():
    pass


@login_required
@app_routes.route('/customers/add', methods=['GET'])
def customers_add():
    pass


@login_required
@app_routes.route('/customers/remove/<int:customer_id>', methods=['GET'])
def customers_remove(customer_id):
    pass


@login_required
@app_routes.route('/customers/update/<int:customer_id>', methods=['GET'])
def customers_update(customer_id):
    pass


@login_required
@app_routes.route('/customers/profile/<int:customer_id>', methods=['GET'])
def customers_profile(customer_id):
    pass
