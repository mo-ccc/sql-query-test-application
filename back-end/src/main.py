import flask

import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()

import flask_migrate
migrate = flask_migrate.Migrate()

import flask_cors
cors = flask_cors.CORS()

import flask_marshmallow
ma = flask_marshmallow.Marshmallow()

def create_app():
    app = flask.Flask(__name__)
    app.config.from_object('default_settings.configuration')
    db.init_app(app)
    migrate.init_app(app, db, include_schemas=True)
    cors.init_app(app)
    ma.init_app(app)

    from controllers import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    from commands import db_custom
    app.register_blueprint(db_custom)

    import os
    from werkzeug.exceptions import HTTPException
    from marshmallow import ValidationError
    from sqlalchemy.exc import ProgrammingError
    if os.getenv("FLASK_ENV") != "development":
        @app.errorhandler(HTTPException)
        def handle_HTTP_error(e):
            return flask.jsonify(error=str(e)), e.code

        @app.errorhandler(ProgrammingError)
        def handle_pyscopg2_error(e):
            return flask.jsonify(error=str(e.orig).split("\n")[0]), 400
        
        @app.errorhandler(ValidationError)
        def handle_validation_error(e):
            return flask.jsonify(error=str(e)), 400

    return app