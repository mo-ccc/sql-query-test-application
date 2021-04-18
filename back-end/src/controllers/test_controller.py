import flask
from main import db
from models.Test import Test
from validation_schemas.TestSchema import TestSchema

tests = flask.Blueprint('tests', __name__)

import os
import json
import datetime

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__() # converts date time to string

@tests.route('/test/<test_id>', methods=["GET"])
def detail_get_test(test_id):
    test = Test.query.get(test_id)
    return flask.jsonify(TestSchema().dump(test))

@tests.route('/test/<test_id>/execute', methods=["POST"])
def execute_query_on_db(test_id):
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

    result_curs = sess.execute(flask.request.json["query"])
    result["keys"] = result_curs.keys()._keys
    result["rows"] = [[c for c in r] for r in result_curs.fetchall()]
    
    
    # # runs the query_as_answer and compares results with user submitted
    
    answer_result = sess.execute(question_answer)
    
    answer["keys"] = answer_result.keys()._keys
    answer["rows"] = [[c for c in r] for r in answer_result.fetchall()]
    print(answer)

    if flask.jsonify(result["rows"]).get_json() == flask.jsonify(answer["rows"]).get_json():
        result["matches"] = True # if they match, matches is set to true
        result["message"] = "correct"
    else:
        result["matches"] = False
        result["message"] = f"was expecting {len(answer['rows'])} rows and {len(answer['keys'])} columns"

    return flask.jsonify(result)


@tests.route('/test/<test_id>/submit', methods=["POST"])
def submit_query_for_marking(test_id):
    pass