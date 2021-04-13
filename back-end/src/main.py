import flask
from werkzeug.exceptions import HTTPException

import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()

def create_app():
    app = flask.Flask(__name__)
    db.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return flask.jsonify(error=str(e)), code

    return app