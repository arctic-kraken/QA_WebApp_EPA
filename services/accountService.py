import uuid

from sqlalchemy.sql.functions import user

from db import db
from models.Account import Account
from models.User import User
from uuid import uuid4
from models.UserAccountRole import UserAccountRole

class AccountService:
    def create_account_for(self, user_id, account_name, account_reference, starting_date, starting_balance, currency_code):
        try:
            new_account = Account()
            new_account.name = account_name
            new_account.reference = account_reference
            new_account.starting_date = starting_date
            new_account.starting_balance = starting_balance
            new_account.currency_code = currency_code

            db.session.add(new_account)
            db.session.commit()

            db.session.refresh(new_account)
            db.session.get_one(User, user_id)

            new_role = UserAccountRole()
            new_role.user_id = user_id
            new_role.account_id = new_account.id
            new_role.is_admin = True
            db.session.add(new_role)
            db.session.commit()

            print("Account created successfully")
            return new_account, None

        except Exception as e:
            print(f"Failed to create Account: {e}")
            return Account(), ["Failed to create Account"]

    def get_account_user_role_for(self, user_id, account_id):
        user = User.query.filter_by(id=user_id).first()
        account = Account.query.filter_by(id=account_id).first()
        role = UserAccountRole.query.filter_by(user_id=user.id, account_id=account_id).first()

        return account, user, role.is_admin

    def get_new_invite_code(self, user_id, account_id):
        account, user, is_admin = self.get_account_user_role_for(user_id, account_id)
        if is_admin is False:
            return None

        new_code = uuid4()
        account.latest_invite_code = new_code
        account.last_invite_created_date = db.func.now()
        db.session.commit()
        return new_code

    def validate_invite_code(self, code):
        try:
            uuid.UUID(code)
            return True, None
        except ValueError:
            return False, ["Invalid Invite Code"]

    def join_user_to_account(self, user_id, invite_code):
        result, error = self.validate_invite_code(invite_code)
        if result is False:
            return False, error, None

        account = Account.query.filter_by(latest_invite_code=invite_code).first()
        if account is None:
            return False, ["Account with this invite code does not exist"], None

        # this is impossible in theory but better to be safe than sorry
        role = UserAccountRole.query.filter_by(user_id=user_id, account_id=account.id).first()
        if role is not None:
            return False, ["You are already assigned to this account"], None

        try:
            role = UserAccountRole()
            role.user_id = user_id
            role.account_id = account.id
            role.is_admin = False

            db.session.add(role)
            db.session.commit()
        except Exception as e:
            return False, [f"Failed to join Account - {e}"], None

        return True, None, account.id

    def get_all_users_for_account(self, account_id):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return None, ["Failed to get all users for this account"]

        all_users = db.session.query(User).join(UserAccountRole, UserAccountRole.user_id == User.id).filter(UserAccountRole.account_id == account.id).all()

        return all_users, None

    def revoke_access_from(self, user_id, account_id):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return None, ["Failed to get account"]

        role = UserAccountRole.query.filter_by(user_id=user_id, account_id=account.id).first()
        if role is None:
            return False, ["Failed to find user assigned to this account"]

        # effectively cant revoke from self
        if role.is_admin:
            return False, ["Cannot revoke access to admin type account"]

        try:
            db.session.delete(role)
            db.session.commit()
        except Exception as e:
            return False, [f"Failed to revoke access - {e}"]

        return True, None


account_service = AccountService()
