import os

os.environ.setdefault("APP_SETTINGS_MODULE", "vbot.config.settings.heroku")

from .utils import *

settings = get_module(os.getenv('APP_SETTINGS_MODULE'))
