from flask import Blueprint

from controllers.budgetController import list, edit, create, delete

budget_bp = Blueprint("budget_bp", __name__)

budget_bp.route('/list', methods=['GET'])(list)
budget_bp.route('/edit/<int:budget_id>', methods=['GET', 'POST'])(edit)
budget_bp.route('/create', methods=['GET'])(create)
budget_bp.route('/delete/<int:budget_id>', methods=['DELETE'])(delete)
