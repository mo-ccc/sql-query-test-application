import unittest
from main import db, create_app
from models.User import User
from models.Test import Test
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

        # secondary tables and private schema setup should occur before db is involved
        runner.invoke(args=["db_custom", "initialize_schema"])
        runner.invoke(args=["db_custom", "seed_secondary_tables"])
        # drops all tables currently in db
        db.drop_all()
        # then create all tables again and seed db with a question
        db.create_all()
        runner.invoke(args=["db_custom", "seed_question"])

        db.session.add(User(email="test@email.com"))
        db.session.flush()
        db.session.add(Test(user_id=1, question_id=1))
        db.session.commit()
        
    # ran after every test
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        db.create_all()
        cls.app_context.pop() # app context is popped from the context