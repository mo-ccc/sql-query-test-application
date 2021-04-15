import flask
from main import db


class Question(db.Model):
    __tablename__ = "questions"
    __table_args__ = {"schema": "private"}

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(), nullable=False)
    answer_as_query = db.Column(db.String(), nullable=False)

    tests = db.relationship('Test', backref='question', passive_deletes='all')