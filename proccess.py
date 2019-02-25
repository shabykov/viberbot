from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
import logging

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


app = Flask(__name__)

viber = Api(BotConfiguration(
    name='norniktest',
    avatar='https://upload.wikimedia.org/wikipedia/ru/7/76/%D0%9B%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF_%D0%9D%D0%BE%D1%80%D0%BD%D0%B8%D0%BA%D0%B5%D0%BB%D1%8C.png',
    auth_token='494908ba3727d304-a5457dfdf68fe853-bcb7cf10d0f7fc54'
))


# viber.set_webhook('https://a99f9e9f.ngrok.io:433')


@app.route('/info/', methods=['GET'])
def info():
    return Response(status=200)


@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=context)
