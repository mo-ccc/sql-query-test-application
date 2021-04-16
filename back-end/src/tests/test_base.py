import unittest
from main import db, create_app
import commands
import sqlalchemy

class TestBase(unittest.TestCase):
    # ran before every test
    @classmethod
    def setUp(cls):
        cls.app = create_app() # creates an app
        cls.app.config.from_object('default_settings.Testing') # forces testing configuration
        test_uri = f"postgresql+psycopg2://postgres:postgres@localhost:5432/testdb"
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = test_uri

        # removes the need to create database and schema for testing
        # database and schema must still be created for env declared database
        
        engine = sqlalchemy.create_engine(test_uri)
        # creates schema if not exists
        if not engine.dialect.has_schema(engine, 'private'):
            engine.execute(sqlalchemy.schema.CreateSchema('private'))

        cls.app_context = cls.app.app_context() # app_context is retrieved
        cls.app_context.push() # binds app context to the current context
        cls.client = cls.app.test_client() # test client is made using the app context
        runner = cls.app.test_cli_runner()
        db.drop_all()
        db.create_all()
        
        
        runner.invoke(args=["db_custom", "seed_question"])
        runner.invoke(args=["db_custom", "seed_secondary_tables"])
        
    # ran after every test
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        db.create_all()
        cls.app_context.pop() # app context is popped from the context