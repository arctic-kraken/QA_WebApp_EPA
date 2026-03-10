from db import db

from models.User import User
from models.UserAccountRole import UserAccountRole
from services.appService import app_service

class UserService:
    CONST_VALIDATE_PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,50}$"

    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()

    # obsolete
    def get_user_and_role_for(user_id, account_id):
        user = User.query.filter_by(id=user_id).first()
        role = UserAccountRole.query.filter_by(user_id=user.id, account_id=account_id).first()

        return user, role.is_admin

    def user_name_is_taken(self, requested_user_name: str):
        return True if User.query.filter_by(name=requested_user_name).first() is not None else False

    def validate_user_name(self, requested_user_name: str):
        errors = []

        if not app_service.validate_user_input(requested_user_name):
            return False, [f'User name {app_service.CONST_REGEX_ERROR_MSG}']

        if self.user_name_is_taken(requested_user_name):
            errors.append('User name taken')

        if len(requested_user_name) < 6 or len(requested_user_name) > 50:
            errors.append('User name must be between 6 and 50 characters long')

        return True if len(errors) == 0 else False, errors

    def validate_password(self, requested_password: str, confirmation: str):
        errors = []

        if not app_service.validate_user_input(requested_password):
            return False, [f"Password {app_service.CONST_REGEX_ERROR_MSG}"]

        if len(requested_password) < 6 or len(requested_password) > 50:
            errors.append('Password must be between 6 and 50 characters long')

        if confirmation != requested_password:
            errors.append("Passwords must match")

        if app_service.validate_user_input(requested_password, self.CONST_VALIDATE_PASSWORD_REGEX):
            errors.append(f"Password must contain at least 1 Upper case, 1 lower case, a number and a special character: @$!%*#?&")

        return True if len(errors) == 0 else False, errors

    def create_user(self, requested_user_name: str, requested_password: str):
        try:
            db.session.add(User(name=requested_user_name, password=app_service.encrypt(requested_password)))
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user(self, user_id: int = 0, name: str = None):
        if name is not None:
            return User.query.filter_by(name=name).first()
        else:
            return User.query.filter_by(id=user_id).first()

    def check_credentials(self, username: str, password: str):
        return User.query.filter_by(name=username, password=app_service.encrypt(password)).first()

user_service = UserService()
