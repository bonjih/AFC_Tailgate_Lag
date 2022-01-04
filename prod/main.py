__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import image_detect
import cv_image_processing
from prod.utils import image_compare
import VariableClass
import ErrorHandlingClass
import db_manager


import json

# controls the error message sent interval in seconds
alarm_delay = 5


#############################################
# load jconfig.json
# if required, change variables in jconfig.json
#############################################
def config_json_parser():
    config_values = []

    with open(r'C:\Users\ben.hamilton\PycharmProjects\Anglo\config.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        for key, value in data.items():
            config_values.append(value)
    return config_values


def db_json_parser():
    db_field_key = []

    with open(r'C:\Users\ben.hamilton\PycharmProjects\Anglo\db_fields.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        for key, value in data.items():
            db_field_key.append(key)
    return db_field_key


def img_processing_controller(jconfig):
    cv_data_tup = cv_image_processing.cv_processing(jconfig)
    cv_data = cv_data_tup[0] + cv_data_tup[1]
    img_meta_data = VariableClass.img_meta_data(jconfig)
    image_data = (list(img_meta_data) + cv_data)
    return image_data


def db_manager_controller(dbfields, cv_data):
    image_data = VariableClass.format_image_data(cv_data)
    sql = db_manager.SQL(jconfigs[2], jconfigs[3], jconfigs[4], jconfigs[5])

    # check if image existing in the db
    exists = sql.check_entry_exist(image_data[8])

    if not exists:
        sql.image_data(image_data, dbfields)
    else:
        print("latest image, '{}', already in the database, skipping....".format(image_data[8]))


if __name__ == "__main__":
    # loop forever, waits for a new image

    while True:
        print('Checking for latest image.....')

        try:
            jconfigs = config_json_parser()
            #image_compare.main(jconfigs)
            image_detect.watchdog_run(jconfigs)
            cv_img_data = img_processing_controller(jconfigs)
            db_fields = db_json_parser()
            db_manager_controller(db_fields, cv_img_data)

        except Exception as e:
            ErrorHandlingClass.ErrorMessageHandler(e)



