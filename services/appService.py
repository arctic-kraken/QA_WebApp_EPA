from flask import session, abort

class AppService:

    def get_current_user_id(self):
        return session.get("uid")

    def get_current_account_id(self):
        return session.get("accid")

    def set_current_user_id(self, user_id):
        session["uid"] = user_id

    def set_current_account_id(self, account_id):
        session["accid"] = account_id

    def check_auth(self):
        user_id = self.get_current_user_id()
        account_id = self.get_current_account_id()
        if user_id is None or account_id is None:
            abort(401)

app_service = AppService()