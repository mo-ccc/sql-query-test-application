import flask
from main import db

from models.User import User
from models.Test import Test
from models.Question import Question

from validation_schemas.UserSchema import UserSchema
from validation_schemas.TestSchema import TestSchema
from validation_schemas.QuestionSchema import QuestionSchema

import random

users = flask.Blueprint('users', __name__)

@users.route('/user', methods=["POST"])
def register():
    # retrieve a user from the database with the same email if it exists
    user = User.query.filter(User.email==flask.request.json["email"]).first()
    # other wise create the user
    if not user:
        user = User()
        user.email = UserSchema(only=("email")).load(flask.request.json)
        db.session.add(user)
        db.session.commit()

    # query all the records within the questions table
    questions = Question.query.all()
    # abort entire operation if there are no records
    if not questions:
        flask.abort(500, description='no questions exist')

    # select a random question from the many
    random_question = random.choice(Question.query.all())

    # initializes a new test belonging to the user with the question attached
    test = Test()
    test.user_id = user.id
    test.question_id = random_question.id
    db.session.add(test)
    db.session.commit()

    # return the json containing the user data and the test id
    output = UserSchema().dump(user)
    output["tests"] = [TestSchema(only=("id",)).dump(test)]
    return flask.jsonify(output)