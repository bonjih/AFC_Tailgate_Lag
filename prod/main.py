__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import time

from prod import image_detect, cv_image_processing, global_conf_variables
from prod import VariableClass, ErrorHandlingClass, db_manager, config_parser
from prod.utils import image_compare

# controls the error message sent interval in seconds
alarm_delay = 5


def img_processing_controller():
    img_meta_data = VariableClass.img_meta_data()
    cv_data_tup = cv_image_processing.cv_processing()
    cv_data = cv_data_tup[0] + cv_data_tup[1]
    image_data = (list(img_meta_data) + cv_data)
    return image_data


def db_manager_controller(dbfields, cv_data):
    image_data = VariableClass.format_image_data(cv_data)
    values = global_conf_variables.get_values()

    sql = db_manager.SQL(values[3], values[4], values[5], values[6])

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
            image_compare.main()
            time.sleep(alarm_delay)
            image_detect.watchdog_run()
            cv_img_data = img_processing_controller()
            db_fields = config_parser.db_json_parser()
            db_manager_controller(db_fields, cv_img_data)
        except Exception as e:
            ErrorHandlingClass.ErrorMessageHandler(e)


