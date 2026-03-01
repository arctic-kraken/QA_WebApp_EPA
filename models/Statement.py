from db import db
from sqlalchemy import Sequence

class Statement(db.Model):
    __tablename__ = 'Statement'
    id = db.Column(db.Integer, Sequence('statement_seq', start=1), primary_key=True)
    account_id = db.Column('account_id', db.Integer, nullable=False)
    name = db.Column('name', db.String(255), nullable=True)
    reference = db.Column('reference', db.String(255), nullable=False)
    trx_count = db.Column('trx_count', db.Integer, nullable=True)
    money_in_total = db.Column('money_in_total', db.Float, nullable=True)
    money_out_total = db.Column('money_out_total', db.Float, nullable=True)
    date_oldest = db.Column('date_oldest', db.DateTime, nullable=True)
    date_newest = db.Column('date_newest', db.DateTime, nullable=True)
    upload_date = db.Column('upload_date', db.DateTime, nullable=True)
    uploaded_by_user_id = db.Column('uploaded_by_user_id', db.Integer, nullable=True)