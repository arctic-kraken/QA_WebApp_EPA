from flask import Blueprint

from controllers.userController import admin_list

user_bp = Blueprint("user_bp", __name__)

user_bp.route('/list', methods=['GET'])(admin_list)
