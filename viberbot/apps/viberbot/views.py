import logging
import flask

from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import (ViberFailedRequest,
                                         ViberMessageRequest,
                                         ViberSubscribedRequest)

from .middlewares import viber_api


viberbot = flask.Blueprint('viberbot', __name__)


def web_hook(bot_api):
    logging.debug("received request. post data: {0}".format(flask.request.get_data()))

    if not bot_api.verify_signature(flask.request.get_data(), flask.request.headers.get('X-Viber-Content-Signature')):
        return flask.Response(status=403)

    viber_request = bot_api.parse_request(flask.request.get_data())
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message

        bot_api.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        bot_api.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.info("client failed receiving message. failure: {0}".format(viber_request))
    return flask.Response(status=200)


viberbot.add_url_rule('/', view_func=web_hook, methods=['POST'])
