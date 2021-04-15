import flask
from main import db
from sqlalchemy.sql.functions import now

class Test(db.Model):
    __tablename__ = "tests"
    __table_args__ = {"schema": "private"}

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('private.questions.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('private.users.id', ondelete="CASCADE"), nullable=False)
    time_started = db.Column(db.DateTime(timezone=False), nullable=False, server_default=now())
    time_submitted = db.Column(db.DateTime(timezone=False))
    user_submitted_query = db.Column(db.String())
    result = db.Column(db.SmallInteger)