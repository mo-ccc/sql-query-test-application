import flask
from models.User import User
from models.Test import Test
from models.Question import Question
import random
from main import db

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

    return flask.jsonify([user.__dict__, test.__dict__, random_question.__dict__])