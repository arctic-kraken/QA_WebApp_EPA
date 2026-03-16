from flask import session, abort
import datetime, re, hashlib, dotenv

class AppService:
    validation_regex_pattern = r"[^\w\s@$!%*#?&.-]|\b(or|and|select|from|where|delete|insert)\b"
    CONST_REGEX_ERROR_MSG = "must only contain letters, numbers and these special characters: @$!%*#?&.-"

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

    def get_month_name(self, month, year):
        m_datetime = datetime.datetime(year=int(year), month=int(month), day=1)
        return m_datetime.strftime("%B")

    def validate_user_input(self, user_input: str, pattern = None):
        pattern = self.validation_regex_pattern if pattern is None else pattern

        return True if re.search(pattern, user_input, flags=re.I|re.M) is None else False

    def encrypt(self, text: str) -> str:
        return hashlib.sha256(f"{text}{dotenv.get_key(".env", "HASH_SALT")}".encode("utf8")).hexdigest()


app_service = AppService()