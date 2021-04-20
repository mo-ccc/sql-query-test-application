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
        # force testing configuration
        cls.app.config["TESTING"] = True
        cls.app.config["DEBUG"] = True

        cls.app_context = cls.app.app_context() # app_context is retrieved
        cls.app_context.push() # binds app context to the current context
        cls.client = cls.app.test_client() # test client is made using the app context
        runner = cls.app.test_cli_runner()

        # private schema setup should occur before db is involved
        runner.invoke(args=["db_custom", "initialize_schema"])
        # drops all tables currently in db
        runner.invoke(args=["db_custom", "drop_tables"])
        # then create all tables again and seed db
        db.create_all()
        runner.invoke(args=["db_custom", "seed_question"])
        runner.invoke(args=["db_custom", "seed_secondary_tables"])
        
        db.session.add(User(email="test@email.com"))
        db.session.flush()
        db.session.add(Test(user_id=1, question_id=1))
        db.session.commit()
        
    # ran after every test
    @classmethod
    def tearDown(cls):
        db.session.remove()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db_custom", "drop_tables"])
        db.create_all()
        cls.app_context.pop() # app context is popped from the context