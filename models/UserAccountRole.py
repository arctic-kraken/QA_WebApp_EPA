from db import db
from sqlalchemy import Sequence

class UserAccountRole(db.Model):
    __tablename__ = 'UserAccountRole'
    id = db.Column(db.Integer, Sequence('role_seq', start=1), primary_key=True)
    user_id = db.Column('user_id', db.Integer, nullable=False)
    account_id = db.Column('account_id', db.Integer, nullable=False)
    is_admin = db.Column('is_admin', db.Boolean, nullable=False, default=False)