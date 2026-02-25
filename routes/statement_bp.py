from flask import Blueprint

from controllers.statementController import view, list, delete_trx

statement_bp = Blueprint("statement_bp", __name__)

# user_bp.route('/<int:user_id>', methods=['GET'])(edit)
statement_bp.route('/list', methods=['GET', 'POST', 'DELETE'])(list)
statement_bp.route('/view/<int:statement_id>', methods=['GET', 'POST', 'DELETE'])(view)
statement_bp.route('/trx/delete/<int:trx_id>', methods=['DELETE'])(delete_trx)