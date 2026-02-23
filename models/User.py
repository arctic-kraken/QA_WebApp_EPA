from db import db
from sqlalchemy import Sequence

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, Sequence('User_seq', start=1), primary_key=True)
    name = db.Column('name', db.String(50), nullable=False, unique=True)
    password = db.Column('password', db.Text, nullable=False)