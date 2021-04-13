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
    user = User.query.filter(User.email==flask.request.json["email"]).first()
    if not user:
        user = User()
        user.email = flask.request.json["email"]
        db.session.add(user)
        db.session.commit()

    questions = Question.query.all()
    if not questions:
        flask.abort(500, description='no questions exist')

    random_question = random.choice(Question.query.all())
    print(random_question)

    test = Test()
    test.user_id = user.id
    test.question_id = random_question.id
    db.session.add(test)
    db.session.commit()

    output = UserSchema().dump(user)
    output["tests"] = TestSchema(exclude=("question",)).dump(test)
    return flask.jsonify(output)