from importlib import metadata
from os.path import dirname

__version__ = metadata.version(__package__)
BASEDIR = dirname(__file__)
