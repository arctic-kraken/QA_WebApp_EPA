from models.User import User
from models.UserAccountRole import UserAccountRole

# obsolete
def get_user_and_role_for(user_id, account_id):
    user = User.query.filter_by(id=user_id).first()
    role = UserAccountRole.query.filter_by(user_id=user.id, account_id=account_id).first()

    return user, role.is_admin
