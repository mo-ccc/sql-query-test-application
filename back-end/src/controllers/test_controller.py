import flask
from models.Test import Test
from validation_schemas.TestSchema import TestSchema

tests = flask.Blueprint('tests', __name__)

@tests.route('/test/<test_id>', methods=["GET"])
def detail_get_test(test_id):
    test = Test.query.get(test_id)
    return flask.jsonify(TestSchema().dump(test))

@tests.route('/test/<test_id>/execute', methods=["POST"])
def execute_query_on_db(test_id):
    pass

@tests.route('/test/<test_id>/submit', methods=["POST"])
def submit_query_for_marking(test_id):
    pass