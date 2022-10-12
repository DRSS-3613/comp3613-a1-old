import flask_login
from flask_jwt import JWT
from App.models import Admin, Reviewer


def authenticate(username, password):
    user = Admin.query.filter_by(username=username).first()
    if not user:
        user = Reviewer.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    user = Admin.query.get(payload["identity"])
    if not user:
        user = Reviewer.query.get(payload["identity"])
    if user:
        return user
    return None


def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)


def logout_user():
    flask_login.logout_user()


def setup_jwt(app):
    return JWT(app, authenticate, identity)


def load_user_from_id(id):
    user = Admin.query.get(id)
    if not user:
        user = Reviewer.query.get(id)
    return user
