from db import db
from sqlalchemy import Sequence

class BudgetSummary(db.Model):
    __tablename__ = 'BudgetSummary'
    id = db.Column(db.Integer, Sequence('budget_summary_seq', start=1), primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('Account.id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey('Budget.id'), nullable=False)
    month_no = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_money_in = db.Column(db.Float, nullable=True)
    total_money_out = db.Column(db.Float, nullable=True)
    latest_balance = db.Column(db.Float, nullable=True)
    starting_balance = db.Column(db.Float, nullable=True)