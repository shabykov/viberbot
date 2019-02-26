import os


from apps import init_app

os.environ.setdefault("APP_SETTINGS_MODULE", "config.settings.heroku")

application = init_app()