import flask
from main import db


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "private"}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), nullable=False, unique=True)

    tests = db.relationship('Test', backref='user', passive_deletes='all')