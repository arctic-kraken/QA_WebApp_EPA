from db import db
from models.Account import Account

from models.User import User
from models.UserAccountRole import UserAccountRole
from services.accountService import account_service
from datetime import datetime
from models.StatementTrx import StatementTrx
from models.Statement import Statement
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

# only for debug
import traceback

class StatementService:
    def upload_file(self, file: FileStorage, user_id: int, account_id: int):
        try:
            if file.mimetype != "text/csv":
                raise Exception("Please upload a '.csv' file")

            new_statement = Statement()
            new_statement.account_id = account_id
            new_statement.reference = secure_filename(file.filename)[:255]
            new_statement.upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_statement.uploaded_by_user_id = user_id

            # if there is less than a header and 1 trx in the file then quit
            if len(file.stream.readlines()) < 2:
                raise Exception("File is empty - make sure there is at least a header row and 1 transaction row")

            trxs = []
            file.stream.seek(0)
            firstline = file.stream.readlines()[0]
            firstline_clean = firstline.decode('utf-8').strip()

            headers = firstline_clean.split(',')
            trx_headers = self.map_file_headers_to_trx_headers(headers)

            decimal_places = 2

            file.stream.seek(len(firstline))
            for line in file.stream.readlines():
                cols = line.decode('utf-8')[:-2].split(',')
                new_trx = StatementTrx()
                new_trx.description = cols[trx_headers['Description']]
                # TODO figure out bullet-proof date format
                new_trx.date = datetime.strptime(cols[trx_headers['Date']], "%Y-%m-%d %H:%M:%S")
                new_trx.balance = round(float(cols[trx_headers['Balance']]), decimal_places)

                if "Amount" in headers:
                    if float(cols[headers.index("Amount")]) < 0:
                        new_trx.money_out = round(float(cols[trx_headers['Money Out']]), decimal_places)
                    else:
                        new_trx.money_in = round(float(cols[trx_headers['Money In']]), decimal_places)
                else:
                    new_trx.money_in = round(float(cols[trx_headers['Money In']]), decimal_places)
                    new_trx.money_out = round(float(cols[trx_headers['Money Out']]), decimal_places)

                trxs.append(new_trx)

            new_statement, trxs = self.calculate_statement_totals(new_statement, trxs)

            db.session.add(new_statement)
            db.session.commit()
            db.session.refresh(new_statement)

            for trx in trxs:
                trx.statement_id = new_statement.id

            db.session.add_all(trxs)
            db.session.commit()

            return True, None
        except Exception as e:
            return False, f"{e}"

    def sortTrxsByDate(self, e):
        return e.date

    def map_file_headers_to_trx_headers(self, header_list):
        mapped_headers: dict = {}
        if "Description" in header_list:
            mapped_headers["Description"] = header_list.index("Description")

        if "Balance" in header_list:
            mapped_headers["Balance"] = header_list.index("Balance")

        if "Money In" in header_list:
            mapped_headers["Money In"] = header_list.index("Money In")
        else:
            mapped_headers["Money In"] = header_list.index("Amount")

        if "Money Out" in header_list:
            mapped_headers["Money Out"] = header_list.index("Money Out")
        else:
            mapped_headers["Money Out"] = header_list.index("Amount")

        if "Completed Date" in header_list:
            mapped_headers["Date"] = header_list.index("Completed Date")
        else:
            mapped_headers["Date"] = header_list.index("Date")

        return mapped_headers

    def get_all_statements_for_account(self, account_id):
        return Statement.query.filter_by(account_id=account_id).all()

    def get_statement_with_trxs(self, statement_id, account_id):
        statement = Statement.query.filter_by(id=statement_id, account_id=account_id).first()
        if statement is None:
            return None, None

        trxs = StatementTrx.query.filter_by(statement_id=statement.id).all()
        if trxs is None:
            return None, None

        return statement, trxs

    def update_statement_name(self, statement_id, account_id, new_statement_name):
        statement = Statement.query.filter_by(id=statement_id, account_id=account_id).first()
        if statement is None:
            return False

        # TODO name validation
        if len(new_statement_name) > 255:
            return False, ["Requested name is too long"]

        if len(new_statement_name) < 1:
            return False, ["Requested name is too short"]

        # regex here # plus return the errors

        try:
            statement.name = new_statement_name
            db.session.commit()
        except Exception:
            return False

        return True

    def delete_statement(self, statement_id, account_id):
        statement = Statement.query.filter_by(id=statement_id, account_id=account_id).first()
        if statement is None:
            return False

        try:
            db.session.delete(statement)
            db.session.commit()
        except Exception:
            return False

        return True

    def delete_trx(self, trx_id, account_id):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return False, ["Account not found"]

        statement = Statement.query.filter_by(account_id=account.id).first()
        if statement is None:
            return False, ["Statement not found"]

        trx = StatementTrx.query.filter_by(id=trx_id, statement_id=statement.id).first()
        if trx is None:
            return False, ["Transaction not found"]

        try:
            db.session.delete(trx)
            db.session.commit()

        except Exception:
            return False, ["Failed to delete trx"]

        return self.recalculate_statement(statement)

    def calculate_statement_totals(self, statement: Statement, trxs):
        statement.trx_count = len(trxs)
        statement.money_in_total = sum(trx.money_in for trx in trxs if trx.money_in is not None)
        statement.money_out_total = sum(trx.money_out for trx in trxs if trx.money_out is not None)

        # date oldest
        trxs.sort(key=self.sortTrxsByDate)
        statement.date_oldest = trxs[0].date if 1 < len(trxs) else None
        # date newest
        trxs.sort(reverse=True, key=self.sortTrxsByDate)
        statement.date_newest = trxs[0].date if 1 < len(trxs) else None

        return statement, trxs

    def recalculate_statement(self, statement: Statement):
        try:
            trxs = StatementTrx.query.filter_by(statement_id=statement.id).all()
            self.calculate_statement_totals(statement, trxs)
            db.session.commit()
        except Exception:
            return False, ["Failed to recalculate statement"]

        return True, None

statement_service = StatementService()
