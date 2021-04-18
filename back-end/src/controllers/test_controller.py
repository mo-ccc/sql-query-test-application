import flask
from main import db
from models.Test import Test
from validation_schemas.TestSchema import TestSchema

import os
import json
import datetime
from sqlalchemy.sql.functions import now

tests = flask.Blueprint('tests', __name__)

# function to run queries on secondary_schema and return results
def run_queries(*queries):
    # session creation with interactor role
    binding = db.get_engine(bind="secondary_schema")
    sess = db.create_scoped_session(options = {'bind': binding})
    # use secondary_schema
    sess.execute("SET search_path TO secondary_schema;")

    results = []
    for query in queries:
        # initialize an output dict
        result = {}
        result_curs = sess.execute(query)
        # keys = columns
        result["keys"] = result_curs.keys()._keys
        # list comprehension to package up arrays of columns in an array of rows
        result["rows"] = [[c for c in r] for r in result_curs.fetchall()]
        result["issues"] = {}
        results.append(result)

    return results

@tests.route('/test/<test_id>', methods=["GET"])
def detail_get_test(test_id):
    test = Test.query.get(test_id)
    return flask.jsonify(TestSchema().dump(test))

@tests.route('/test/<test_id>/execute', methods=["POST"])
def execute_query_on_db(test_id):
    user_submitted, answer = run_queries(
        flask.request.json["query"], Test.query.get(test_id).question.answer_as_query
    )
    # compare query_as_answer with user submitted
    # then produce feedback text etc
    if flask.jsonify(user_submitted["rows"]).get_json() == flask.jsonify(answer["rows"]).get_json():
        user_submitted["matches"] = True # if they match, matches is set to true
    else:
        user_submitted["matches"] = False
        for x in ["rows", "keys"]:
            if len(answer[x]) != len(user_submitted[x]):
                user_submitted["issues"][x] = len(answer[x])

    return flask.jsonify(user_submitted)


@tests.route('/test/<test_id>/submit', methods=["POST"])
def submit_query_for_marking(test_id):
    test = Test.query.get(test_id)
    if test.time_submitted:
        return flask.abort(400, description="test already submitted")

    user_query = flask.request.json["query"]
    
    user_submitted = None
    try:
        user_submitted, answer = run_queries(
            user_query, test.question.answer_as_query
        )
    except:
        pass

    test.result = 0
    if user_submitted and flask.jsonify(user_submitted["rows"]).get_json() == flask.jsonify(answer["rows"]).get_json():
        test.result = 1
            
    test.time_submitted = now()
    test.user_submitted_query = user_query
    
    db.session.commit()
    return flask.jsonify(TestSchema().dump(test))
        