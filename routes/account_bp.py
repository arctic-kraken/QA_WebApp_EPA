from flask import Blueprint

from controllers.accountController import create, select, join, view, newinvite, revoke

account_bp = Blueprint("account_bp", __name__)

account_bp.route('/create', methods=['GET', 'POST'])(create)
account_bp.route('/select', methods=['GET'])(select)
account_bp.route('/join', methods=['GET', 'POST'])(join)
account_bp.route('/view', methods=['GET'])(view)
account_bp.route('/newinvite', methods=['GET'])(newinvite)
account_bp.route('/revoke_access/<int:user_id>', methods=['DELETE'])(revoke)