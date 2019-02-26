import flask
import viberbot

from .bot.views import viberbot as vb


def init_app(settings):

    app = flask.Flask(__name__)

    bot_api = viberbot.Api(viberbot.BotConfiguration(
        name=settings.VIBER_BOT_NAME,
        avatar=settings.VIBER_BOT_AVATAR,
        auth_token=settings.VIBER_BOT_AUTH_TOKEN
    ))

    app.register_blueprint(vb)
    return app
