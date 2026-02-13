from flask import Blueprint

from controllers.userController import create, edit

user_bp = Blueprint("user_bp", __name__)

user_bp.route('/<int:user_id>', methods=['GET'])(edit)
user_bp.route('/create', methods=['POST'])(create)



# user_bp.route('/', *methods*=['GET'])(**index**)
# user_bp.route('/create', *methods*=['POST'])(**store**)
# user_bp.route('/<int:user_id>', *methods*=['GET'])(**show**)
# user_bp.route('/<int:user_id>/edit', *methods*=['POST'])(**update**)
# user_bp.route('/<int:user_id>', *methods*=['DELETE'])(**destroy**)