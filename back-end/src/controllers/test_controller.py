import flask
from models.Test import Test

tests = flask.Blueprint('tests', __name__)

@tests.route('/test/<test_id>', methods=["GET"])
def detail_get_test(test_id):
    test = Test.query.get(test_id)
    return flask.jsonify(test.__dict__)