import flask
from main import db
from models.Test import Test
from validation_schemas.TestSchema import TestSchema

tests = flask.Blueprint('tests', __name__)

import os
import json
import datetime

def run_query_against(test_id, query):
    # session creation
    binding = db.get_engine(bind="secondary_schema")
    sess = db.create_scoped_session(options = {'bind': binding})
    # use secondary_schema
    sess.execute("SET search_path TO secondary_schema;")

    # retrieves the query_as_answer to run alongside user submitted
    question_answer = Test.query.get(test_id).question.answer_as_query
    # initialize an output dict
    result = {}
    answer = {} 

    result_curs = sess.execute(query)
    result["keys"] = result_curs.keys()._keys
    result["rows"] = [[c for c in r] for r in result_curs.fetchall()]
    result["issues"] = {}

    # # runs the query_as_answer
    answer_result = sess.execute(question_answer)
    answer["keys"] = answer_result.keys()._keys
    answer["rows"] = [[c for c in r] for r in answer_result.fetchall()]

    return result, answer

@tests.route('/test/<test_id>', methods=["GET"])
def detail_get_test(test_id):
    test = Test.query.get(test_id)
    return flask.jsonify(TestSchema().dump(test))

@tests.route('/test/<test_id>/execute', methods=["POST"])
def execute_query_on_db(test_id):
    result, answer = run_query_against(test_id, flask.request.json["query"])
    # compare query_as_answer with user submitted
    # then produce feedback text etc
    if flask.jsonify(result["rows"]).get_json() == flask.jsonify(answer["rows"]).get_json():
        result["matches"] = True # if they match, matches is set to true
    else:
        result["matches"] = False
        for x in ["rows", "keys"]:
            if len(answer[x]) != len(result[x]):
                result["issues"][x] = len(answer[x])

    return flask.jsonify(result)


@tests.route('/test/<test_id>/submit', methods=["POST"])
def submit_query_for_marking(test_id):
    pass