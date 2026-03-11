from db import db

from sqlalchemy import Sequence, Uuid

class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, Sequence('account_seq', start=1), primary_key=True)
    name = db.Column('name', db.String(10), nullable=False)
    reference = db.Column('reference', db.String(255), nullable=True)
    date_created = db.Column('date_created', db.DateTime, default=db.func.now(), nullable=True)
    currency_code = db.Column('currency_code', db.String(3), default="GBP")
    latest_invite_code = db.Column('latest_invite_code', Uuid(as_uuid=True), nullable=True)
    last_invite_created_date = db.Column('last_invite_created_date', db.DateTime, nullable=True)


