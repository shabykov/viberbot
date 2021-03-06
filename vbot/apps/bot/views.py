import json
import logging

import flask
from viberbot import Api, BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import (ViberFailedRequest,
                                         ViberMessageRequest,
                                         ViberSubscribedRequest)

from vbot.config import settings

viberbot = flask.Blueprint('vbot', __name__)

viberbot_api = Api(BotConfiguration(
    name=settings.VIBER_BOT_NAME,
    avatar=settings.VIBER_BOT_AVATAR,
    auth_token=settings.VIBER_BOT_AUTH_TOKEN
))


def incoming_view():
    logging.info("Event: {0}".format(flask.request.get_data()))
    logging.info("Signature: {0}".format(flask.request.headers.get('X-Viber-Content-Signature')))

    if not viberbot_api.verify_signature(flask.request.get_data(),
                                         flask.request.headers.get('X-Viber-Content-Signature')):
        return flask.Response(status=403)

    viber_request = viberbot_api.parse_request(flask.request.get_data())
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message

        viberbot_api.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viberbot_api.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.info("client failed receiving message. failure: {0}".format(viber_request))
    return flask.Response(status=200)


def set_webhook_view():
    try:
        data = json.loads(flask.request.get_data().decode('utf-8'))
    except Exception as error:
        logging.error('input data parse error {}'.format(error))
        data = {}

    webhook = data.get('webhook')
    try:
        if webhook is not None:
            viberbot_api.set_webhook(url=webhook)
        else:
            viberbot_api.set_webhook(url=settings.VIBER_BOT_WEBHOOK)
    except Exception as error:
        logging.error("Error: {}".format(error))
        return flask.Response(status=404)

    return flask.jsonify(message='WebHook успешно задан', account=viberbot_api.get_account_info())


def verify_signature_view():
    logging.info(flask.request.get_data())
    return flask.jsonify({
        'X-Viber-Content-Signature': viberbot_api._calculate_message_signature(flask.request.get_data()),
        'X-Viber-Content-Signature-Is-True': viberbot_api.verify_signature(flask.request.get_data(),
                                                                           flask.request.headers.get(
                                                                               'X-Viber-Content-Signature')),
        'message': flask.request.get_data().decode('utf-8')})


def replace_auth_token_view():
    try:
        data = json.loads(flask.request.get_data().decode('utf-8'))
    except Exception as error:
        logging.error('input data parse error {}'.format(error))
        data = {}

    name = data.get('name')
    avatar = data.get('avatar')
    auth_token = data.get('token')
    webhook = data.get('webhook')

    if auth_token is not None and name is not None and avatar is not None:
        try:

            viberbot_api = Api(BotConfiguration(name=name, avatar=avatar, auth_token=auth_token))
            viberbot_api.set_webhook(url=webhook)

            resp = flask.jsonify(message='Auth token успешно заменен', account=viberbot_api.get_account_info())
            resp.status_code = 200
            return resp

        except Exception as error:
            logging.error('replace auth token error: {}'.format(error))
            resp = flask.jsonify(error='Auth token не удалось замененить ')
            resp.status_code = 404
            return resp

    resp = flask.jsonify(message='некорректные входные данные {}'.format(flask.request.get_data()))
    resp.status_code = 404
    return resp


viberbot.add_url_rule('/', view_func=incoming_view, methods=['POST'])
viberbot.add_url_rule('/set_webhook', view_func=set_webhook_view, methods=['POST'])
viberbot.add_url_rule('/verify_signature', view_func=verify_signature_view, methods=['POST'])
viberbot.add_url_rule('/replace_auth_token', view_func=replace_auth_token_view, methods=['POST'])
