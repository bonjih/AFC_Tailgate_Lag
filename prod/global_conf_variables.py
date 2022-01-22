__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

from prod.config_parser import config_json_parser

config = config_json_parser()


class GlobalVars:
    GELPhotos = config[0]  # image from GelPhotos folder
    file_type = config[1]
    filtered = config[2]  # where scripts puts new images to process cv
    user = config[3]
    passwd = config[4]
    host = config[5]
    database = config[6]
    known_distance = config[7]
    known_width = config[8]

    def __init__(self, configs):
        self.configs = configs
