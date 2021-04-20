import flask
from main import db, create_app
from datetime import datetime, timedelta, date

import dotenv
import os
dotenv.load_dotenv()

db_custom = flask.Blueprint('db_custom', __name__)

# will try to create the schema
# if it fails will check error to ensure it is because schema exists
# if the schema existed will print it did
# or will print the actual error that occurred
@db_custom.cli.command('initialize_schema')
def initialize_schema():
    from psycopg2.errors import DuplicateSchema
    try:
        db.session.execute("""CREATE SCHEMA private;""")
        db.session.commit()
        print("schema_initialized")
    except Exception as e:
        if isinstance(e.orig, DuplicateSchema):
            print("schema already exists")
        else:
            print(e)

# drops all tables in private schema and secondary_schema 
@db_custom.cli.command('drop_tables')
def drop_db():
    db.drop_all()
    db.session.execute("DROP TABLE IF EXISTS alembic_version;")
    db.session.execute("DROP TABLE IF EXISTS secondary_schema.users;")
    db.session.execute("DROP TABLE IF EXISTS secondary_schema.google_users;")
    db.session.commit()
    print("dropped all tables")

# adds a question to the question table. use this after dropping all tables.
@db_custom.cli.command('seed_question')
def seed_question():
    from models.Question import Question
    from validation_schemas.QuestionSchema import QuestionSchema
    import json
    directory = os.path.dirname(__file__)
    with open(os.path.join(directory, 'dumps/questions.json')) as f:
        questions = json.load(f)
        for question in questions:
            db.session.add(Question(**question))
            db.session.flush()
            print("added")
        db.session.commit()
    

@db_custom.cli.command('seed_secondary_tables')
def seed_secondary_tables():
    db.session.execute("""DROP TABLE IF EXISTS secondary_schema.users;""")
    db.session.execute("""DROP TABLE IF EXISTS secondary_schema.google_users;""")
    print("dropped secondary tables")
    db.session.execute("""DROP SCHEMA IF EXISTS secondary_schema;""")
    db.session.execute("""CREATE SCHEMA IF NOT EXISTS secondary_schema;""")
    db.session.execute("""SET search_path TO secondary_schema;""")
    db.session.commit()
    print("created secondary_schema")
    try:
        db.session.execute(f"""REVOKE CONNECT ON DATABASE {os.getenv("DB_NAME")} FROM interactor;""")
        db.session.execute("""DROP ROLE interactor;""")
        db.session.commit()
    except Exception as e:
        print(e)
        print("interactor role does not exist. will be created")
        db.session.rollback()
    
    db.session.execute("""CREATE ROLE interactor LOGIN;""")
    db.session.execute(f"""ALTER ROLE interactor WITH PASSWORD '{os.getenv("PASSWORD")}'""")
    db.session.execute(f"""GRANT CONNECT ON DATABASE {os.getenv("DB_NAME")} TO interactor""")
    db.session.execute("""GRANT USAGE ON SCHEMA secondary_schema TO interactor;""")
    print("created interactor role with permissions")

    db.session.execute("""CREATE TABLE IF NOT EXISTS
    google_users(id INTEGER PRIMARY KEY, user_id INTEGER, browser_language VARCHAR, created_on TIMESTAMP WITHOUT TIME ZONE, device_cat VARCHAR);
    """)

    db.session.execute("""CREATE TABLE IF NOT EXISTS
    users(user_id INTEGER PRIMARY KEY, is_activated BOOLEAN, signed_up_on TIMESTAMP WITHOUT TIME ZONE, last_login TIMESTAMP WITHOUT TIME ZONE, sign_up_source VARCHAR, unsubscribed INTEGER, user_type INTEGER);
    """)
    print("created secondary tables")

    db.session.execute("""GRANT SELECT ON secondary_schema.users, secondary_schema.google_users TO interactor;""")
    print("gave select permissions on secondary tables to interactor")
    db.session.commit()
    
    with db.session.connection().connection.cursor() as raw_curs:
        with open('./dumps/google_users.txt', 'r') as f:
            raw_curs.copy_expert("""COPY secondary_schema.google_users FROM STDIN""", f)

        with open('./dumps/users.txt', 'r') as f:
            raw_curs.copy_expert("""COPY secondary_schema.users FROM STDIN""", f)
    db.session.commit()
    print("dumped data to secondary tables successfully")

    