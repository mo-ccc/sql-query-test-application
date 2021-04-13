import flask
from models.User import User

users = flask.Blueprint('users', __name__)

@users.route('/user', methods=["POST"])
def register():
    print(flask.request.json)