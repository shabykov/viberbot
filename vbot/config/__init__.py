import os

from .urils import *

settings = get_module(os.getenv('APP_SETTINGS_MODULE', 'config.settings.dev'))
