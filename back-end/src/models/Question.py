import flask
from main import db


class Question():
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(), nullable=False)
    answer_as_query = db.Column(db.String(), nullable=False)