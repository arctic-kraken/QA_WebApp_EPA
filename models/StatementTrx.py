from db import db
from sqlalchemy import Sequence

class StatementTrx(db.Model):
    __tablename__ = 'StatementTrx'
    id = db.Column(db.Integer, Sequence('statementtrx_seq', start=1), primary_key=True)
    statement_id = db.Column('statement_id', db.Integer, nullable=False)
    description = db.Column('description', db.String(50), nullable=True)
    date = db.Column('date', db.DateTime, nullable=True)
    money_in = db.Column('money_in', db.Float, nullable=True)
    money_out = db.Column('money_out', db.Float, nullable=True)
    balance = db.Column('balance', db.Float, nullable=True)
    #budget_id = db.Column('budget_id', db.Integer, nullable=True)