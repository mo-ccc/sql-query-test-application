import flask
from models.Test import Test
from validation_schemas.TestSchema import TestSchema

tests = flask.Blueprint('tests', __name__)

import psycopg2
from psycopg2.extras import RealDictCursor
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
    try:
        question_answer = Test.query.get(test_id).question.answer_as_query
        result = {}

        conn = psycopg2.connect(
            host=os.getenv("HOST"), 
            dbname=flask.current_app.config["SQLALCHEMY_DATABASE_URI"].split("/")[-1],
            user="interactor", password=os.getenv("PASSWORD"),
            port=os.getenv("PORT")
        )

        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("""SET search_path TO secondary_schema;""")
            curs.execute(flask.request.json["query"])
            result["result_set"] = json.dumps(curs.fetchall(), default=myconverter)
        
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("""SET search_path TO secondary_schema;""")
            curs.execute(question_answer)
            result2 = json.dumps(curs.fetchall(), default=myconverter)
            
            if result["result_set"] == result2:
                result["matches"] = True
            else:
                result["matches"] = False
        return flask.jsonify(result)

    except Exception as e:
        print(e)
    return 'null'


@tests.route('/test/<test_id>/submit', methods=["POST"])
def submit_query_for_marking(test_id):
    pass