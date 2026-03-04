from db import db
import json
from models.Budget import Budget
from models.Account import Account
from models.BudgetSummary import BudgetSummary
from models.StatementTrx import StatementTrx
from models.Statement import Statement


class BudgetService:

    def get(self, budget_id, account_id):
        budget = Budget.query.filter_by(id=budget_id, account_id=account_id).first()
        if budget is None:
            return None, None, ["Failed to get this budget for this account"]

        try:
            clauses = []
            if budget.capture_clause_json is not None:
                clauses = json.loads(budget.capture_clause_json)['clauses']

            return budget, clauses, []
        except Exception as e:
            return None, None, ["Failed to get this budget for this account"]

    def create(self, account_id):
        try:
            new_budget = Budget()
            new_budget.account_id = account_id
            new_budget.name = "New Budget"
            new_budget.monthly_amount_limit = 0
            new_budget.capture_clause_json = json.dumps({"clauses": []})

            db.session.add(new_budget)
            db.session.commit()
            db.session.refresh(new_budget)

            return new_budget.id
        except Exception as e:
            return None

    def get_budgets_for_account(self, account_id):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return None, ["Failed to get all budgets for this account"]

        all_budgets = Budget.query.filter_by(account_id=account_id).all()
        if all_budgets is None:
            return None, ["Failed to get all budgets for this account"]

        return all_budgets, None

    def update(self, budget_id, account_id, new_name, new_limit, json_clauses):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return False, ["Failed to get this budget for this account"]

        budget = Budget.query.filter_by(id=budget_id, account_id=account_id).first()
        if budget is None:
            return False, ["Failed to get this budget for this account"]

        # TODO validation
        try:
            clauses = json.loads(json_clauses)
            # validation of above

            budget.name = new_name
            budget.monthly_amount_limit = new_limit
            budget.capture_clause_json = json.dumps(clauses)

            db.session.commit()
            db.session.refresh(budget)
        except Exception as e:
            return False, [f"Failed to update this budget - {e}"]

        return True, None

    def delete(self, budget_id, account_id):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return False, ["Failed to get this budget for this account"]

        budget = Budget.query.filter_by(id=budget_id, account_id=account_id).first()
        if budget is None:
            return False, ["Failed to get this budget for this account"]

        try:
            db.session.delete(budget)
            db.session.commit()
        except Exception as e:
            return False, [f"Failed to delete this budget - {e}"]

        return True, None

    def calculate_monthly_budget_summary(self, account_id: int, budget_id: int, month: int, year: int):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return False, ["Failed to get this budget for this account"]

        budget, clause, errors = self.get(budget_id, account_id)
        if budget is None:
            return False, errors

        year_in_next_month = year
        next_month = int(month) + int(1)
        if next_month > 12:
            year_in_next_month = int(year) + int(1)
            next_month = 1

        update = True
        try:
            summary = BudgetSummary.query.filter_by(budget_id=budget.id, account_id=account.id, month_no=month, year=year).first()
            if summary is None:
                update = False
                summary = BudgetSummary()

            summary.account_id = account.id
            summary.budget_id = budget.id
            summary.month_no = month
            summary.year = year
            summary.total_money_in = 0
            summary.total_money_out = 0
            summary.starting_balance = 0
            summary.latest_balance = 0
            for text in clause:
                trxs = (db.session.query(StatementTrx).join(Statement, Statement.id == StatementTrx.statement_id)
                        .filter(Statement.account_id == account.id, StatementTrx.date >= f"{year}-{month}-01",
                                StatementTrx.date < f"{year_in_next_month}-{next_month}-01", StatementTrx.description.like(f"%{text}%")).all())

                summary.total_money_in += sum(trx.money_in for trx in trxs if trx.money_in is not None)
                summary.total_money_out += sum(trx.money_out for trx in trxs if trx.money_out is not None)

            if update is False:
                db.session.add(summary)

            db.session.commit()
        except Exception as e:
            return False, [f"Failed to calculate summary - {e}"]

        return True, []

    def calc_all_budget_summaries(self, account_id: int, month: int, year: int):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return False, ["Failed to get calculate summaries for this account"]

        budgets = Budget.query.filter_by(account_id=account_id).all()
        if budgets is None:
            return False, ["No Budgets for calculations found"]

        for budget in budgets:
            result, errors = self.calculate_monthly_budget_summary(account.id, budget.id, month, year)
            if result is False:
                return False, errors

        return True, []

    def get_all_budget_summaries(self, account_id: int, month: int, year: int):
        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return None, False, ["Failed to get budget summaries for this account"]

        budgets = Budget.query.filter_by(account_id=account_id).all()
        if budgets is None:
            return None, False, ["No Budget with Summaries found"]

        summaries = BudgetSummary.query.filter_by(account_id=account_id, month_no=month, year=year).all()
        if summaries is None:
            return None, False, ["No Budget Summaries found"]

        return summaries, True, []

    def get_budget_summary(self, budget_id: int, account_id: int, month: int, year: int):
        summary = BudgetSummary.query.filter_by(budget_id=budget_id, account_id=account_id, month_no=month, year=year).first()

        return summary

    def get_budget_summaries_view_models(self, account_id: int, month: int, year: int):
        budgets, errors = self.get_budgets_for_account(account_id)
        viewmodel = []

        for budget in budgets:
            summary = self.get_budget_summary(budget.id, account_id, month, year)
            if summary is None:
                continue

            model = SummaryViewModel()
            model.budget_name = budget.name
            model.budget_limit = budget.monthly_amount_limit
            model.total_in = summary.total_money_in
            model.total_out = summary.total_money_out
            viewmodel.append(model)

        return viewmodel


class SummaryViewModel:
    budget_name: str
    budget_limit: float
    total_in: float
    total_out: float

budget_service = BudgetService()
