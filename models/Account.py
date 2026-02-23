from db import db
from uuid import uuid4
from sqlalchemy import Sequence, Uuid

class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer, Sequence('account_seq', start=1), primary_key=True)
    name = db.Column('name', db.String(10), nullable=False)
    reference = db.Column('reference', db.String(255), nullable=True)
    date_created = db.Column('date_created', db.DateTime, default=db.func.now(), nullable=True)
    starting_date = db.Column('starting_date', db.DateTime, default=db.func.now(), nullable=True)
    #current_balance = db.Column('current_balance', db.Integer, default=0)
    currency_id = db.Column('currency_id', db.Integer, default=0)
    latest_invite_code = db.Column('latest_invite_code', Uuid(as_uuid=True), nullable=True)
    last_invite_created_date = db.Column('last_invite_created_date', db.DateTime, nullable=True)

# TODO do account name formatting

