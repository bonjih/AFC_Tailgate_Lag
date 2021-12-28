__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American - email: "
__status__ = "Dev"

import image_detect
import db_manager
import cv_image_processing
from prod.utils import image_compare
import VariableClass
import ErrorHandlingClass

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
    cv_image_processing.load_image(jconfig)
    cv_data_tup = cv_image_processing.cv_processing(jconfig)
    cv_data = cv_data_tup[0] + cv_data_tup[1]
    img_meta_data = VariableClass.img_meta_data(jconfig)
    image_data = (list(img_meta_data) + cv_data)
    return image_data


def db_manager_controller(dbfields, cv_data):
    image_data = VariableClass.format_image_data(cv_data)
    db_manager.db_creds_json(jconfigs)
    db_manager.db_connect()

    # check if image existing in the db
    exists = db_manager.check_entry_exist(image_data[8])

    if not exists:
        db_manager.image_data(image_data, dbfields)  # for a single db insert
    else:
        print("latest image, '{}', already in the database, skipping....".format(image_data[8]))


if __name__ == "__main__":
    # loop forever, waits for a new image

    while True:
        print('Checking for latest image.....')

        try:
            jconfigs = config_json_parser()
            image_compare.main(jconfigs)
            image_detect.watchdog_run(jconfigs)
            cv_img_data = img_processing_controller(jconfigs)
            db_fields = db_json_parser()
            db_manager_controller(db_fields, cv_img_data)

        except Exception as e:
            ErrorHandlingClass.ErrorMessageHandler(e)
