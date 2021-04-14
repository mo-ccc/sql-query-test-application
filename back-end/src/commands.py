import flask
from main import db, create_app
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

@db_custom.cli.command('seed_secondary_tables')
def seed_secondary_tables():
    import psycopg2
    import dotenv
    import os
    dotenv.load_dotenv()
    db_name = create_app().config["SQLALCHEMY_DATABASE_URI"].split("/")[-1]
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"), 
            dbname=db_name,
            user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
            port=os.getenv("PORT")
        )
        curs = conn.cursor() # initialize a cursor
        curs.execute("""DROP TABLE IF EXISTS secondary_schema.users;""")
        curs.execute("""DROP TABLE IF EXISTS secondary_schema.google_users;""")
        print("dropped secondary tables")
        curs.execute("""DROP SCHEMA IF EXISTS secondary_schema;""")
        curs.execute("""CREATE SCHEMA IF NOT EXISTS secondary_schema;""")
        curs.execute("""SET search_path TO secondary_schema;""")
        print("created secondary_schema")

        curs.execute(f"""REVOKE CONNECT ON DATABASE {db_name} FROM interactor""")
        curs.execute("""DROP ROLE IF EXISTS interactor;""")
        curs.execute("""CREATE ROLE interactor LOGIN;""")
        curs.execute(f"""ALTER ROLE interactor WITH PASSWORD '{os.getenv("PASSWORD")}'""")
        curs.execute(f"""GRANT CONNECT ON DATABASE {db_name} TO interactor""")
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

    except Exception as e:
        print(e)

    finally:
        if(conn):
            curs.close()
            conn.close()

    