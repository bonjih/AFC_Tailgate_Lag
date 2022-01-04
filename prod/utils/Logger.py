__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

from prod.LoggerClass import get_logger

log = get_logger()


class ErrorLog:

    def __init__(self, name):
        self.name = name

    def show(self):
        log.info("name: %s" % self.name)
