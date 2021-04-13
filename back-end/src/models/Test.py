import flask
from main import db
from sqlalchemy.sql.functions import now

class Test():
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    time_started = db.Column(db.DateTime(timezone=False), nullable=False, server_default=now())
    time_submitted = db.Column(db.DateTime(timezone=False))
    user_submitted_query = db.Column(db.String())
    result = db.Column(db.SmallInteger)