from db import db
from sqlalchemy import Sequence

class Currency(db.Model):
    __tablename__ = 'Currency'
    id = db.Column(db.Integer, Sequence('currency_seq', start=1), primary_key=True)
    code = db.Column('name', db.String(3), nullable=False, unique=True)