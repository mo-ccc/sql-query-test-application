import flask
from main import db
from datetime import datetime, timedelta, date

db_custom = flask.Blueprint('db_custom', __name__)

@db_custom.cli.command('drop')
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("dropped all tables")

@db_custom.cli.command('seed_question')
def seed_question():
    from models.Question import Question
    question = Question()
    question.prompt = "Write a query to get the number of unique Google users whose last login was in July, 2019, broken down by device type. Show the most used device in that period first."
    question.answer_as_query = "SELECT COUNT(device_cat) from google_users GROUP BY device_cat ORDER BY COUNT(device_cat) desc"
    db.session.add(question)
    db.session.commit()
