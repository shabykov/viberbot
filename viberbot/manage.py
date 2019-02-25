import logging
import os
from optparse import OptionParser

from .apps import init_app
from .config.urils import get_module


def main():

    settings = get_module(os.getenv('APP_SETTINGS_MODULE', 'config.settings.dev'))

    logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        filename=settings.LOGGING_FILE,
                        filemode='a',
                        level=logging.INFO)

    app = init_app(settings)


if __name__ == "__main__":

    op = OptionParser()
    op.add_option("-s", "--settings", type=str, default=None)
    (opts, args) = op.parse_args()

    if opts.settings is not None:
        os.environ["APP_SETTINGS_MODULE"] = opts.settings

    main()
