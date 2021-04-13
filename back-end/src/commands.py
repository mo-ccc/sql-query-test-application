import flask
from main import db
from datetime import datetime, timedelta, date

db_custom = flask.Blueprint('db_custom', __name__)

@db_custom.cli.command('drop')
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("dropped all tables")
