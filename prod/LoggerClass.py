__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import logging
import os
import datetime

# All the log files are created inside ./logs/ dir with current date


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                    SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=SingletonType):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.DEBUG)

        # creating a logging format
        fmt = "[%(levelname)s] %(asctime)s :: %(filename)s:%(lineno)d -" \
            " %(funcName)s() | %(message)s"
        formatter = logging.Formatter(fmt)

        # ensuring that logs dir exist
        now = datetime.datetime.now()
        dirname = "./logs"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        # setting handlers
        fileHandler = logging.FileHandler(
                dirname + "/log_" + now.strftime("%Y-%m-%d")+".log")
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)


def get_logger():
    return Logger.__call__()._logger

