import flask
from .bot.views import viberbot


def init_app():
    app = flask.Flask(__name__)
    app.register_blueprint(viberbot)
    return app
