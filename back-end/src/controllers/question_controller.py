import flask
from models.Question import Question

questions = flask.Blueprint('questions', __name__)

@questions.route('/question/<question_id>', methods=["GET"])
def detail_get_question(question_id):
    question = Question.query.get(question_id)
    return flask.jsonify(question.__dict__)