import os
from optparse import OptionParser

from vbot.apps import init_app
from vbot.config import settings


def run_app():
    app = init_app()
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG, ssl_context=settings.SSL_CONTEXT)


if __name__ == "__main__":

    op = OptionParser()

    op.add_option("-s", "--settings", type=str, default=None)
    (opts, args) = op.parse_args()

    if opts.settings is not None:
        os.environ.setdefault("APP_SETTINGS_MODULE", opts.settings)

    run_app()
