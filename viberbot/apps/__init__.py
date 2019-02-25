import flask
import viberbot

from .viberbot.views import viberbot


app = flask.Flask(__name__)


def init_app(setting):
    bot_api = viberbot.Api(viberbot.BotConfiguration(
        name='norniktest',
        avatar='https://upload.wikimedia.org/wikipedia/ru/7/76/%D0%9B%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF_%D0%9D%D0%BE%D1%80%D0%BD%D0%B8%D0%BA%D0%B5%D0%BB%D1%8C.png',
        auth_token='494908ba3727d304-a5457dfdf68fe853-bcb7cf10d0f7fc54'
    ))

    app.register_blueprint(viberbot)
    return app
