from flask import Blueprint
from controllers.appController import landing, login, dashboard

app_bp = Blueprint('app_bp', __name__)

app_bp.route('/', methods=['GET'])(landing)
app_bp.route('/login', methods=['GET'])(login)
# app_bp.route('/logout', methods=['GET'])(landing)
app_bp.route('/dashboard', methods=['GET'])(dashboard)