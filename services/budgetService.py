from db import db
import json
from models.Budget import Budget
from models.Account import Account


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


budget_service = BudgetService()
