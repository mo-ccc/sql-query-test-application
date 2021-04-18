import unittest
from main import db, create_app
import commands
import sqlalchemy

class TestBase(unittest.TestCase):
    # ran before every test
    @classmethod
    def setUp(cls):
        # create an app from factory
        cls.app = create_app()
        # force testing configuration with a custom uri
        cls.app.config.from_object('default_settings.Testing')
        test_uri = f"postgresql+psycopg2://postgres:postgres@localhost:5432/testdb"
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = test_uri

        cls.app_context = cls.app.app_context() # app_context is retrieved
        cls.app_context.push() # binds app context to the current context
        cls.client = cls.app.test_client() # test client is made using the app context
        runner = cls.app.test_cli_runner()

        # database setup should occur before db is involved
        runner.invoke(args=["db_custom", "initialize_schema"])
        runner.invoke(args=["db_custom", "seed_question"])
        runner.invoke(args=["db_custom", "seed_secondary_tables"])

        db.drop_all()
        db.create_all()
        
        
        
    # ran after every test
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        db.create_all()
        cls.app_context.pop() # app context is popped from the context