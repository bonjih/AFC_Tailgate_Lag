__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

#############################################
# load jconfig.json
# if required, change variables in jconfig.json
#############################################
import json


def config_json_parser():
    with open(r'C:\Users\ben.hamilton\PycharmProjects\Anglo\config.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        pairs = data.items()
        return pairs


def db_json_parser():
    db_field_key = []

    with open(r'C:\Users\ben.hamilton\PycharmProjects\Anglo\db_fields.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        for key, value in data.items():
            db_field_key.append(key)
    return db_field_key
