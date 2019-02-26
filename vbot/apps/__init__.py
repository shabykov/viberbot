import flask

from vbot.config import settings
from .bot.views import viberbot


def init_app():
    app = flask.Flask(__name__)
    app.register_blueprint(viberbot)
    return app


def execute_from_command_line():
    app = init_app()

    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG, ssl_context=settings.SSL_CONTEXT)