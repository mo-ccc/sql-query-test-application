import flask
from werkzeug.exceptions import HTTPException

import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()

import flask_migrate
migrate = flask_migrate.Migrate()

def create_app():
    app = flask.Flask(__name__)
    app.config.from_object('default_settings.configuration')
    db.init_app(app)
    migrate.init_app(app, db)

    from controllers import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    from commands import db_custom
    app.register_blueprint(db_custom)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return flask.jsonify(error=str(e)), code

    return app