from flask import Blueprint
from controllers.appController import landing, login, logout, signup, dashboard

app_bp = Blueprint('app_bp', __name__)

app_bp.route('/', methods=['GET'])(landing)
app_bp.route('/login', methods=['GET', 'POST'])(login)
app_bp.route('/logout', methods=['GET'])(logout)
app_bp.route('/signup', methods=['GET', 'POST'])(signup)
app_bp.route('/dashboard', methods=['GET'])(dashboard)