from db import db
from sqlalchemy import Sequence

class Budget(db.Model):
    __tablename__ = 'Budget'
    id = db.Column(db.Integer, Sequence('budget_seq', start=1), primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('Account.id'), nullable=False)
    name = db.Column('name', db.String(255), nullable=True)
    monthly_amount_limit = db.Column('monthly_amount_limit', db.Float, nullable=True)
    capture_clause_json = db.Column('capture_clause_json', db.JSON, nullable=True)