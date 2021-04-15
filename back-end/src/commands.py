import flask
from main import db, create_app
from datetime import datetime, timedelta, date

import dotenv
import os
dotenv.load_dotenv()

conn_args = {
    "host": os.getenv("HOST"), 
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("USERNAME"), 
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("PORT")
}

db_custom = flask.Blueprint('db_custom', __name__)

@db_custom.cli.command('initialize_schema')
def initialize_schema():
    import psycopg2
    with psycopg2.connect(**conn_args) as conn:
        conn.autocommit = True
        with conn.cursor() as curs:
            curs.execute("""DROP SCHEMA IF EXISTS private;""")
            curs.execute("""CREATE SCHEMA IF NOT EXISTS private;""")
    print("schema_initialized")


@db_custom.cli.command('initialize_db')
def initialize_db():
    import psycopg2
    copy_args = conn_args.copy()
    copy_args["dbname"] = "postgres" # initializing a connect with default dbname instead
    with psycopg2.connect(**copy_args) as conn: # create a connection using ctx manager
        conn.autocommit = True
        with conn.cursor() as curs: # initialize a cursor
            curs.execute(f"""DROP DATABASE IF EXISTS {os.getenv("DB_NAME")};""")
            curs.execute(f"""CREATE DATABASE {os.getenv("DB_NAME")};""")
    initialize_schema()
    print("db initialized")
    

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
    question.answer_as_query = "SELECT COUNT(device_cat) from google_users GROUP BY device_cat ORDER BY COUNT(device_cat) desc;"
    db.session.add(question)
    db.session.commit()

@db_custom.cli.command('seed_secondary_tables')
def seed_secondary_tables():
    import psycopg2
    with psycopg2.connect(**conn_args) as conn:
        with conn.cursor() as curs: # initialize a cursor
            curs.execute("""DROP TABLE IF EXISTS secondary_schema.users;""")
            curs.execute("""DROP TABLE IF EXISTS secondary_schema.google_users;""")
            print("dropped secondary tables")
            curs.execute("""DROP SCHEMA IF EXISTS secondary_schema;""")
            curs.execute("""CREATE SCHEMA IF NOT EXISTS secondary_schema;""")
            curs.execute("""SET search_path TO secondary_schema;""")
            print("created secondary_schema")

            curs.execute(f"""REVOKE CONNECT ON DATABASE {os.getenv("DB_NAME")} FROM interactor""")
            curs.execute("""DROP ROLE IF EXISTS interactor;""")
            curs.execute("""CREATE ROLE interactor LOGIN;""")
            curs.execute(f"""ALTER ROLE interactor WITH PASSWORD '{os.getenv("PASSWORD")}'""")
            curs.execute(f"""GRANT CONNECT ON DATABASE {os.getenv("DB_NAME")} TO interactor""")
            curs.execute("""GRANT USAGE ON SCHEMA secondary_schema TO interactor;""")
            print("created interactor role with permissions")

            curs.execute("""CREATE TABLE IF NOT EXISTS
            google_users(id INTEGER PRIMARY KEY, user_id INTEGER, browser_language VARCHAR, created_on TIMESTAMP WITHOUT TIME ZONE, device_cat VARCHAR);
            """)

            curs.execute("""CREATE TABLE IF NOT EXISTS
            users(user_id INTEGER PRIMARY KEY, is_activated BOOLEAN, signed_up_on TIMESTAMP WITHOUT TIME ZONE, last_login TIMESTAMP WITHOUT TIME ZONE, sign_up_source VARCHAR, unsubscribed INTEGER, user_type INTEGER);
            """)
            print("created secondary tables")

            curs.execute("""GRANT SELECT ON secondary_schema.users, secondary_schema.google_users TO interactor;""")
            print("gave select permissions on secondary tables to interactor")
            conn.commit()
            
            with open('./dumps/google_users.txt', 'r') as f:
                curs.copy_expert("""COPY google_users FROM STDIN""", f)
            conn.commit()

            with open('./dumps/users.txt', 'r') as f:
                curs.copy_expert("""COPY users FROM STDIN""", f)
            conn.commit()
            print("dumped data to secondary tables successfully")

    