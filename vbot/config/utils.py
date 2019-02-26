import imp
from importlib import import_module


def is_module(module_path):
    return module_path is not None and isinstance(module_path, str)


def find_module(name):
    try:
        fp, pathname, description = imp.find_module(name)
    except ImportError:
        return (None, None)

    return fp, pathname, description


def load_module(name, fp, pathname, description):
    try:
        module = imp.load_module(name, fp, pathname, description)
    except Exception as error:
        raise ImportError(error)
    return module


def get_module(name):
    return import_module(name)
