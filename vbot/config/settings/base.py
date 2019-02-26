import logging

LOGGING_FILE = None

logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    filename=LOGGING_FILE,
                    filemode='a',
                    level=logging.INFO)
