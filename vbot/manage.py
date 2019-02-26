import os

from optparse import OptionParser

if __name__ == "__main__":

    op = OptionParser()

    op.add_option("-s", "--settings", type=str, default=None)

    (opts, args) = op.parse_args()

    if opts.settings is not None:
        os.environ.setdefault('APP_SETTINGS_MODULE', opts.settings)
    else:
        os.environ.setdefault('APP_SETTINGS_MODULE', 'config.settings.dev')

    try:
        from vbot.apps import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import App. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line()